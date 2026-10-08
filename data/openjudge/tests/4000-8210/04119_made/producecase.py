"""4119 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

第 15-19 组为补充的边界组（替换了原先的随机组，组数不变）：N=1、K=1、K=N、N=50 取遍 K，以及全部 1275 个 (N, K) 组合。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4119
SAMPLE_IN = '5 2\n'
SAMPLE_OUT = '2\n3\n3\n'
REFERENCE_SOURCE = '# https://blog.csdn.net/hejnhong/article/details/105211551\ndef divide_k(n, k):\n    # dp[i][j]为将i划分为j个正整数的划分方法数量\n    dp = [[0]*(k+1) for _ in range(n+1)]\n    for i in range(n+1):\n        dp[i][1] = 1\n    for i in range(1, n+1):\n        for j in range(1, k+1):\n            if i >= j:\n                # dp[i-1][j-1]为包含1的划分的数量\n                # 若不包含1，我们对每个数-1仍为正整数，划分数量为dp[i-j][j]\n                dp[i][j] = dp[i-j][j]+dp[i-1][j-1]\n    return dp[n][k]\n\n\ndef divide_dif(n):\n    # dp[i][j]表示将数字 i 划分，其中最大的数字不大于 j 的方法数量\n    dp = [[0] * (n + 1) for _ in range(n + 1)]\n    for i in range(1, n + 1):\n        for j in range(1, n + 1):\n            # 比i大的数没用\n            if i < j:\n                dp[i][j] = dp[i][i]\n            # 多了一种：不划分\n            elif i == j:\n                dp[i][j] = dp[i][j - 1] + 1\n            # 用/不用j\n            else:\n                dp[i][j] = dp[i][j - 1] + dp[i - j][j - 1]\n    return dp[n][n]\n\n\n# 关于分拆数的一个结论，https://zhuanlan.zhihu.com/p/21440865\n# 一个数的奇分拆总是等于互异分拆\ndef divide_odd(n):\n    # dp[i][j]整数i的划分里最大的数是j\n    dp = [[0] * (n + 1) for _ in range(n + 1)]\n    dp[0][0] = 1\n    for i in range(1, n + 1):\n        for j in range(1, n + 1):\n            if j % 2 == 0:\n                dp[i][j] = dp[i][j-1]\n            else:\n                if i < j:\n                    dp[i][j] = dp[i][i]\n                elif i == j:\n                    dp[i][j] = dp[i][j - 1] + 1\n                # 用/不用j\n                else:\n                    dp[i][j] = dp[i][j - 1] + dp[i - j][j]\n\n    return dp[n][n]\n\n\nwhile True:\n    try:\n        n, k = map(int, input().split())\n        print(divide_k(n, k))\n        print(divide_dif(n))\n        print(divide_odd(n))\n    except EOFError:\n        break\n\n'

def g4119(r):
    count = r.randint(2, 5)
    pairs = []
    for _ in range(count):
        n = r.randint(1, 50)
        pairs.append((n, r.randint(1, n)))
    return "\n".join(f"{n} {k}" for n, k in pairs) + "\n"

EXTRA_CASES = [
    "1 1\n",                                                        # 15 最小规模
    "".join(f"{n} 1\n" for n in range(1, 51)),                      # 16 K=1，N 取遍 1..50
    "".join(f"50 {k}\n" for k in range(1, 51)),                     # 17 N=50，K 取遍 1..50
    "".join(f"{n} {n}\n" for n in range(50, 0, -1)),                # 18 K=N
    "".join(f"{n} {k}\n" for n in range(1, 51) for k in range(1, n + 1)),  # 19 全部 (N, K)
]


def valid(text):
    """题面：若干组测试数据，每组一行两个整数 N K（0 < N <= 50，0 < K <= N）。"""
    if not isinstance(text, str) or not text.endswith("\n") or "\r" in text:
        return False
    for line in text[:-1].split("\n"):
        parts = line.split(" ")
        if len(parts) != 2 or not all(re.fullmatch(r"[1-9]\d*", x) for x in parts):
            return False
        n, k = map(int, parts)
        if not (0 < n <= 50 and 0 < k <= n):
            return False
    return True


def build_cases():
    return [SAMPLE_IN] + [g4119(random.Random(NUMBER + i)) for i in range(1, 15)] + EXTRA_CASES

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    assert len(set(cases)) == len(cases), "存在重复组"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
