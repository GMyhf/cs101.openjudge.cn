"""`rebuilt_tests` 的题：第 0 组必须是**题面的官方样例**。

单题流水线（`producecase.py` + `samplecode.py` + `valid()`）的外部锚点只有一个 ——
题面给的那组样例。它是唯一不出自我们自己代码的事实：生成器、参考实现、`valid()`
三者可以一起错，样例不会跟着错。

2026-09-20 加这条判据时，50 道里当场红了三道：

  · `1374C` 第 0 组把样例里的 `())()()(` 抄成了 `())()(()`（答案碰巧一样，锚点却没了）；
  · `2227B` 第 0 组放的是**另一道题**（1374C）的样例；
  · `2140B` 第 0 组是自造的 `1\\n6`，顺带暴露出它的参考实现只在 y < 10^5 里线性扫 ——
    官方样例的 x = 9876543 会让它直接抛异常，那根本不是这道题的正确解法。

输出侧：答案唯一的题连 `.out` 一起核；有 checker/interactor 的题只核输入，
因为「另一个同样合法的答案」本来就该被接受。
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data" / "openjudge"

# 第 0 组不是官方样例的题，必须在这里写明理由。
ANCHOR_EXEMPT = {
    "2109C1": "交互题：.in 里放的是交互器用的隐藏测试，不是题面样例的对话。",
    "2109C2": "交互题：同上。",
    "2109C3": "交互题：同上。",
    "2173E": "交互题：.in 是交互器用的排列，题面样例是一段对话。",
    "2209C": "交互题：.in 是交互器用的隐藏串。",
}


class RebuiltAnchorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog = json.loads((MIRROR / "catalog.json").read_text(encoding="utf-8"))
        cls.rows = [item for item in catalog["problems"]
                    if item.get("book") == "codeforces"
                    and item.get("data_status") == "rebuilt_tests"]
        cls.loose = {item["id"] for item in catalog["problems"]
                     if item.get("comparison") == "case_insensitive_tokens"}

    def statement_sample(self, problem_id):
        path = MIRROR / "statements" / f"{problem_id}.json"
        samples = json.loads(path.read_text(encoding="utf-8")).get("samples") or []
        return samples[0] if samples else None

    def test_case_zero_is_the_official_sample(self):
        failures = []
        for row in self.rows:
            problem_id = row["id"]
            if problem_id in ANCHOR_EXEMPT:
                continue
            sample = self.statement_sample(problem_id)
            if sample is None:
                failures.append(f"{problem_id}: 镜像题面里没有官方样例")
                continue
            data = MIRROR / "tests" / "codeforces" / f"{problem_id}_made" / "data"
            if (data / "0.in").read_text(encoding="utf-8").split() != sample["input"].split():
                failures.append(f"{problem_id}: 第 0 组的输入不是官方样例")
                continue
            if row.get("special_checker") or row.get("checker") or row.get("interactor"):
                continue                      # 答案不唯一，只钉输入
            expected = (data / "0.out").read_text(encoding="utf-8")
            if problem_id in self.loose:
                if expected.lower().split() != sample["output"].lower().split():
                    failures.append(f"{problem_id}: 第 0 组的输出与官方样例不符")
            elif expected.split() != sample["output"].split():
                failures.append(f"{problem_id}: 第 0 组的输出与官方样例不符")
        self.assertEqual(failures, [], "\n".join(failures))

    def test_every_exemption_has_a_reason(self):
        for problem_id, reason in ANCHOR_EXEMPT.items():
            self.assertTrue(reason.strip(), f"{problem_id} 的豁免理由不能是空的")
            path = MIRROR / "tests" / "codeforces" / f"{problem_id}_made"
            self.assertTrue((path / "interactor.py").is_file(),
                            f"{problem_id} 不是交互题，豁免理由不成立")


if __name__ == "__main__":
    unittest.main()
