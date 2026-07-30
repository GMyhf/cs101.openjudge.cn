"""Regression tests for report-wide data-quality checks."""
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import full_sweep


class FullSweepConstraintTests(unittest.TestCase):
    def test_exact_decimal_exponentiation_is_a_documented_exception(self):
        self.assertIn(1001, full_sweep.ACCEPTED_REPEATING)
        self.assertIn("exact", full_sweep.ACCEPTED_REPEATING[1001])

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


class ArchiveOracleAuditabilityTests(unittest.TestCase):
    """oracle 可回查：round8 起报告要记下用了哪些存档目录，不能只记排除了谁。"""

    ENTRIES = [
        ("t028-round8-report.json", {"local_number": 1, "archive_cross_check": {"cases": 2}}),
        ("t028-round8-report.json", {"local_number": 2, "archive_cross_check": {"dirs": ["tests/x/1"]}}),
        ("t028-round9-report.json", {"local_number": 3,
                                     "archive_cross_check": {"no_archive_reason": "盘上没有存档"}}),
        ("t028-round7-report.json", {"local_number": 4, "archive_cross_check": {"cases": 1}}),
    ]

    def test_requires_recorded_dirs_from_round8_onwards(self):
        with mock.patch.object(full_sweep, "report_entries", return_value=iter(self.ENTRIES)):
            _label, bad = full_sweep.check_archive_oracle_is_auditable()
        # 只该报第 1 条：round8 且既没记 dirs 也没写「没有存档」的理由
        self.assertEqual(len(bad), 1, bad)
        self.assertIn("1（t028-round8-report.json）", bad[0])


class PriorityGapTests(unittest.TestCase):
    """跳过某个 priority 可以，不留痕不行 —— 没记录就等于没人在跟着它。"""

    def test_flags_a_priority_that_is_neither_built_nor_excluded(self):
        import json, tempfile, pathlib
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp); (root / "collab").mkdir()
            (root / "collab" / "t028-round1-manifest.json").write_text(json.dumps({
                "entries": [{"priority": 1}, {"priority": 2}, {"priority": 4}],
                "selection_exclusions": [{"priority": 3, "reason": "多解题"}],
            }), encoding="utf-8")
            with mock.patch.object(full_sweep, "ROOT", root):
                _label, bad = full_sweep.check_priority_gaps_are_recorded()
            self.assertEqual(bad, [], "3 已记录、1/2/4 已建，不该报")

            (root / "collab" / "t028-round1-manifest.json").write_text(json.dumps({
                "entries": [{"priority": 1}, {"priority": 2}, {"priority": 4}],
                "selection_exclusions": [],
            }), encoding="utf-8")
            with mock.patch.object(full_sweep, "ROOT", root):
                _label, bad = full_sweep.check_priority_gaps_are_recorded()
            self.assertEqual(len(bad), 1, bad)
            self.assertIn("priority 3", bad[0])


class SelfAuditMeasuredTests(unittest.TestCase):
    """自检数字必须是量出来的 —— T-002 立的规矩，现在搬进闸门。"""

    def test_flags_a_frequency_that_data_cannot_produce(self):
        import tempfile, pathlib
        with tempfile.TemporaryDirectory() as tmp:
            made = pathlib.Path(tmp) / "2000-2999" / "09999_made" / "data"
            made.mkdir(parents=True)
            for i, out in enumerate(["a", "b", "c"]):          # 三组、输出两两不同
                (made / f"{i}.in").write_text(f"{i}\n")
                (made / f"{i}.out").write_text(out + "\n")
            entry = {"local_number": 9999,
                     "self_audit": {"constant_output_probe": {"total": 2, "frequency": 2},
                                    "distinct_cases": {"total": 2, "distinct": 2}}}
            with mock.patch.object(full_sweep, "made_dirs",
                                   return_value=[(9999, made.parent)]), \
                 mock.patch.object(full_sweep, "report_entries",
                                   return_value=iter([("t028-round9-report.json", entry)])):
                _label, bad = full_sweep.check_self_audit_numbers_are_measured()
            self.assertEqual(len(bad), 1, bad)
            self.assertIn("frequency", bad[0])

            entry["self_audit"]["constant_output_probe"]["frequency"] = 1
            with mock.patch.object(full_sweep, "made_dirs",
                                   return_value=[(9999, made.parent)]), \
                 mock.patch.object(full_sweep, "report_entries",
                                   return_value=iter([("t028-round9-report.json", entry)])):
                _label, bad = full_sweep.check_self_audit_numbers_are_measured()
            self.assertEqual(bad, [], "改成实测值就该放行")


