"""剩余下载数据的独立审核算法；夹具自带，不读取被忽略的后台下载。"""
import heapq
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import check_gmyhf_remaining as audit
import recheck_gmyhf_references as references
import report_gmyhf_followup as report


class IndependentAuditTests(unittest.TestCase):
    def test_blank_exam_answers_are_preserved_and_distinct_from_zero(self):
        self.assertEqual('0 1', audit.exam('1 3\n1 0 2\n\n0 1 0 0\n0 0 0 0\n'))
        self.assertEqual('2 0', audit.exam('1 2\n0 1\n\n\n'))
        with self.assertRaises(ValueError): audit.exam('1 2\n0 1\n\n')
        with self.assertRaises(ValueError): audit.exam('1 2\n0 0\n\n\n')

    def test_contract_driver_does_not_strip_exam_answer_lines(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work); data = root/'data'; data.mkdir()
            text = '1 2\n0 1\n\n\n'
            (data/'0.in').write_text(text)
            module = root/'producecase.py'
            module.write_text('def valid(text):\n    return text == '+repr(text)+'\n')
            result = subprocess.run([sys.executable, '-c', references.contract_driver(16531),
                                     str(module), str(data), '16531'], text=True, capture_output=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual([], json.loads(result.stdout))
            # 原文不通过时也不能删答题行后再把它标成通过。
            module.write_text('def valid(text):\n    return text == '+repr(text.rstrip('\n')+'\n')+'\n')
            result = subprocess.run([sys.executable, '-c', references.contract_driver(16531),
                                     str(module), str(data), '16531'], text=True, capture_output=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(1, len(json.loads(result.stdout)))

    def test_lattice_formula_matches_direct_eight_direction_graph(self):
        # 独立最短路覆盖斜走更便宜、轴向更便宜、奇偶性及零距离。
        for costs in itertools.product(range(1, 4), repeat=3):
            a, b, c = costs
            distances = {(0, 0): 0}; queue = [(0, 0, 0)]
            while queue:
                cost, x, y = heapq.heappop(queue)
                if cost != distances[x, y]: continue
                for dx, dy in itertools.product((-1, 0, 1), repeat=2):
                    if not (dx or dy): continue
                    xx, yy = x+dx, y+dy
                    if not (-5 <= xx <= 5 and -5 <= yy <= 5): continue
                    candidate = cost+(c if dx and dy else a if dx else b)
                    if candidate < distances.get((xx, yy), 10**10):
                        distances[xx, yy] = candidate
                        heapq.heappush(queue, (candidate, xx, yy))
            for x, y in itertools.product(range(5), repeat=2):
                self.assertEqual(distances[x, y], audit.lattice_distance(x, y, costs), (costs, x, y))
        self.assertEqual(2, audit.lattice_distance(2, 0, (8, 8, 1)))
        self.assertEqual(8, audit.lattice_distance(1, 0, (8, 8, 1)))

    def test_cookie_hall_deficit_matches_exhaustive_matching(self):
        rng = random.Random(18104)
        for _ in range(150):
            children = [rng.randrange(4) for _ in range(rng.randrange(5))]
            biscuits = [rng.randrange(4) for _ in range(rng.randrange(5))]

            def brute(index, used):
                if index == len(children): return 0
                return max([brute(index+1, used)]+[1+brute(index+1, used | {j})
                           for j, s in enumerate(biscuits) if j not in used and s >= children[index]])

            text = ' '.join(map(str, children))+'\n'+' '.join(map(str, biscuits))+'\n'
            self.assertEqual(str(brute(0, set())), audit.cookies(text))

    def test_separators_match_shortlex_enumeration(self):
        names = [''.join(p) for width in range(1, 4) for p in itertools.product('AB', repeat=width)]
        candidates = [''.join(p) for width in range(1, 4) for p in itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', repeat=width)]
        for lo, hi in itertools.combinations(sorted(names), 2):
            expected = next(s for s in candidates if lo <= s < hi)
            self.assertEqual(expected, audit.separator(f'2\n{lo}\n{hi}\n'))

    def test_forbidden_queries_match_literal_cartesian_product(self):
        words = [''.join(p) for n in range(1, 4) for p in itertools.product('ab', repeat=n)]
        pairs = list(itertools.product('ab', repeat=2))
        for a, b in itertools.product(words, repeat=2):
            for mask in range(16):
                banned = {pair for i, pair in enumerate(pairs) if mask & (1 << i)}
                expanded = ''.join(x+y for x in a for y in b if (x, y) not in banned)
                text = f'{len(a)} {len(b)} {len(banned)} {len(expanded)}\n{a}\n{b}\n'
                text += ''.join(f'{x} {y}\n' for x, y in sorted(banned))
                text += ''.join(f'{i}\n' for i in range(len(expanded)))
                self.assertEqual(list(expanded), audit.forbidden(text).split())
        with self.assertRaises(ValueError): audit.forbidden('1 1 0 1\na\nb\n2\n')

    def test_statement_boundaries_and_independent_answers(self):
        cases = [
            (audit.components, '1\n2 2\nW.\n.W\n', '2'),
            (audit.arbitrage, '4 8\n18 14 15 17 10 11 10 14\n19 15 18 18 15 11 15 16\n16 18 13 10 17 13 14 17\n20 12 11 16 14 17 11 15\n', '1 3 38'),
            (audit.sma, '1\n1.0 2.00 3.0 4.00 5.0\n', '3.00'),
            (audit.houses, '3\n(10,90) (20,180) (30,270)\n100 200 300\n', '0'),
            (audit.circle, '3\n0\n1\n4\n', '1\n1\n8'),
            (audit.holiday, '3\n1.7 1.7 3\n1.7 1.8 4\n1.8 1.8 5\n', '8'),
            (audit.equations, '3\na==b b==c a!=c\n', 'False'),
            (audit.hashing, '4\n-1 4 -1\n', '4 0 4'),
            (audit.project, '3 3\n3 1 2\n3 1 1\n1 2 3\n', '5\n1 2\n3 1'),
            (audit.word_search, '2 2\nab\ncd\nab\n', '1 1\n0 1'),
            (audit.ladder, '3\nFOOL\nPOOL\nPOLL\nFOOL POLL\n', 'FOOL POOL POLL'),
            (audit.linear_system, '2\n0 1 2\n1 0 3\n', 'x1 = 3.00\nx2 = 2.00'),
            (audit.island, '2 2\n1 1\n1 0\n', '8'),
        ]
        for solver, text, expected in cases:
            with self.subTest(solver=solver.__name__): self.assertEqual(expected, solver(text))
        with self.assertRaises(ValueError): audit.linear_system('2\n1 1 2\n2 2 4\n')
        with self.assertRaises(ValueError): audit.island('3 3\n1 1 1\n1 0 1\n1 1 1\n')
        with self.assertRaises(ValueError): audit.ladder('4\nFOOL\nPOOL\nFOLL\nPOLL\nFOOL POLL\n')
        with self.assertRaises(ValueError): audit.arbitrage('2 5\n1 1 1 2 3\n2 2 2 3 4\n')

    def test_wrong_expression_is_distinct_from_illegal_input_characters(self):
        for text, expected in [('1+2*3', '7.00'), ('2**3**2', '512.00'), ('-2**2', '-4.00'),
                               ('1 2', 'WRONG'), ('unknown(2)', 'WRONG'), ('1/0', 'WRONG'),
                               ('sin(0)+cos(0)', '1.00')]:
            self.assertEqual(expected, audit.expression_value(text, {}))
        self.assertEqual('WRONG', audit.expressions('1\n0\nPKU is great.\n'))
        with self.assertRaises(ValueError): audit.expressions('1\n0\na=1\n')
        with self.assertRaises(RuntimeError): audit.expression_value('2**100000', {})

    def test_evidence_cannot_be_reused_after_pair_changes(self):
        import hashlib
        with tempfile.TemporaryDirectory() as work:
            path = Path(work)/'0.in'; path.write_text('input')
            output = path.with_suffix('.out'); output.write_text('answer')
            row = {'input': str(path), 'input_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                   'output_sha256': hashlib.sha256(output.read_bytes()).hexdigest()}
            report.bound_files([row])
            output.write_text('wrong')
            with self.assertRaises(ValueError): report.bound_files([row])
            output.write_text('answer'); path.write_text('changed')
            with self.assertRaises(ValueError): report.bound_files([row])

    def test_routes_include_all_optimal_pickup_orders(self):
        text = '8 8 1\na 2 0\nb 2 0\nc 2 0\n'
        routes = audit.part_routes(text)
        best = min(cost for cost, _ in routes)
        optimal = [names for cost, names in routes if cost == best]
        self.assertIn(('a', 'b', 'c'), optimal)
        self.assertEqual(6, len(optimal))
        self.assertEqual(10, audit.lattice_graph_check('8 8 1\na 0 0\nb 1 0\nc 2 0\n'))


if __name__ == '__main__':
    unittest.main()
