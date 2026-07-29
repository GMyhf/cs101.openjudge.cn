"""Regression tests for report-wide data-quality checks."""
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import full_sweep


class FullSweepConstraintTests(unittest.TestCase):
    def test_rejects_one_constraint_label_shared_by_an_entire_round(self):
        entries = [
            ("round.json", {"local_number": 1, "constraints": [["same label", True]],
                            "constraint_counterexample": "1\n"}),
            ("round.json", {"local_number": 2, "constraints": [["same label", True]],
                            "constraint_counterexample": "2\n"}),
        ]
        with mock.patch.object(full_sweep, "report_entries", return_value=iter(entries)):
            _label, bad = full_sweep.check_degenerate_constraints()
        self.assertEqual(len(bad), 1)
        self.assertIn("2 题共用同一约束", bad[0])

    def test_accepts_problem_specific_labels_and_counterexamples(self):
        entries = [
            ("round.json", {"local_number": 1, "constraints": [["n is 1..10", True]],
                            "constraint_counterexample": "0\n"}),
            ("round.json", {"local_number": 2, "constraints": [["x is positive", True]],
                            "constraint_counterexample": "-1\n"}),
        ]
        with mock.patch.object(full_sweep, "report_entries", return_value=iter(entries)):
            _label, bad = full_sweep.check_degenerate_constraints()
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
