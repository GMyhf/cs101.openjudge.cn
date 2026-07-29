"""T-028 rounds 2-4 keep priority order and executable input checks."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import t028_rounds2_4 as rounds  # noqa: E402


class Round234ConstraintTests(unittest.TestCase):
    def test_priority_slice_and_problem_specific_checks(self):
        entries=json.loads((ROOT/'collab/t028-candidates.json').read_text())['entries'][:60]
        numbers=[int(x['number']) for x in entries]
        self.assertEqual([x['priority'] for x in entries],list(range(1,61)))
        self.assertEqual(set(numbers),set(rounds.LABELS))
        self.assertEqual(len(set(rounds.LABELS.values())),60)
        counterexamples={n:f'invalid-{n}\n' for n in numbers}
        self.assertEqual(len(set(counterexamples.values())),60)
        for n in numbers:
            with self.subTest(number=n):
                self.assertFalse(rounds.valid(n,counterexamples[n]))
                for seed in range(100):
                    self.assertTrue(rounds.valid(n,rounds.generate(n,seed)),seed)


if __name__=='__main__':unittest.main()
