"""28190 的零解、严格端点与可复现自产数据；20139 的废弃决定。"""
import contextlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import materialize_gmyhf_downloads

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'data/openjudge/tests/20000-29982/28190_made'


def brute(heights):
    """直接枚举连续区间，以两端为严格最小/最大值。"""
    answer = 0
    for left in range(len(heights)):
        for right in range(left + 1, len(heights)):
            middle = heights[left + 1:right]
            if heights[left] < heights[right] and all(
                    heights[left] < value < heights[right] for value in middle):
                answer = max(answer, right - left + 1)
    return answer


def reference(code, heights):
    lines = iter([str(len(heights)), *map(str, heights)])
    output = io.StringIO()
    with patch('builtins.input', side_effect=lambda: next(lines)), contextlib.redirect_stdout(output):
        exec(code, {'__name__': '__main__'})
    return int(output.getvalue())


def range_oracle(heights):
    """独立算法：下一不大于边界，区间内首次最大值作为最远合法右端。"""
    n = len(heights)
    bounds, stack = [n] * n, []
    for index, height in enumerate(heights):
        while stack and heights[stack[-1]] >= height:
            bounds[stack.pop()] = index
        stack.append(index)
    size = 1 << (n - 1).bit_length()
    tree = [(0, 0)] * (2 * size)
    for index, height in enumerate(heights):
        tree[size + index] = (height, -index)
    for index in range(size - 1, 0, -1):
        tree[index] = max(tree[2 * index], tree[2 * index + 1])
    answer = 0
    for index, bound in enumerate(bounds):
        left, right = size + index + 1, size + bound
        best = (0, 0)
        while left < right:
            if left % 2:
                best = max(best, tree[left])
                left += 1
            if right % 2:
                right -= 1
                best = max(best, tree[right])
            left //= 2
            right //= 2
        if best[0]:
            answer = max(answer, -best[1] - index + 1)
    return answer


def generator():
    spec = importlib.util.spec_from_file_location('cow_generator', DIRECTORY / 'producecase.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Review28190Tests(unittest.TestCase):
    def test_small_domain_and_official_samples(self):
        code = compile((DIRECTORY / 'samplecode.py').read_text(), 'samplecode.py', 'exec')
        for length in range(2, 9):
            for heights in itertools.product(range(1, 4), repeat=length):
                self.assertEqual(brute(heights), reference(code, heights), heights)
                self.assertEqual(brute(heights), range_oracle(heights), heights)
        self.assertEqual(4, reference(code, [1, 2, 3, 4, 1]))
        self.assertEqual(5, reference(code, [15, 15, 2, 13, 7, 4, 11, 5, 11, 12]))

    def test_all_answers_against_independent_range_oracle(self):
        paths = list((DIRECTORY / 'data').glob('*.in'))
        self.assertEqual(48, len(paths))
        for path in paths:
            count, *heights = map(int, path.read_text().split())
            self.assertEqual(count, len(heights))
            self.assertTrue(2 <= count <= 10**6)
            self.assertTrue(all(1 <= value < 2**31 for value in heights))
            self.assertEqual(range_oracle(heights), int(path.with_suffix('.out').read_text()), path.name)

    def test_generated_boundaries_and_reproduction(self):
        module = generator()
        self.assertEqual((DIRECTORY / 'samplecode.py').read_text(), module.REFERENCE)
        expected = [0, 0, 0, 0, 2, 2, 3, 3]
        for seed, answer in zip(range(40, 48), expected):
            text = module.generate(28190, seed)
            self.assertTrue(module.valid(28190, text))
            values = list(map(int, text.split()))
            self.assertEqual(values[0], len(values) - 1)
            self.assertTrue(2 <= values[0] <= 10**6)
            self.assertTrue(all(1 <= value < 2**31 for value in values[1:]))
            self.assertEqual(text, (DIRECTORY / f'data/{seed}.in').read_text())
            self.assertEqual(f'{answer}\n', (DIRECTORY / f'data/{seed}.out').read_text())
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            shutil.copyfile(DIRECTORY / 'producecase.py', folder / 'producecase.py')
            subprocess.run([sys.executable, '-I', str(folder / 'producecase.py')],
                           cwd=folder, check=True, capture_output=True, timeout=60)
            self.assertEqual(96, len(list((folder / 'data').iterdir())))
            for path in (DIRECTORY / 'data').iterdir():
                self.assertEqual(path.read_bytes(), (folder / 'data' / path.name).read_bytes(), path.name)

    def test_deprecated_20139_stays_excluded(self):
        self.assertIn(20139, materialize_gmyhf_downloads.MANUAL_EXCLUSIONS)
        catalog = json.loads((ROOT / 'data/openjudge/catalog.json').read_text())
        self.assertFalse(any(item.get('global_number') == 20139 and item.get('test_cases')
                             for item in catalog['problems']))


if __name__ == '__main__':
    unittest.main()
