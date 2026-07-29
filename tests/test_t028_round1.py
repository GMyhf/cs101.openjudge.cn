"""T-028 round1 generators must satisfy their named problem constraints."""
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import build_t028_round1 as round1


class Round1ConstraintTests(unittest.TestCase):
    def test_generated_cases_pass_and_specific_counterexamples_fail(self):
        self.assertEqual(len(round1.CONSTRAINTS), 20)
        self.assertEqual(len(set(round1.CONSTRAINTS.values())), 20)
        self.assertEqual(len(set(round1.COUNTEREXAMPLES.values())), 20)
        for number, generator in round1.GENERATORS.items():
            with self.subTest(number=number):
                self.assertFalse(round1.meaningful_check(number, round1.COUNTEREXAMPLES[number]))
                for seed in range(100):
                    self.assertTrue(round1.meaningful_check(number, generator(random.Random(seed))), seed)


if __name__ == "__main__":
    unittest.main()
