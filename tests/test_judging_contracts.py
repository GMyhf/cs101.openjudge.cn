"""判题口径：2026-09-20 新加的三条，用**真实 `judge()` 跑真实数据**钉住。

这三条都不是格式问题，是「按题面写的正确程序会不会被判错」：

  · `case_insensitive_tokens` —— 题面明写「YES/NO 大小写随意」的题，此前照官方样例写
    `Yes` 会被 token 精确比对判 Wrong Answer。
  · `pairwise_sum_triple`（1154A）—— 题面写「a、b、c 任意顺序输出」，精确比对只认生成器那一种。
  · 2218F 题面正文里的那条规则：`If the number of test cases (t) = 2, I want you to add 1 to x`。
    生成器与特判原本都没实现它，而 21 组数据的 t 全是 2 —— 照题面写的程序全错。

每条都配一份**会挂的对照程序**：口径放宽之后，判据还得能把错的挡住，否则只是把闸门拆了。
"""
import unittest

from judge import judge


TWIST_2218F = '''import sys
data = sys.stdin.read().split()
t = int(data[0]); p = 1; out = []
for _ in range(t):
    x, y = int(data[p]), int(data[p + 1]); p += 2
    if t == 2: x += 1
    n = x + y
    if x > n // 2 or (n % 2 == 0 and x == 0):
        out.append("NO"); continue
    out.append("YES")
    nxt = 2; pairs = x if n % 2 else x - 1
    for _ in range(pairs):
        out.append(f"1 {nxt}"); out.append(f"{nxt} {nxt + 1}"); nxt += 2
    while nxt <= n:
        out.append(f"1 {nxt}"); nxt += 1
print("\\n".join(out))
'''

SORTED_1154A = '''import sys
data = sys.stdin.read().split()
values = sorted(map(int, data))
total = values[3]
print(total - values[0], total - values[1], total - values[2])
'''

REVERSED_1154A = SORTED_1154A.replace(
    "print(total - values[0], total - values[1], total - values[2])",
    "print(total - values[2], total - values[0], total - values[1])")

BOARD_ECHO_1154A = '''import sys
data = list(map(int, sys.stdin.read().split()))
print(data[0], data[1], data[2])
'''

TREE_2171D = '''import sys
data = sys.stdin.read().split()
t = int(data[0]); p = 1; out = []
for _ in range(t):
    n = int(data[p]); perm = list(map(int, data[p + 1:p + 1 + n])); p += 1 + n
    smallest, split = n + 1, False
    for length in range(1, n):
        smallest = min(smallest, perm[length - 1])
        if smallest == n - length + 1:
            split = True
            break
    out.append("No" if split else "Yes")
print("\\n".join(out))
'''

ALWAYS_YES_2171D = '''import sys
data = sys.stdin.read().split()
t = int(data[0]); p = 1; out = []
for _ in range(t):
    n = int(data[p]); p += 1 + n
    out.append("yes")
print("\\n".join(out))
'''


class JudgingContractTests(unittest.TestCase):
    def verdict(self, problem_id, source):
        return judge("codeforces", problem_id, "Python3", source)["status"]

    def test_2218f_follows_the_rule_hidden_in_the_statement(self):
        """t == 2 时 x 要加一。数据里 21 组的 t 全是 2，所以这条必须判得出来。"""
        self.assertEqual(self.verdict("2218F", TWIST_2218F), "Accepted")
        without_rule = TWIST_2218F.replace("    if t == 2: x += 1\n", "")
        self.assertEqual(self.verdict("2218F", without_rule), "Wrong Answer",
                         "漏掉题面那条规则的程序必须挂，否则数据没判别力")

    def test_2218f_accepts_the_official_samples_casing(self):
        lowercase = TWIST_2218F.replace('"YES"', '"Yes"').replace('"NO"', '"No"')
        self.assertEqual(self.verdict("2218F", lowercase), "Accepted")

    def test_1154a_accepts_any_order_but_not_any_triple(self):
        self.assertEqual(self.verdict("1154A", SORTED_1154A), "Accepted")
        self.assertEqual(self.verdict("1154A", REVERSED_1154A), "Accepted")
        self.assertEqual(self.verdict("1154A", BOARD_ECHO_1154A), "Wrong Answer")

    def test_2171d_accepts_either_casing_but_not_a_constant_answer(self):
        self.assertEqual(self.verdict("2171D", TREE_2171D), "Accepted")
        uppercase = TREE_2171D.replace('"No"', '"NO"').replace('"Yes"', '"YES"')
        self.assertEqual(self.verdict("2171D", uppercase), "Accepted")
        self.assertEqual(self.verdict("2171D", ALWAYS_YES_2171D), "Wrong Answer",
                         "大小写放宽之后，常量程序仍然必须挂")


if __name__ == "__main__":
    unittest.main()
