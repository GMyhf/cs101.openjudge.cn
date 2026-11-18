"""接雨水的活数据须覆盖不蓄水及最大蓄水量，答案按定义独立复核。"""
import itertools
import json
from pathlib import Path
import tempfile
import unittest

from scripts import strengthen_26977 as boundary


class RainBoundaryTests(unittest.TestCase):
    def test_active_cases_cover_boundaries_and_have_correct_answers(self):
        catalog = json.loads((boundary.ROOT / 'data/openjudge/catalog.json').read_text())
        problems = [p for p in catalog['problems'] if p.get('global_number') == 26977]
        self.assertTrue(problems)
        for problem in problems:
            inputs = set()
            for case in problem['test_cases']:
                path = boundary.ROOT / 'data/openjudge' / case['input']
                text = path.read_text()
                self.assertTrue(boundary.valid(text), path)
                heights = list(map(int, text.split()))[1:]
                inputs.add(tuple(heights))
                left = itertools.accumulate(heights, max)
                right = list(itertools.accumulate(reversed(heights), max))[::-1]
                expected = sum(min(a, b) - h for a, b, h in zip(left, right, heights))
                output = boundary.ROOT / 'data/openjudge' / case['output']
                self.assertEqual(output.read_text().split(), [str(expected)], path)
            for purpose, heights in boundary.cases():
                self.assertIn(tuple(heights), inputs, purpose)

    def test_supplements_are_reproducible(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder)
            (directory / 'data').mkdir()
            boundary.build(directory)
            for path in directory.rglob('*'):
                if path.is_file():
                    self.assertEqual(path.read_bytes(),
                                     (boundary.DIRECTORY / path.relative_to(directory)).read_bytes())

    def test_contract_rejects_invalid_inputs(self):
        for text in ('0\n\n', '2\n1\n', '1\n-1\n', '1\n200001\n',
                     '20001\n' + '0 ' * 20001 + '\n', '1\n0\n0\n'):
            self.assertFalse(boundary.valid(text), text[:50])


if __name__ == '__main__':
    unittest.main()