class InputDomainAnchorTests(unittest.TestCase):
    """把「题面范围」和「生成极值」钉在一起的判据（full_sweep 第 10 条）。

    这条判据是 2026-07-30 复核 round15-19 抓到七题「生成数据越出题面保证范围」之后加的
    （18106 题面 `1<=n<=20`、数据到 100；27625 题面 `0<n<50`、数据到 1000 …）。
    它只对 round20 起生效，所以**现在跑全库是绿的** —— 一条现在必然绿的判据，
    必须在这里证明它真能红，否则就是我自己批评过的「永远不会红的检查」。
    """

    def _entries(self, domain):
        return [("t028-round20-report.json", {"local_number": 18106, "input_domain": domain})]

    def _manifest(self, tmp):
        return {"task": "T-028", "entries": [{"local_number": 18106, "submit_group": "practice",
                                              "submit_id": "18106", "made_dir": "tests/x_made"}]}

    def _run(self, domain, quote_text, cases, made_rel="tests/x_made"):
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "collab").mkdir()
            (root / "data" / "openjudge" / "pages").mkdir(parents=True)
            data = root / "data" / "openjudge" / made_rel / "data"
            data.mkdir(parents=True)
            for index, case in enumerate(cases):
                (data / f"{index}.in").write_text(case, encoding="utf-8")
            (root / "data" / "openjudge" / "pages" / "practice__18106.html").write_text(
                f"<html><body><dd>{quote_text}</dd></body></html>", encoding="utf-8")
            (root / "collab" / "t028-round20-manifest.json").write_text(
                json.dumps(self._manifest(root)), encoding="utf-8")
            with mock.patch.object(full_sweep, "ROOT", root), \
                 mock.patch.object(full_sweep, "report_entries",
                                   return_value=iter(self._entries(domain))):
                return full_sweep.check_input_domain_is_anchored()[1]

    def test_accepts_a_verbatim_quote_with_recomputed_extremes(self):
        bad = self._run({"statement_quote": "给定一个n(1<=n<=20)",
                         "generated_extremes": {"max_int": 20, "min_int": 3}},
                        "给定一个n(1&lt;=n&lt;=20)，生成数组", ["3\n", "20\n"])
        self.assertEqual(bad, [])

    def test_rejects_a_quote_that_is_not_in_the_statement(self):
        bad = self._run({"statement_quote": "给定一个n(1<=n<=100)",
                         "generated_extremes": {"max_int": 20, "min_int": 3}},
                        "给定一个n(1&lt;=n&lt;=20)，生成数组", ["3\n", "20\n"])
        self.assertEqual(len(bad), 1)
        self.assertIn("找不到原话", bad[0])

    def test_rejects_extremes_that_disagree_with_the_data_on_disk(self):
        """报告说数据最大到 20，磁盘上其实有 100 —— 正是 18106 那条缺陷的形状。"""
        bad = self._run({"statement_quote": "给定一个n(1<=n<=20)",
                         "generated_extremes": {"max_int": 20, "min_int": 3}},
                        "给定一个n(1&lt;=n&lt;=20)，生成数组", ["3\n", "100\n"])
        self.assertEqual(len(bad), 1)
        self.assertIn("重算是", bad[0])

    def test_rejects_a_round20_entry_with_no_input_domain_at_all(self):
        bad = self._run(None, "给定一个n(1&lt;=n&lt;=20)", ["3\n"])
        self.assertEqual(len(bad), 1)
        self.assertIn("没有 input_domain", bad[0])

    def test_bare_less_than_in_the_statement_survives_tag_stripping(self):
        """题面里的 `1<=n<=20` 是裸的 `<`；按标签剥会把范围声明整段吃掉。"""
        text = full_sweep.statement_text.__doc__
        self.assertIn("裸的", text)

    def test_string_only_input_has_a_recomputable_zero_integer_state(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            made = Path(folder)
            data = made / "data"
            data.mkdir()
            (data / "0.in").write_text("ABCD\n", encoding="utf-8")
            self.assertEqual({"integer_tokens": 0}, full_sweep.generated_extremes(made))


class MultiAnswerUniqueFailureTests(unittest.TestCase):
    def _run(self, output):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            page_dir = root / "data" / "openjudge" / "pages"
            made = root / "data" / "openjudge" / "tests" / "30193_made"
            page_dir.mkdir(parents=True); (made / "data").mkdir(parents=True)
            (page_dir / "practice__30193.html").write_text(
                "<p>输出任意一种即可。</p>", encoding="utf-8")
            (made / "data" / "0.out").write_text(output, encoding="utf-8")
            entry = {"local_number": 30193,
                     "multi_answer_exemption": "only unique no-solution cases"}
            with mock.patch.object(full_sweep, "ROOT", root), \
                 mock.patch.object(full_sweep, "made_dirs", return_value=[(30193, made)]), \
                 mock.patch.object(full_sweep, "report_entries",
                                   return_value=iter([("t028-round21-report.json", entry)])):
                return full_sweep.check_multi_answer_problems()[1]

    def test_all_minus_one_outputs_are_unambiguous(self):
        self.assertEqual([], self._run("-1\n"))

    def test_a_path_output_reactivates_the_multi_answer_gate(self):
        self.assertEqual(1, len(self._run("1 1\n1 2\n")))
