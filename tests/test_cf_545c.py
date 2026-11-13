"""545C：官方样例不能只供试运行，提交也必须判；答案用三状态 DP 独立核验。"""
import json
import unittest
from pathlib import Path

from judge import judge

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data/openjudge"
MADE = MIRROR / "tests/codeforces/545C_made"


def optimal(text):
    """枚举每棵树的左倒、站立、右倒状态，按占用区间检查相邻冲突。"""
    rows = [tuple(map(int, line.split())) for line in text.splitlines()[1:]]
    states = {float("-inf"): 0}
    for x, h in rows:
        next_states = {}
        for left, right, cut in ((x - h, x, 1), (x, x, 0), (x, x + h, 1)):
            scores = [score + cut for end, score in states.items() if end < left]
            if scores:
                next_states[right] = max(next_states.get(right, -1), max(scores))
        states = next_states
    return str(max(states.values()))


class WoodcuttersTests(unittest.TestCase):
    def test_active_cases_cover_both_samples_and_match_interval_dp(self):
        catalog = json.loads((MIRROR / "catalog.json").read_text())
        item = next(row for row in catalog["problems"]
                    if row.get("book") == "codeforces" and row["id"] == "545C")
        pairs = []
        for case in item["test_cases"]:
            text = (MIRROR / case["input"]).read_text()
            answer = (MIRROR / case["output"]).read_text().strip()
            self.assertEqual(answer, optimal(text), case["input"])
            pairs.append((text.split(), answer.split()))
        statement = json.loads((MIRROR / "statements/545C.json").read_text())
        for sample in statement["samples"]:
            self.assertEqual(optimal(sample["input"]), sample["output"].strip())
            self.assertTrue((sample["input"].split(), sample["output"].split()) in pairs,
                            "提交判题漏了官方样例")

    def test_reference_passes_and_reported_wrong_solution_fails(self):
        reference = (MADE / "samplecode.py").read_text()
        self.assertEqual(judge("codeforces", "545C", "python", reference)["status"], "Accepted")
        # 用户报告的错法：给下一棵树左倒预留空间，漏算了倒数第二棵向右倒。
        wrong = '''n = int(input())
a = [tuple(map(int, input().split())) for _ in range(n)]
cnt = min(n, 2)
for i in range(1, n - 1):
    if a[i][0] - a[i][1] > a[i - 1][0]:
        cnt += 1
    elif a[i+1][0] - a[i+1][1] > a[i][0] and a[i][0] + a[i][1] < a[i+1][0] - a[i+1][1]:
        cnt += 1
    elif a[i+1][0] - a[i+1][1] <= a[i][0] and a[i][0] + a[i][1] < a[i+1][0]:
        cnt += 1
print(cnt)
'''
        self.assertEqual(judge("codeforces", "545C", "python", wrong)["status"], "Wrong Answer")
