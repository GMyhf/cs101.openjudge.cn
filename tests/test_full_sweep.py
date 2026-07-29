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


class MultiAnswerDetectionTests(unittest.TestCase):
    """多解题判据要两头都对：抓住「随便哪个都算对」，放过「存在多解但题面自己消歧」。

    第一版判据这两头都错过：`multiple solutions` 一命中就报，于是误伤了 04012
    （「output the one whose first number is the smallest」—— 答案唯一）；
    `任意一[个种组]` 太松，误伤了 30931（「对任意一个右括号」是语法用词，跟输出无关）。
    """

    REAL = (
        "If there are multiple solutions for a given value of n, any one of them is acceptable.",
        "If there are several sequences of minimal length, output any one of them.",
        "如果有多个答案，输出任意一个即可。",
        "存在多组解时任选一组输出。",
    )
    FAKE = (
        "If there exists multiple solutions, output the one whose first number is the smallest",
        "对任意一个右括号，它必须与当前距离它最近的尚未匹配的左括号类型相同。",
        "输出一个整数，表示最大嵌套深度。",
        "若有多解，输出字典序最小的那个。",
    )

    def test_flags_only_statements_that_accept_any_valid_answer(self):
        for text in self.REAL:
            self.assertTrue(full_sweep.MULTI_ANSWER.search(text), text[:40])
        for text in self.FAKE:
            self.assertIsNone(full_sweep.MULTI_ANSWER.search(text), text[:40])
