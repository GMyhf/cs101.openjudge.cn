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
    def test_stock_repair_preserves_each_price_difference(self):
        before = b'4\n0 8 2 5\n4 7 0 9\n'
        self.assertEqual(b'4\n1 9 3 6\n5 8 1 10\n', rules.repair_input(25579, before))
        self.assertEqual(b'3\n1 4 2\n2 5 9\n',
                         rules.repair_input(25579, b'3\n0 3 1\n2 5 9\n'))
        legal = b'3  2 3 4  9 7 1'
        self.assertEqual(legal, rules.repair_input(25579, legal))
        for bad in (b'2 1 2 3 4', b'3 0 1 2 3 4', b'3 -1 2 3 4 5 6'):
            with self.assertRaises(AssertionError):
                rules.repair_input(25579, bad)

    def test_stock_reference_against_all_transactions(self):
        solve = self.reference(25579, 11, 'stocks')
        rng = random.Random(606)
        for n in range(3, 8):
            for _ in range(30):
                rows = [[rng.randrange(6) for _ in range(n)] for _ in range(2)]
                trades = [(buy, sell, row[sell]-row[buy]) for row in rows
                          for buy in range(n) for sell in range(buy, n)]
                expected = max([0] + [p for b,s,p in trades] +
                               [p+q for b,s,p in trades for c,d,q in trades if s <= c])
                before = (' '.join(map(str, [n]+rows[0]+rows[1]))).encode()
                after = rules.repair_input(25579, before)
                self.assertEqual(str(expected), solve(before.decode()))
                self.assertEqual(str(expected), solve(after.decode()))

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

    def test_second_batch_rules_and_legal_inputs_unchanged(self):
        self.assertEqual(b'4\n1 4\n2 5\n3 6\n0 7\n',
                         rules.repair_input(27945, b'3\n1 4\n2 5\n3 6\n0 7\n'))
        self.assertEqual(b'2\npopSmallest\naddBack 1\n',
                         rules.repair_input(28014, b'1\npopSmallest\naddBack 1\n'))
        self.assertEqual(b'3\n1 10000\n2 1\n3 2346\n',
                         rules.repair_input(28191, b'3\n1 99999\n2 1\n3 23456\n'))
        fixed = rules.repair_input(28339, (' '.join(map(str, range(1,50002)))).encode())
        self.assertEqual(list(range(1,50001)), list(map(int,fixed.split())))
        self.assertEqual(b'3 1\n2 4\n', rules.repair_input(29905, b'3 1\n2 4 7\n'))
        for n, value in ((27945,b'2\n1 2\n3 4'), (28014,b'1\npopSmallest'),
                         (28191,b'2\n1 2\n2 3'), (28339,b'2 3'), (29905,b'2 1\n4')):
            self.assertEqual(value, rules.repair_input(n,value))

    def test_smallest_range_against_cartesian_choices(self):
        solve = self.reference(27945,13,'smallest_range')
        rng = random.Random(61)
        for _ in range(100):
            rows = [sorted(rng.sample(range(-5,10),3)) for _ in range(4)]
            expected = min((max(v)-min(v),min(v),max(v)) for v in itertools.product(*rows))
            text = '4\n'+'\n'.join(' '.join(map(str,row)) for row in rows)
            self.assertEqual(f'{expected[1]} {expected[2]}', solve(text))

    def test_infinite_set_against_explicit_set(self):
        solve = self.reference(28014,13,'infinite_set')
        rng = random.Random(62)
        remaining = set(range(1,2001))
        operations, expected = [], []
        for _ in range(1000):
            if rng.randrange(2):
                value = min(remaining)
                remaining.remove(value)
                expected.append(str(value))
                operations.append('popSmallest')
            else:
                value = rng.randrange(1,1001)
                remaining.add(value)
                operations.append(f'addBack {value}')
        self.assertEqual('\n'.join(expected),solve('1000\n'+'\n'.join(operations)))

    def test_stations_against_direct_nearest_higher(self):
        solve = self.reference(28191,13,'stations')
        rng = random.Random(63)
        for n in range(1,30):
            height = rng.sample(range(100),n)
            energy = [rng.randrange(1,10001) for _ in range(n)]
            received = [0]*n
            for i in range(n):
                for direction in (-1,1):
                    j = i+direction
                    while 0 <= j < n:
                        if height[j] > height[i]:
                            received[j] += energy[i]
                            break
                        j += direction
            text = str(n)+'\n'+'\n'.join(f'{h+1} {v}' for h,v in zip(height,energy))
            self.assertEqual(str(max(received)),solve(text))

    def test_deviation_against_all_reachable_choices(self):
        solve = self.reference(28339,13,'deviation')
        def reachable(x):
            choices = {x}
            if x%2:
                choices.add(x*2)
            else:
                while x%2 == 0:
                    x //= 2
                    choices.add(x)
            return choices
        for a in itertools.product(range(1,9),repeat=3):
            expected = min(max(v)-min(v) for v in itertools.product(*(reachable(x) for x in a)))
            self.assertEqual(str(expected),solve(' '.join(map(str,a))))

    def test_schools_against_all_school_locations(self):
        solve = self.reference(29905,14,'schools')
        for gaps in itertools.product(range(1,4),repeat=4):
            positions = [0]
            for gap in gaps:
                positions.append(positions[-1]+gap)
            for m in range(1,6):
                expected = min(sum(min(abs(x-school) for school in schools) for x in positions)
                               for schools in itertools.combinations(positions,m))
                self.assertEqual(str(expected),solve(f'5 {m}\n'+' '.join(map(str,gaps))))


    def test_third_batch_bounds_preserve_rows_and_parameters(self):
        matrix = [[100*i+j for j in range(21)] for i in range(21)]
        given = '21\n'+'\n'.join(' '.join(map(str,row)) for row in matrix)
        fixed = list(map(int,rules.repair_input(21471,given.encode()).split()))
        self.assertEqual([20]+[v for row in matrix[:20] for v in row[:20]],fixed)
        self.assertEqual(b'3 2\n2 3 2\n',rules.repair_input(25563,b'3 2\n1 3 2'))
        replacement = rules.repair_input(25577,b'3 2\n1 3 2').strip()
        self.assertTrue(replacement.isdigit())
        self.assertGreaterEqual(int(replacement),0)
        self.assertEqual(b'-1000 3 1000\n2\n1\n',rules.repair_input(27946,b'-2000 3 5000\n2\n1'))
        self.assertEqual(b'3 4\n1 3 5\n',rules.repair_input(30177,b'3 4\n1 3 5\n2 3\n1 2'))
        for n,value in ((21471,b'1\n7'),(25563,b'2 1\n2 3'),(25577,b'0'),
                        (27946,b'-1000 1000\n1\n0'),(30177,b'1 1\n1')):
            self.assertEqual(value,rules.repair_input(n,value))

    def test_attention_against_expanded_four_index_formula(self):
        solve = self.reference(21471,9,'attention')
        rng = random.Random(64)
        for n in range(1,6):
            for _ in range(10):
                a = [[rng.randrange(-4,5) for _ in range(n)] for _ in range(n)]
                expected = [[sum(a[i][r]*a[s][r]*a[s][j] for r in range(n) for s in range(n))
                             for j in range(n)] for i in range(n)]
                text = str(n)+'\n'+'\n'.join(' '.join(map(str,row)) for row in a)
                self.assertEqual([v for row in expected for v in row],list(map(int,solve(text).split())))

    def test_teams_against_every_contiguous_partition(self):
        solve = self.reference(25563,11,'teams')
        for a in itertools.product(range(2,5),repeat=5):
            for m in range(1,6):
                expected = min(max(sum(a[l:r]) for l,r in zip((0,)+cuts,cuts+(5,)))
                               for cuts in itertools.combinations(range(1,5),m-1))
                self.assertEqual(str(expected),solve(f'5 {m}\n'+' '.join(map(str,a))))

    def test_fibonacci_against_linear_exact_integer_recurrence(self):
        solve = self.reference(25577,11,'fibonacci')
        a,b = 0,1
        for n in range(10001):
            if n < 100 or n == 10000:
                self.assertEqual(str(a),solve(str(n)))
            a,b = b,a+b

    def test_close_duplicates_against_all_index_pairs(self):
        solve = self.reference(27946,13,'close_duplicates')
        rng = random.Random(65)
        for _ in range(300):
            a = [rng.randrange(-2000,2001) for _ in range(12)]
            k,d = rng.randrange(1,13),rng.randrange(1001)
            expected = any(j-i <= k and abs(a[i]-a[j]) <= d for i in range(12) for j in range(i+1,12))
            self.assertEqual('true' if expected else 'false',solve(' '.join(map(str,a))+f'\n{k}\n{d}'))

    def test_tickets_against_explicit_reachable_sums(self):
        solve = self.reference(30177,14,'tickets')
        for tail_size in range(4):
            for tail in itertools.combinations(range(2,9),tail_size):
                coins = (1,)+tail
                for k in range(1,5):
                    reachable = {0}
                    for _ in range(k):
                        reachable |= {x+c for x in reachable for c in coins}
                    first_missing = next(x for x in range(1,k*max(coins)+2) if x not in reachable)
                    self.assertEqual(str(first_missing-1),solve(f'{len(coins)} {k}\n'+' '.join(map(str,coins))))


    def test_tree_repair_keeps_forest_edges_and_connects_all_vertices(self):
        result = list(map(int,rules.repair_input(28187,b'5\n1 2\n2 3\n3 1\n0 4\n').split()))
        n = result[0]
        edges = list(zip(result[1::2],result[2::2]))
        self.assertEqual(4,len(edges))
        self.assertIn((1,2),edges)
        self.assertIn((2,3),edges)
        graph = [[] for _ in range(n+1)]
        for u,v in edges:
            self.assertTrue(1<=u<=n and 1<=v<=n and u!=v)
            graph[u].append(v);graph[v].append(u)
        reached = {1}
        todo = [1]
        while todo:
            for v in graph[todo.pop()]:
                if v not in reached:
                    reached.add(v);todo.append(v)
        self.assertEqual(set(range(1,n+1)),reached)

    def test_hotel_outgoing_edges_only_are_removed(self):
        result = list(map(int,rules.repair_input(28188,b'5\n0 1 0 1 0\n0 1 2 3 4\n').split()))
        self.assertEqual([5,0,1,0,1,0,0,1,0,3,0],result)

    def test_restaurant_total_preserves_whole_test_prefix(self):
        cases = [(400,[1]*400,[2]*400),(400,[3]*400,[4]*400),(300,[5]*300,[6]*300)]
        rows = ['3']
        for n,a,b in cases:
            rows += [str(n),' '.join(map(str,a)),' '.join(map(str,b))]
        result = list(map(int,rules.repair_input(28189,'\n'.join(rows).encode()).split()))
        expected = [2]
        for n,a,b in cases[:2]:expected += [n]+a+b
        self.assertEqual(expected,result)
        self.assertEqual(800,sum(c[0] for c in cases[:2]))

    def test_toy_names_are_distinct_and_steps_strictly_bounded(self):
        fixed = rules.repair_input(28682,b'4 2\n0 a\n1 a\n0 fixa\n1 c\n0 4\n1 1\n').decode().splitlines()
        people = [line.split() for line in fixed[1:5]]
        names = [name for d,name in people]
        self.assertEqual(4,len(set(names)))
        self.assertEqual(['a','fixa','c'],[names[i] for i in (0,2,3)])
        self.assertTrue(all(name.isascii() and name.isalpha() and len(name)<=10 for name in names))
        self.assertEqual(['0','1','0','1'],[d for d,name in people])
        self.assertEqual(['0 3','1 1'],fixed[5:])

    def test_mouse_ranks_are_distinct_and_preserve_unequal_order(self):
        health = [3,3,-2,100,100]
        ranks = list(map(int,rules.repair_input(28696,b'5\n3 3 -2 100 100').split()))[1:]
        self.assertEqual(5,len(set(ranks)))
        for i,j in itertools.product(range(5),repeat=2):
            if health[i]<health[j]:self.assertLess(ranks[i],ranks[j])

    def test_fifth_batch_valid_inputs_stay_byte_identical(self):
        for n,value in ((28187,b'2\n1 2'),(28188,b'2\n0 1\n0 1'),
                        (28189,b'1\n2\n1 1\n1 1'),(28682,b'2 1\n0 a\n1 b\n0 1'),(28696,b'2\n10 -3')):
            self.assertEqual(value,rules.repair_input(n,value))

    def test_vacation_against_all_deterministic_forward_paths(self):
        solve = self.reference(28188,13,'vacation')
        rng = random.Random(66)
        for _ in range(100):
            n = 8
            kinds = [rng.randrange(2) for _ in range(n)]
            kinds[-1] = 1
            parents = [rng.randrange(n+1) for _ in range(n)]
            parents = [p if not p or not kinds[p-1] else 0 for p in parents]
            graph = [[] for _ in range(n)]
            for i,p in enumerate(parents):
                if p:graph[p-1].append(i)
            candidates = []
            for start in range(n):
                path,seen,at = [],set(),start
                while at not in seen:
                    path.append(at+1);seen.add(at)
                    if kinds[at]:
                        candidates.append(path);break
                    if len(graph[at])!=1:break
                    at = graph[at][0]
            best = min(candidates,key=lambda p:(-len(p),p[-1]))
            given = str(n)+'\n'+' '.join(map(str,kinds))+'\n'+' '.join(map(str,parents))
            self.assertEqual([len(best)]+best,list(map(int,solve(given).split())))

    def test_restaurant_against_all_disjoint_affordable_groups(self):
        solve = self.reference(28189,13,'restaurant')
        rng = random.Random(67)
        for _ in range(80):
            n = 7
            a,b = [[rng.randrange(1,8) for _ in range(n)] for _ in range(2)]
            valid = [mask for mask in range(1,1<<n) if bin(mask).count('1')>=2 and
                     sum(b[i]-a[i] for i in range(n) if mask>>i&1)>=0]
            dp = [0]*(1<<n)
            for mask in range(1,1<<n):
                first = mask&-mask
                dp[mask] = dp[mask^first]
                for group in valid:
                    if group&first and group&mask==group:
                        dp[mask] = max(dp[mask],1+dp[mask^group])
            given = f'1\n{n}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))
            self.assertEqual(str(dp[-1]),solve(given))

    def test_toys_against_counting_each_individual_step(self):
        solve = self.reference(28682,13,'toys')
        rng = random.Random(68)
        for n in range(2,10):
            people = [(rng.randrange(2),chr(ord('a')+i)) for i in range(n)]
            commands = [(rng.randrange(2),rng.randrange(1,n)) for _ in range(20)]
            at = 0
            for direction,steps in commands:
                increment = -1 if direction==people[at][0] else 1
                for _ in range(steps):at=(at+increment)%n
            given = f'{n} 20\n'+'\n'.join(f'{d} {name}' for d,name in people)+'\n'+'\n'.join(f'{d} {s}' for d,s in commands)
            self.assertEqual(people[at][1],solve(given))

    def test_mice_against_all_pair_differences(self):
        solve = self.reference(28696,13,'mice')
        rng = random.Random(69)
        for n in range(2,20):
            a = rng.sample(range(-1000,1001),n)
            _,i,j = max((a[i]-a[j],i,j) for i in range(n) for j in range(n) if i!=j)
            self.assertEqual(f'{i+1} {j+1}',solve(str(n)+'\n'+' '.join(map(str,a))))



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
