"""数算 A 往年私有题：题面样例、独立定义、输入契约和实际判题。"""
import importlib.util
import itertools
import random
import unittest
from pathlib import Path

from judge import judge
from server import Handler

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/openjudge/tests/private'
IDS = range(1000004, 1000012)


def load(number, name):
    path = BASE / f'{number}_made' / f'{name}.py'
    spec = importlib.util.spec_from_file_location(f'{name}_{number}', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GENERATORS = {n: load(n, 'producecase') for n in IDS}


class DsaPrivateFinalTests(unittest.TestCase):
    def test_contracts_reject_out_of_range_and_malformed_inputs(self):
        invalid = {
            1000004: ['1 1 0 1\na\nb\n2\n', '1 1 1 1\na\nb\na b\n0\n',
                      '1 1 0 1\nA\nb\n0\n'],
            1000005: ['2\n1 1\n1 2\n', '1\n200001 1\n', '1\n1 0\n'],
            1000006: ['1\n-1 0\n', '1\n0 1000000001\n', '2\n0 0\n'],
            1000007: ['a\n00\n', 'A\n1\n', 'a\n2\n'],
            1000008: ['1\n2\n1\n', '1\n1\n200001\n', '0\n'],
            1000009: ['A\n', 'a'*100001+'\n', 'a\nb\n'],
            1000010: ['3\n1 2 1\n1 2 1\n', '2\n1 2 0\n', '2\n1 3 1\n'],
            1000011: ['3\n2 3\n3 2\n', '4\n1 2\n1 3\n1 4\n', '1\n'],
        }
        for number, examples in invalid.items():
            for text in examples:
                self.assertFalse(GENERATORS[number].valid(text), (number, text[:80]))

    def test_samples_and_all_input_contracts(self):
        handler = Handler.__new__(Handler)
        for number, module in GENERATORS.items():
            with self.subTest(problem=number):
                data = BASE / f'{number}_made/data'
                paths = sorted(data.glob('*.in'), key=lambda p: int(p.stem))
                self.assertEqual(len(paths), 21)
                self.assertEqual(paths[0].read_text(), module.SAMPLE_IN)
                self.assertEqual(paths[0].with_suffix('.out').read_text(), module.SAMPLE_OUT)
                page = ROOT / f'data/openjudge/pages/private__{number}.html'
                samples = handler.sample_io(page)['cases']
                self.assertEqual(samples[0]['input'].strip(), module.SAMPLE_IN.strip())
                self.assertEqual(samples[0]['output'].strip(), module.SAMPLE_OUT.strip())
                self.assertEqual(len(samples), {1000006: 2, 1000007: 3}.get(number, 1))
                for path in paths:
                    self.assertTrue(module.valid(path.read_text()), (number, path.name))
                self.assertFalse(module.valid(''), number)
                regenerated = list(module.cases(1))
                self.assertEqual(regenerated, [p.read_text() for p in paths])

    def test_small_data_match_independent_oracles(self):
        for number, module in GENERATORS.items():
            checked = 0
            for path in (BASE / f'{number}_made/data').glob('*.in'):
                # 最大组已经真判；这里对小组使用不同算法，避免自洽地全错。
                if path.stat().st_size > 20000:
                    continue
                expected = module.oracle(path.read_text())
                if expected is not None:
                    self.assertEqual(path.with_suffix('.out').read_text(), expected,
                                     (number, path.name))
                    checked += 1
            if number != 1000007:
                self.assertGreaterEqual(checked, 10, number)

    def test_common_wrong_answers_have_counterexamples(self):
        # 禁用后可能出现零长度块，且查询是从 0 开始。
        m = GENERATORS[1000004]
        self.assertEqual(m.reference.solve(m.render('ba', 'a', [('b', 'a')], [0, 1])), 'a\na\n')
        # 单叶哈夫曼树的代价为 0；不能把叶子数当作输入行数。
        self.assertEqual(GENERATORS[1000005].reference.solve('1\n7 1\n'), '0\n')
        self.assertEqual(GENERATORS[1000005].reference.solve('1\n7 3\n'), '35\n')
        # 重合点、斜率 ±1 包含在内，垂直且不重合的点不包含。
        self.assertEqual(GENERATORS[1000006].reference.solve('4\n0 0\n0 0\n1 1\n0 1\n'), '4\n')
        # 相邻相等不能组成三元回文，首尾重复可以。
        self.assertEqual(GENERATORS[1000008].reference.solve('2\n2\n1 1\n3\n1 2 1\n'), 'NO\nYES\n')
        # 已经重复两次无需添加；无真周期则必须再加一整份。
        self.assertEqual(GENERATORS[1000009].reference.solve('abab\n'), '0\n')
        self.assertEqual(GENERATORS[1000009].reference.solve('ab\n'), '2\n')
        # 唯一 MST 要求新边严格大于路径最大值，且树边也计入总和。
        self.assertEqual(GENERATORS[1000010].reference.solve('3\n1 2 1\n2 3 1\n'), '4\n')
        # 删除叶子会使原本平衡的祖先变得不平衡。
        self.assertEqual(GENERATORS[1000011].reference.solve('3\n1 2\n1 3\n'), '1\n')

    def test_huffman_matches_exhaustive_optimal_merging(self):
        """枚举所有二元合并顺序，与哈夫曼贪心算法独立。"""
        from functools import lru_cache

        @lru_cache(None)
        def optimum(weights):
            if len(weights) < 2:
                return 0
            return min(weights[i] + weights[j] + optimum(tuple(sorted(
                [v for k, v in enumerate(weights) if k not in (i, j)] + [weights[i]+weights[j]])))
                for i in range(len(weights)) for j in range(i+1, len(weights)))

        module = GENERATORS[1000005]
        for weights in itertools.combinations_with_replacement(range(1, 5), 6):
            rows = [(w, weights.count(w)) for w in sorted(set(weights))]
            self.assertEqual(int(module.reference.solve(module.render(rows))), optimum(weights))

    def test_conflict_count_matches_all_pairs(self):
        rng = random.Random(2024)
        module = GENERATORS[1000006]
        for _ in range(60):
            points = [(rng.randrange(10), rng.randrange(10)) for _ in range(30)]
            count = sum(abs(y-v) <= abs(x-u)
                        for (x, y), (u, v) in itertools.combinations(points, 2))
            self.assertEqual(int(module.reference.solve(module.render(points))), count)

    def test_matching_checker_accepts_alternatives_and_rejects_bad_answers(self):
        checker = load(1000007, 'checker')
        self.assertTrue(checker.check('abc\n000\n', 'z\n', 'abca\n'))
        self.assertTrue(checker.check('abc\n100\n', 'a\n', 'abc\n'))
        self.assertTrue(checker.check('aaaaa\n11110\n', 'aa\n', 'aa\n'))
        for data, output, answer in [
            ('abc\n100\n', '-1', 'abc'),
            ('abc\n000\n', 'a', 'z'),
            ('aaaaa\n11110\n', 'a', 'aa'),
            ('ababa\n10100\n', 'ababa', 'aba'),
            ('abc\n100\n', 'A', 'abc'),
            ('abc\n100\n', 'a b', 'abc'),
            ('abc\n100\n', '', 'abc'),
            ('abc\n100\n', 'x'*1000002, 'abc'),
        ]:
            self.assertFalse(checker.check(data, output, answer), (data, output[:20]))

    def test_matching_exhaustive_small_strings(self):
        module = GENERATORS[1000007]
        checker = load(1000007, 'checker')
        for n in range(1, 6):
            for chars in itertools.product('ab', repeat=n):
                s = ''.join(chars)
                for bits in itertools.product('01', repeat=n):
                    p = ''.join(bits)
                    text = module.render(s, p)
                    answer = module.reference.solve(text)
                    self.assertEqual(answer.strip() != '-1', module.possible(s, p), (s, p))
                    self.assertTrue(checker.check(text, answer, answer), (s, p))

    def test_large_tree_answers_and_integer_width(self):
        data = lambda n, i: (BASE / f'{n}_made/data/{i}.out').read_text()
        # 等权树：每条新边必须是 w+1；长链删掉唯一叶子后的大小是 n-1。
        self.assertEqual(int(data(1000010, 18)), 100001*100000*99999//2 - 99999)
        self.assertEqual(int(data(1000010, 19)), 100000*99999 - 99999)
        self.assertEqual(int(data(1000011, 18)), 49999*49998//2)
        self.assertEqual(int(data(1000006, 18)), 200000*199999//2)

    def test_reference_programs_accepted(self):
        for number in IDS:
            with self.subTest(problem=number):
                source = (BASE / f'{number}_made/samplecode.py').read_text()
                self.assertEqual(judge('private', str(number), 'python', source)['status'], 'Accepted')


if __name__ == '__main__':
    unittest.main()
