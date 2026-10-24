"""第8批旧输入格式与边界：自产夹具及独立小域复算。"""
from decimal import Decimal, localcontext, ROUND_HALF_EVEN
from fractions import Fraction
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from gmyhf_review_fixes import repair_input


def reference(number, function):
    proof = next(e for e in json.loads((ROOT/'collab/gmyhf-pending-batch8-review.json').read_text())['entries']
                 if e['global_number'] == number)['authored_reference']
    assert hashlib.sha256(proof['source'].encode()).hexdigest() == proof['sha256']
    namespace = {}; exec(proof['source'].split('import sys\nsys.stdout.write')[0], namespace)
    return namespace[function]


class LegacyInputTests(unittest.TestCase):
    def test_luffy_clamps_only_upper_bounds(self):
        self.assertEqual(b'10000 17 10000\n', repair_input(19965, b'12345 17 54321'))
        self.assertEqual(b'10000 10000 10000\n', repair_input(19965, b'10001 10002 10003'))
        for given in (b'1 2 3\r\n', b'10000  10000 10000'):
            self.assertIs(given, repair_input(19965, given))
        for bad in (b'0 1 1', b'-1 2 3', b'1 2', b'1 2 3 4'):
            with self.assertRaises(AssertionError): repair_input(19965, bad)

    def test_cinema_restores_count_preserves_all_cases_and_layout(self):
        given = b'1 4 6\r\n0 11 9\r\n-50 4 6\r\n\r\n'
        after = b'3\n'+given
        self.assertEqual(after, repair_input(19974, given))
        self.assertIs(after, repair_input(19974, after))
        given = b'1\r\n-1 1 1\r\n'
        self.assertIs(given, repair_input(19974, given))
        for bad in (b'', b'0', b'2\n1 2 3', b'1 0 2', b'1 2 0', b'1 2 3 4', b'1\n1 2 3\n4 5 6'):
            with self.assertRaises(AssertionError): repair_input(19974, bad)

    def test_synthesis_removes_only_out_of_triangle_cell(self):
        rows = [' '.join(['1']*(i+1)) for i in range(10)]
        rows[8] += ' 0.7'
        given = ('10\r\n120\r\n'+'\r\n'.join(rows)+'\r\n').encode()
        expected = given.replace(b'1 1 1 1 1 1 1 1 1 0.7', b'1 1 1 1 1 1 1 1 1 ')
        self.assertEqual(expected, repair_input(19984, given))
        self.assertIs(expected, repair_input(19984, expected))
        self.assertIs(b'1\n0\n0.256\n', repair_input(19984, b'1\n0\n0.256\n'))
        given = ('20\n100\n'+'\n'.join(' '.join(['1']*(i+1)) for i in range(20))+'\n').encode()
        self.assertIs(given, repair_input(19984, given))

    def test_synthesis_rejects_unknown_schema_unreachable_or_ties(self):
        for bad in (b'0\n100\n', b'21\n100\n', b'1\n100\n0\n', b'1\n100\n1.1\n',
                    b'1\n100\n-0.1\n', b'1\n100\n1 1\n', b'2\n100\n1\n0.5 0.75\n',
                    b'2\n100\n1\n1\n', b'1\n100\n1\n1\n'):
            with self.subTest(bad=bad), self.assertRaises(AssertionError): repair_input(19984, bad)

    def test_luffy_reference_against_all_meat_consumption_choices(self):
        solve = reference(19965, 'luffy')
        for a in range(1, 10):
            @lru_cache(None)
            def best(b, c):
                answer = b
                for used in range(1, c+1):
                    if used*b >= a:
                        answer = max(answer, best(b+a//b, c-used))
                return answer
            for b in range(1, 12):
                for c in range(1, 16):
                    self.assertEqual(str(best(b,c)), solve(f'{a} {b} {c}'))

    def test_cinema_reference_against_lattice_paths_on_both_sides(self):
        solve = reference(19974, 'cinema')
        for m in range(-4, 5):
            for p in range(1, 8):
                for q in range(1, 8):
                    paths = [[0]*(q+1) for _ in range(p+1)]
                    for x in range(p+1):
                        for y in range(q+1):
                            if y-x == m: continue
                            if x == y == 0: paths[x][y] = 1
                            else: paths[x][y] = (paths[x-1][y] if x else 0)+(paths[x][y-1] if y else 0)
                    self.assertEqual(str(paths[p][q]), solve(f'1\n{m} {p} {q}'))

    def test_synthesis_reference_against_credit_equation_and_decimal_rounding(self):
        solve = reference(19984, 'synthesis')
        self.assertEqual('0\n390.62', solve('1\n0\n0.256'))
        self.assertEqual('0\n1171.88', solve('1\n100\n0.256'))
        for base in (1, 7, 100):
            for probs in itertools.product(('0.5', '0.75', '1'), repeat=6):
                costs = [Fraction(base)]; route = []; at = 0
                for i in range(3):
                    previous = costs[i-1] if i else 0
                    options = []
                    for j in range(i+1):
                        p = Fraction(probs[at]); at += 1
                        # 先扣除全部低级副产品，损失部分按成功率摊销，再补回保留价值。
                        options.append(previous+(costs[i]+costs[j]+100-previous)/p)
                    route.append(options.index(min(options))); costs.append(min(options))
                with localcontext() as context:
                    context.prec = 100
                    price = (Decimal(costs[-1].numerator)/Decimal(costs[-1].denominator)).quantize(Decimal('0.01'),rounding=ROUND_HALF_EVEN)
                text = f'3\n{base}\n{probs[0]}\n'+ ' '.join(probs[1:3])+'\n'+' '.join(probs[3:])
                self.assertEqual(' '.join(map(str,route))+f'\n{price}', solve(text))
