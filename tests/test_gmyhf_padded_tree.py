"""完整孩子槽位循环的独立逐步模拟；不依赖抓取快照或后台。"""
from collections import deque
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import gmyhf_review_fixes as rules
import repair_gmyhf_review_findings as repair
import repair_gmyhf_sample_findings as statements


def reference():
    entry = next(e for e in json.loads((ROOT / 'collab/gmyhf-pending-batch14-review.json').read_text())['entries']
                 if e['global_number'] == 29663)
    proof = entry['authored_reference']
    assert hashlib.sha256(proof['source'].encode()).hexdigest() == proof['sha256']
    namespace = {}
    exec(proof['source'].split('import sys\nsys.stdout.write')[0], namespace)
    return namespace['shift_tree']


def slow_shift(text):
    """以节点编号映射保存边；每次只把一个槽位交给右侧，独立于切片参考。"""
    k, n, *values = map(int, text.split())
    assert n == len(values) and values[0] != -1
    children = {}; layers = []; queue = [0]; cursor = 1
    while queue:
        layers.append(queue[:]); following = []
        for parent in queue:
            row = []
            for _ in range(2):
                child = cursor if cursor < n and values[cursor] != -1 else None
                if cursor < n: cursor += 1
                row.append(child)
                if child is not None: following.append(child)
            children[parent] = row
        queue = following
    assert cursor == n
    for parents in reversed(layers):
        for _ in range(k % (2 * len(parents))):
            old = {p: children[p][:] for p in parents}
            for i, p in enumerate(parents):
                children[p] = [old[parents[i-1]][1], old[p][0]]
    result = []; queue = deque([0])
    while queue:
        node = queue.popleft()
        result.append(-1 if node is None else values[node])
        if node is not None: queue.extend(children[node])
    return ' '.join(map(str, result))


@lru_cache(None)
def shapes(n):
    if n == 0: return (None,)
    return tuple((left, right) for i in range(n) for left in shapes(i) for right in shapes(n-1-i))


def serialize(shape):
    result = []; queue = deque([shape]); value = 0
    while queue:
        node = queue.popleft()
        if node is None: result.append(-1)
        else:
            result.append(value); value += 1; queue.extend(node)
    return result


class PaddedTreeTests(unittest.TestCase):
    def test_padding_witness_and_bottom_up_order(self):
        solve = reference()
        self.assertEqual('1 -1 2 -1 -1', solve('1 2\n1 2'))
        self.assertEqual('1 3 2 -1 -1 -1 4 -1 -1', solve('1 4\n1 2 3 4'))
        self.assertEqual('1 2 3 4 -1 -1 -1 -1 -1', solve('1000 4\n1 2 3 4'))

    def test_all_small_shapes_and_all_trailing_null_omissions(self):
        solve = reference()
        checked = 0
        for n in range(1, 6):
            for shape in shapes(n):
                values = serialize(shape)
                while len(values) >= 2:
                    for k in (1, 2, 3, 4, 5, 7, 1000):
                        text = f'{k} {len(values)}\n' + ' '.join(map(str, values))
                        with self.subTest(n=n, k=k, values=values):
                            self.assertEqual(slow_shift(text), solve(text))
                            self.assertEqual(2*n+1, len(solve(text).split()))
                        checked += 1
                    if values[-1] != -1: break
                    values.pop()
        self.assertGreater(checked, 1000)

    def test_repair_changes_only_root_token_and_preserves_legal_bytes(self):
        before = b'390 8\r\n  -1  2 -1 3 4 -1 -1 5\r\n'
        after = before.replace(b'  -1', b'  0', 1)
        self.assertEqual(after, rules.repair_input(29663, before))
        self.assertIs(after, rules.repair_input(29663, after))
        for n, k in ((2, 1), (10001, 1000)):
            given = (f'{k} {n}\r\n' + '  '.join(['0']*n) + '\r\n').encode()
            self.assertIs(given, rules.repair_input(29663, given))

    def test_repair_rejects_unreachable_nodes_and_invalid_bounds(self):
        for given in (b'1 4\n1 -1 -1 7', b'1 4\n-1 -1 -1 7', b'0 2\n1 2',
                      b'1001 2\n1 2', b'1 1\n1', b'1 3\n1 2', b'1 2\n1 2 3',
                      ('1 10002\n'+'0 '*10002).encode()):
            with self.subTest(given=given[:80]), self.assertRaises(AssertionError):
                rules.repair_input(29663, given)

    def test_prepare_recomputes_unchanged_input_and_binds_confirmed_policy(self):
        source = 'import sys\nsys.stdout.write(' + repr('0 -1 2 -1 -1\n') + ')\n'
        with tempfile.TemporaryDirectory() as work:
            root = Path(work); base = root/'data/openjudge/tests/admin_download/29663'
            base.mkdir(parents=True); records = []; hashes = []
            for i, given in enumerate((b'1 2\n-1 2', b'1 2\n0 2')):
                for name, payload in ((f'{i}.in', given), (f'{i}.out', b'old\n')):
                    (base/name).write_bytes(payload)
                    hashes.append({'filename': name, 'sha256': repair.sha(payload)})
                records.append({'input': f'{i}.in', 'output': f'{i}.out',
                                'input_sha256': repair.sha(given), 'output_sha256': repair.sha(b'old\n')})
            entry = {'global_number': 29663, 'authored_reference': {'source': source, 'sha256': repair.sha(source.encode())},
                     'checks': {'readback': {'files': hashes}, 'answers': {'files': records}}}
            evidence = root/'collab/gmyhf-pending-batch14-review.json'; evidence.parent.mkdir()
            evidence.write_text(json.dumps({'entries': [entry]}))
            receipt = {'status': 'Accepted', 'timing_audit': {'status': 'passed'}}
            with patch.object(repair, 'ROOT', root), patch.object(repair.judge, 'judge', return_value=receipt):
                group = repair.prepare(15, root/'work')[0][0]
            self.assertEqual({'0.in', '0.out', '1.out'}, {c['filename'] for c in group['changes']})
            self.assertTrue(group['reference_policy']['recompute_all_answers'])
            self.assertEqual(1, group['repaired_inputs'])
            for i in range(2):
                self.assertEqual(b'0 -1 2 -1 -1\n', (root/group['local_dataset']/f'data/{i}.out').read_bytes())

    def test_statement_adds_only_confirmed_padding_rule(self):
        fields = {'description': '<p>旧题面</p>', 'input': '旧输入', 'output': '旧输出', 'hint': '',
                  'sampleInput': '1 2\n1 2', 'sampleOutput': '1 -1 2 -1 -1'}
        result = statements.repaired_form(29663, fields, ['1 -1 2 -1 -1'])
        self.assertEqual({'description'}, {k for k in fields if result[k] != fields[k]})
        self.assertTrue(result['description'].startswith(fields['description']))
        self.assertIn('每个非空父节点的左右孩子空位', result['description'])
        self.assertIn('末尾省略的空孩子也参与循环', result['description'])
        with self.assertRaises(AssertionError): statements.repaired_form(29663, result, ['1 -1 2 -1 -1'])
