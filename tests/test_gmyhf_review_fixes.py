"""输入修复、精确参考及平台回填保护；只用自产夹具和已入库源码。"""
import contextlib
import io
import itertools
import json
from pathlib import Path
import random
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import gmyhf_review_fixes as rules
import repair_gmyhf_review_findings as repair


class ReviewRulesTests(unittest.TestCase):
    def reference(self, number, batch, name):
        path = repair.ROOT / f'collab/gmyhf-pending-batch{batch}-review.json'
        entry = next(e for e in json.loads(path.read_text())['entries'] if e['global_number'] == number)
        source = entry['authored_reference']['source'].split('import sys\nsys.stdout.write')[0]
        namespace = {}
        exec(source, namespace)
        return namespace[name]

    def test_repair_bounds_and_preserve_other_values(self):
        before = b'12\n' + b' '.join(str(x).encode() for x in range(12)) + b'\n' + b' '.join(str(x).encode() for x in range(20, 32))
        fixed = list(map(int, rules.repair_input(19964, before).split()))
        self.assertEqual([10] + list(range(10)) + list(range(20, 30)), fixed)
        self.assertEqual(b'0' * 29 + b'\n' + b'1' * 29 + b'\n',
                         rules.repair_input(19968, b'0' * 30 + b'\n' + b'1' * 30))
        self.assertEqual(b'3 2 2\n4 5 6\n', rules.repair_input(30825, b'3 2 8\n4 5 6\n'))
        self.assertEqual(b'33 2\n', rules.repair_input(30920, b'33 1\n'))
        for n, value in ((19964, b'3\n1 2 3\n4 5 6'), (19968, b'0\n1'),
                         (30825, b'1 1 1\n9'), (30920, b'2 2')):
            self.assertEqual(value, rules.repair_input(n, value))
        with self.assertRaises(AssertionError):
            rules.repair_input(19964, b'12\n1 2')

    def test_ranges_exact_sample_and_empty_negative_singleton(self):
        self.assertEqual('["0->2","4->5","7"]', rules.canonical_ranges('0 1 2 4 5 7'))
        self.assertEqual('[]', rules.canonical_ranges('[]'))
        self.assertEqual('["-3->-1","4"]', rules.canonical_ranges('[-3,-2,-1,4]'))
        with self.assertRaises(AssertionError):
            rules.canonical_ranges('1 1')

    def test_assignment_against_all_permutations(self):
        solve = self.reference(19964, 16, 'assignment')
        rng = random.Random(60)
        for n in range(3, 8):
            for _ in range(8):
                a, b = [[rng.randrange(4) for _ in range(n)] for _ in range(2)]
                expected = max(sum((y > x) - (y < x) for x, y in zip(a, p)) for p in itertools.permutations(b))
                self.assertEqual(str(expected), solve(' '.join(map(str, [n] + a + b))))

    def test_toggle_reference_against_exhaustive_presses(self):
        solve = self.reference(19968, 16, 'toggles')
        for n in range(1, 9):
            possible = {}
            for mask in range(1 << n):
                result = (mask ^ (mask << 1) ^ (mask >> 1)) & ((1 << n) - 1)
                possible[result] = min(possible.get(result, n + 1), bin(mask).count('1'))
            for target in range(1 << n):
                self.assertEqual(str(possible.get(target, 'impossible')),
                                 solve('0' * n + '\n' + format(target, f'0{n}b')))

    def test_window_reference_against_direct_counting(self):
        solve = self.reference(30825, 15, 'frequency_windows')
        for a in itertools.product(range(1, 4), repeat=5):
            for w in range(1, 6):
                for k in range(1, w + 1):
                    expected = []
                    for i in range(6 - w):
                        window = a[i:i+w]
                        expected.append(min((v for v in set(window) if window.count(v) >= k), default=-1))
                    self.assertEqual(list(map(int, solve(' '.join(map(str, (5,w,k)+a))).split())), expected)

    def test_digits_reference_against_every_base(self):
        solve = self.reference(30920, 16, 'digits')
        for n in range(2, 151):
            for m in range(2, 12):
                best = 0
                for base in range(2, n + 1):
                    value, digits = n, []
                    while value:
                        value, digit = divmod(value, base)
                        digits.append(digit)
                    if max(digits) <= m:
                        best = max(best, sum(digits))
                self.assertEqual(str(best), solve(f'{n} {m}'))

    def test_reach_reference_against_graph_search(self):
        solve = self.reference(31415, 15, 'reach')
        for a in itertools.product(range(4), repeat=6):
            seen = {0}
            for i in range(len(a)):
                if i in seen:
                    seen.update(range(i + 1, min(len(a), i + a[i] + 1)))
            self.assertEqual('true' if len(a)-1 in seen else 'false', solve(' '.join(map(str,a))))


class ReviewUploadTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.live = {'a.in': b'33 1\n', 'a.out': b'1\n', 'note.txt': b'attachment'}
        self.uploads = []
        self.page = '<textarea name="description">fixture</textarea>' + ''.join(
            f'<a href="/admin/download?problem_id=42&filename={name}">下载</a>' for name in self.live)
        before = {n: repair.sha(v) for n,v in self.live.items()}
        after = {'a.in': b'33 2\n', 'a.out': b'2\n'}
        directory = self.root / 'local/data'
        directory.mkdir(parents=True)
        changes = []
        for name, value in after.items():
            (directory / name).write_bytes(value)
            changes.append({'filename': name, 'input': 'a.in', 'output': 'a.out',
                            'before_sha256': before[name], 'after_sha256': repair.sha(value),
                            'pair_before': {n:before[n] for n in after},
                            'pair_after': {n:repair.sha(v) for n,v in after.items()}})
        self.group = {'global_number':42, 'changes':changes, 'local_dataset':'local', 'baseline_files':before}
        entry = {'global_number':42, 'checks':{'statement':{'field_sha256':{'description':repair.sha(b'fixture')}}}}
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.object(repair, 'ROOT', self.root))
        # 绑定脚本哈希时需要真实规则源码，不依赖后台快照。
        (self.root / 'scripts').mkdir()
        (self.root / 'scripts/gmyhf_review_fixes.py').write_text('fixture')
        self.stack.enter_context(patch.object(repair, 'prepare', return_value=[(self.group, entry)]))
        self.stack.enter_context(patch.object(repair.subprocess, 'check_output', return_value='fixture\n'))
        session = self.stack.enter_context(patch.object(repair.platform.oj_submit, 'Session')).return_value
        session.login.return_value = session
        session._get.side_effect = lambda url:self.page
        self.stack.enter_context(patch.object(repair.platform, 'parse_form', return_value={'description':'fixture'}))
        self.stack.enter_context(patch.object(repair.platform, 'download', side_effect=lambda s,n,f:self.live[f]))
        self.stack.enter_context(patch.object(repair.platform, 'upload', side_effect=self.upload))
        self.stack.enter_context(contextlib.redirect_stdout(io.StringIO()))

    def upload(self, session, number, name, value):
        self.uploads.append(name)
        self.live[name] = value

    def run_repair(self, apply=True):
        repair.run(1, self.root / 'work', apply)

    def test_apply_pair_preserves_attachment_and_retry(self):
        self.run_repair()
        self.assertEqual(['a.in','a.out'], self.uploads)
        self.assertEqual({'a.in':b'33 2\n','a.out':b'2\n','note.txt':b'attachment'}, self.live)
        self.run_repair()
        self.assertEqual(['a.in','a.out'], self.uploads)

    def test_default_readonly(self):
        self.run_repair(False)
        self.assertEqual([], self.uploads)
        self.assertFalse((self.root / 'collab/gmyhf-review-fixes-batch1.json').exists())

    def test_drift_stops_all_writes(self):
        self.live['a.in'] = b'34 1\n'
        with self.assertRaises(ValueError):
            self.run_repair()
        self.assertEqual([], self.uploads)

    def test_readback_failure_does_not_claim_completion(self):
        with patch.object(repair.platform, 'upload', return_value=None):
            with self.assertRaises(ValueError):
                self.run_repair()
        self.assertFalse((self.root / 'collab/gmyhf-review-fixes-batch1.json').exists())
