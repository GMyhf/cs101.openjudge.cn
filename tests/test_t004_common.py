"""共享自检模块的回归测试。

这个模块存在的意义就是「让判据不会再退化成写死的字面量」，所以它自己的每条判据
都必须能输出「失败」。下面每个用例都成对写：一条证明通过路径、一条证明失败路径。
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import t004_common as common


class ExternalSourceAttributionTests(unittest.TestCase):
    """入库的第三方源码必须带出处与许可状态。

    2026-07-26 人拍板保留平台既有 Accepted 源码时明确要求注明「统计页 / 提交 ID /
    源码链接 / 许可状态」。round6 的 6 份做到了，round7/round8 新增的 42 份**一份都没有** ——
    署名写在流程里管不住，得有一条会红的检查。
    """

    ROOT = Path(__file__).resolve().parents[1]

    @staticmethod
    def _is_third_party(path):
        """判据用 `/solution/<id>/` 链接，不能只看有没有 openjudge.cn。

        T-002/T-003 的 samplecode 头部是 `# Source: /home/rocky/git/...openjudge.cn_problems.md`
        —— 那是人的本地题解合集路径，不是第三方平台提交。第一版判据把它们也算进来，
        一口气误报 90 个。**一个乱叫的检查会被整体忽略，比没有更糟。**
        """
        head = path.read_text(encoding="utf-8", errors="replace")[:800]
        return "/solution/" in head or "External reference" in head

    def _external_sources(self):
        staged = sorted(self.ROOT.glob("scripts/t004_platform_accepted_*"))
        shipped = [p for p in self.ROOT.glob("data/openjudge/tests/*/*_made/samplecode.*")
                   if self._is_third_party(p)]
        return staged + shipped

    def test_every_external_source_carries_provenance_and_license(self):
        missing = []
        for path in self._external_sources():
            head = path.read_text(encoding="utf-8", errors="replace")[:800]
            if "openjudge.cn" not in head:
                missing.append(f"{path.name}: 缺来源链接")
            elif "License" not in head and "许可" not in head:
                missing.append(f"{path.name}: 缺许可状态")
        self.assertEqual(missing, [], "入库的第三方源码缺署名：" + "; ".join(missing[:6]))

    def test_the_check_actually_looks_at_something(self):
        # 防「一个文件都没扫到也算通过」的空转
        self.assertGreater(len(self._external_sources()), 20)


class ConstantOutputProbeTests(unittest.TestCase):
    def test_all_outputs_identical_means_the_probe_accepts(self):
        # 21 组输出一模一样 -> 常量解法能过全部数据 -> 这份数据没有鉴别力。
        # round5 把这个字段写成了字面量 "rejected"，4140 的 21/21 就这么被盖住了。
        probe = common.constant_output_probe(["5.705085930\n"] * 21)
        self.assertEqual(probe["status"], "accepted")
        self.assertEqual((probe["frequency"], probe["total"]), (21, 21))

    def test_one_differing_output_is_enough_to_reject(self):
        probe = common.constant_output_probe(["1"] * 20 + ["2"])
        self.assertEqual(probe["status"], "rejected")
        self.assertEqual(probe["frequency"], 20)

    def test_token_semantics_match_the_judge(self):
        # 判题按 token 比对，探针也必须按 token，否则空白差异会假装成「有鉴别力」。
        self.assertEqual(common.constant_output_probe(["1 2", " 1  2 ", "1\n2"])["status"],
                         "accepted")


class DistinctCasesTests(unittest.TestCase):
    def test_below_threshold_without_exemption_fails(self):
        row = common.distinct_cases(["a"] * 18 + ["b", "c", "d"])
        self.assertEqual(row["status"], "FAILED")
        self.assertEqual(row["distinct"], 4)            # round5 的 4012 就是 4 组

    def test_below_threshold_with_exemption_is_recorded_not_hidden(self):
        row = common.distinct_cases(["x"], exemption="题面无输入，输入域只有 1 个取值")
        self.assertEqual(row["status"], "exempted")
        self.assertIn("题面无输入", row["exemption"])

    def test_at_threshold_passes(self):
        self.assertEqual(common.distinct_cases([str(i) for i in range(15)])["status"], "passed")


class ConstraintChecklistTests(unittest.TestCase):
    """「AC 源码直接当实现」之后，这条是唯一承重的检查，所以它必须能失败。"""

    def test_all_true_booleans_alone_are_not_enough(self):
        """契约 2026-07-26 收紧：每条都 True 只是必要条件，不是充分条件。

        round6 出现过三种「看着在测、其实测不出」的写法，其中两种静态扫不出来，
        所以还要求交付方给一个刻意违规的输入、证明这套谓词至少有一条会翻成 False。
        """
        row = common.constraint_checklist([("1<=n<=1000", True), ("两端不相等", True)])
        self.assertEqual(row["status"], "FAILED")
        self.assertEqual(row["checked"], 2)
        row = common.constraint_checklist(
            [("1<=n<=1000", True), ("两端不相等", True)],
            counterexample=("n=0 的输入", [("1<=n<=1000", False), ("两端不相等", True)]))
        self.assertEqual(row["status"], "passed")

    def test_empty_checklist_fails(self):
        # 不给打钩表就通过，等于这条检查不存在
        self.assertEqual(common.constraint_checklist([])["status"], "FAILED")
        self.assertEqual(common.constraint_checklist(None)["status"], "FAILED")

    def test_a_violated_constraint_fails(self):
        # 9202 的形状：题面写「两端不相等」，生成器却造了自环
        row = common.constraint_checklist([("1<=n<=25", True), ("边的两端不相等", False)])
        self.assertEqual(row["status"], "FAILED")
        self.assertIn("未满足", row["problems"][0])

    def test_without_a_counterexample_it_fails(self):
        # 每条都 True 说明不了什么——必须证明这套谓词能失败
        row = common.constraint_checklist([("1<=n<=1000", True)])
        self.assertEqual(row["status"], "FAILED")
        self.assertIn("反例", row["problems"][0])

    def test_counterexample_that_flips_nothing_fails(self):
        # round6 的 4112：len(x)<=2**31-1 真在计算，但要 2GB 一行才为假
        row = common.constraint_checklist(
            [("每行长度不超过 int 范围", True)],
            counterexample=("一行 900 字符", [("每行长度不超过 int 范围", True)]))
        self.assertEqual(row["status"], "FAILED")
        self.assertIn("装饰", row["problems"][0])

    def test_counterexample_that_flips_one_passes(self):
        row = common.constraint_checklist(
            [("边的两端不相等", True), ("1<=n<=25", True)],
            counterexample=("含自环的图", [("边的两端不相等", False), ("1<=n<=25", True)]))
        self.assertEqual(row["status"], "passed")
        self.assertEqual(row["falsified_by"]["constraints"], ["边的两端不相等"])

    def test_empty_checklist_with_exemption_is_exempted_not_missing(self):
        """无输入题（4140/4142）没有可检查的输入约束，但那要如实记成 exemption。

        round7 的 4142 一度是**整条字段消失** —— 「这项没出现」和「不适用」在报告里长得一样，
        和「忘了」也长得一样。现在 audit() 总会写这一项：空表无理由判 FAILED，给了理由才 exempted。
        """
        row = common.constraint_checklist([], exemption="题面无输入，没有可机械验证的输入约束")
        self.assertEqual(row["status"], "exempted")
        self.assertEqual(row["checked"], 0)
        self.assertEqual(common.constraint_checklist([])["status"], "FAILED")

    def test_exemption_is_recorded_when_nothing_is_checkable(self):
        row = common.constraint_checklist(
            [("输入为任意字符串", True)], exemption="题面对输入没有可机械验证的限制")
        self.assertEqual(row["status"], "exempted")
        self.assertIn("可机械验证", row["exemption"])

    def test_literal_instead_of_measured_boolean_fails(self):
        # 001d 的教训：字段写成字面量，看着通过、其实没测
        for fake in ("True", 1, None, "passed"):
            row = common.constraint_checklist([("1<=n<=10", fake)])
            self.assertEqual(row["status"], "FAILED", fake)
            self.assertIn("不是生成器实测的布尔", row["problems"][0])


class HasOracleTests(unittest.TestCase):
    def test_derives_from_the_implementation_not_a_list(self):
        def oracle(number, text):
            if number == 1:
                return "ok"
            raise LookupError(number)
        self.assertTrue(common.has_oracle(oracle, 1, ""))
        self.assertFalse(common.has_oracle(oracle, 2, ""))

    def test_a_real_error_is_not_swallowed_as_absent(self):
        # 只有 LookupError 才算「没实现」；其他异常是真 bug，必须抛出来，
        # 否则一个手滑的 NameError 会被静默记成「这题没有 oracle」。
        def oracle(number, text):
            raise ValueError("boom")
        with self.assertRaises(ValueError):
            common.has_oracle(oracle, 1, "")


class OracleIndependenceTests(unittest.TestCase):
    def test_renamed_copy_raises_the_alarm(self):
        reference = "\n".join(f"line{i} = compute({i})" for i in range(12))
        oracle = reference.replace("line3", "renamed3")     # 只改一行
        self.assertEqual(common.oracle_independence(reference, oracle)["status"], "ALARM")

    def test_short_implementations_sharing_boilerplate_do_not_alarm(self):
        # 回归：round5 的 3377 曾因两行模板（`while i<=j:` / `else:...`）被误报。
        # 一个乱叫的检查会被整体忽略，所以这条必须钉住。
        reference = ("n=int(a[0]);v=a[1:1+n];i,j=0,n-1;out=[]\n"
                     "while i<=j:\n"
                     "if v[i:j+1] <= v[i:j+1][::-1]:out.append(v[i]);i+=1\n"
                     "else:out.append(v[j]);j-=1\n"
                     'return "".join(out)+"\\n"')
        oracle = ("a=text.split(); v=a[1:1+int(a[0])]\n"
                  "i,j=0,len(v)-1; out=[]\n"
                  "while i<=j:\n"
                  "if v[i] < v[j]: out.append(v[i]); i+=1\n"
                  "elif v[i] > v[j]: out.append(v[j]); j-=1\n"
                  "else:\n"
                  "k=0\n"
                  "while i+k<=j-k and v[i+k]==v[j-k]: k+=1\n"
                  "if i+k>j-k or v[i+k] < v[j-k]: out.append(v[i]); i+=1\n"
                  "else:out.append(v[j]);j-=1\n"
                  "return ''.join(out)+'\\n'")
        row = common.oracle_independence(reference, oracle)
        self.assertEqual(row["status"], "passed", row)

    def test_identical_one_liner_alarms(self):
        # round5 的 4140：参考解法与 oracle 是同一句写死的常量。
        line = 'return "5.705085930\\n"'
        self.assertEqual(common.oracle_independence(line, line)["status"], "ALARM")


class MutationTests(unittest.TestCase):
    @staticmethod
    def _run(source, case):
        return source.replace("X", case)          # 一个便于观察的假 run

    def test_no_op_mutation_fails(self):
        # 变异串没匹配上 -> 源码没变 -> 探针在测一个不存在的变化。
        row = common.mutation_is_effective(self._run, "same", "same", ["a", "b"])
        self.assertEqual(row["status"], "FAILED")

    def test_mutation_that_changes_no_output_fails(self):
        # 源码变了但落在死代码上：21 组输出一模一样。round4 抓到过 3 条这样的。
        row = common.mutation_is_effective(lambda src, case: "constant",
                                           "before", "after", ["a", "b", "c"])
        self.assertEqual(row["status"], "FAILED")
        self.assertEqual(row["changed_cases"], 0)

    def test_effective_mutation_passes(self):
        row = common.mutation_is_effective(self._run, "X", "Y", ["a", "b"])
        self.assertEqual(row["status"], "passed")
        self.assertEqual(row["changed_cases"], 2)


def _make_fixture(folder, *, cases, sample="1 2\n", broken_reference=False):
    """搭一个最小的 `_made` 目录：samplecode.py 求和，producecase.py 固定重放。"""
    made = Path(folder) / "00001_made"
    (made / "data").mkdir(parents=True)
    for index, text in enumerate(cases):
        (made / "data" / f"{index}.in").write_text(text, encoding="utf-8")
        total = "999" if broken_reference and index else str(sum(int(x) for x in text.split()))
        (made / "data" / f"{index}.out").write_text(total + "\n", encoding="utf-8")
    (made / "samplecode.py").write_text(
        "import sys\nprint(sum(int(x) for x in sys.stdin.read().split()))\n", encoding="utf-8")
    (made / "producecase.py").write_text(
        "from pathlib import Path\n"
        f"CASES = {cases!r}\n"
        "root = Path(__file__).parent / 'data'\n"
        "for i, c in enumerate(CASES):\n"
        "    (root / f'{i}.in').write_text(c, encoding='utf-8')\n"
        "    (root / f'{i}.out').write_text(str(sum(int(x) for x in c.split())) + '\\n', encoding='utf-8')\n",
        encoding="utf-8")
    return made


class DiskCheckTests(unittest.TestCase):
    def test_sample_must_be_case_zero(self):
        with tempfile.TemporaryDirectory() as folder:
            made = _make_fixture(folder, cases=["1 2\n", "3 4\n"])  # 0.out == "3\n"
            self.assertEqual(
                common.sample_is_case_zero(made, "1 2\n", "3\n")["status"], "passed")
            self.assertEqual(
                common.sample_is_case_zero(made, "9 9\n", "18\n")["status"], "FAILED")

    def test_sample_output_must_match_the_statement(self):
        """21006 的形状：输入对得上，但参考实现算错，输出与题面样例不符。

        这是六项检查里唯一拿**外部真值**做基准的一条 —— 其余五项都在拿数据自己
        跟自己比，参考实现错了它们照样全绿。
        """
        with tempfile.TemporaryDirectory() as folder:
            made = _make_fixture(folder, cases=["1 2\n", "3 4\n"])
            row = common.sample_is_case_zero(made, "1 2\n", "8\n")   # 题面说 8，数据是 3
            self.assertEqual(row["status"], "FAILED")
            self.assertEqual(row["input_matches"], "passed")          # 输入是对的
            self.assertEqual(row["output_matches"], "FAILED")         # 错在输出
            self.assertIn("与题面样例不符", row["output_reason"])

    def test_missing_sample_output_is_not_silently_skipped(self):
        """不传样例输出必须记 FAILED —— 「没给」不能和「不适用」「忘了」长得一样。"""
        with tempfile.TemporaryDirectory() as folder:
            made = _make_fixture(folder, cases=["1 2\n"])
            row = common.sample_is_case_zero(made, "1 2\n")
            self.assertEqual(row["status"], "FAILED")
            self.assertEqual(row["output_matches"], "FAILED")
            # 题面确实没给输出时，走豁免、并且理由要留在报告里
            ok = common.sample_is_case_zero(made, "1 2\n", None,
                                            sample_output_exemption="题面未给样例输出")
            self.assertEqual(ok["status"], "passed")
            self.assertEqual(ok["output_matches"], "exempted")
            self.assertEqual(ok["output_exemption"], "题面未给样例输出")

    def test_audit_always_carries_the_sample_output_verdict(self):
        """audit() 不能有「不传就没这个字段」的口子（4142 那条教训的同一形状）。"""
        with tempfile.TemporaryDirectory() as folder:
            made = _make_fixture(folder, cases=["1 2\n", "3 4\n"])
            row = common.audit(made, cases=["1 2\n", "3 4\n"], outputs=["3\n", "7\n"],
                               sample_input="1 2\n", run_byte_reproduction=False)
            self.assertIn("output_matches", row["sample_is_case_zero"])
            self.assertIn("sample_is_case_zero", row["failed"])

    def test_samplecode_recompute_catches_wrong_expected_output(self):
        with tempfile.TemporaryDirectory() as folder:
            good = _make_fixture(folder, cases=["1 2\n", "3 4\n"])
            self.assertEqual(common.samplecode_recompute(good)["status"], "passed")
        with tempfile.TemporaryDirectory() as folder:
            bad = _make_fixture(folder, cases=["1 2\n", "3 4\n"], broken_reference=True)
            row = common.samplecode_recompute(bad)
            self.assertEqual(row["status"], "FAILED")
            self.assertIn("1.in", row["mismatched"])

    def test_missing_samplecode_is_reported(self):
        # round5 的 3433 就是这种：目录里根本没有 samplecode.py。
        with tempfile.TemporaryDirectory() as folder:
            made = _make_fixture(folder, cases=["1 2\n"])
            (made / "samplecode.py").unlink()
            row = common.samplecode_recompute(made)
            self.assertEqual(row["status"], "FAILED")
            self.assertIn("samplecode.py", row["reason"])

    def test_byte_reproduction_passes_and_can_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            made = _make_fixture(folder, cases=["1 2\n", "3 4\n"])
            self.assertEqual(common.byte_reproduction(made)["status"], "passed")
            # 把入库数据改掉，重跑就对不上——这条检查必须能红。
            (made / "data" / "0.out").write_text("777\n", encoding="utf-8")
            row = common.byte_reproduction(made)
            self.assertEqual(row["status"], "FAILED")
            self.assertIn("0.out", row["differing_files"])

    def test_audit_collects_every_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            made = _make_fixture(folder, cases=["1 2\n"] * 21)      # 21 组全一样
            row = common.audit(made, cases=["1 2\n"] * 21, outputs=["3\n"] * 21,
                               sample_input="1 2\n", run_byte_reproduction=False)
            self.assertIn("distinct_cases", row["failed"])          # 去重 1 组
            self.assertIn("constant_output_probe", row["failed"])   # 常量解法必 AC


class PendingReworkStatusTests(unittest.TestCase):
    def test_status_is_derived_from_data_and_can_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "tests" / "20000-29982" / "24607_made" / "data"
            root.mkdir(parents=True)
            (root / "0.in").write_text("93 1\nH\n", encoding="utf-8")
            item = [{"local_number": 24607,
                     "machine_gate": {"metric": "max_input_field", "field": "N",
                                       "field_index": 0, "minimum": 10000}}]
            row = common.pending_rework_status(item, Path(folder) / "tests")
            self.assertEqual(row["status"], "FAILED")
            self.assertEqual(row["items"][0]["actual_maximum"], 93)
            (root / "1.in").write_text("10000 1\nH\n", encoding="utf-8")
            self.assertEqual(common.pending_rework_status(item, Path(folder) / "tests")["status"], "passed")


if __name__ == "__main__":
    unittest.main()
