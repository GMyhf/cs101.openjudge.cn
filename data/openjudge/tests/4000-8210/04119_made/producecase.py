import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '5 2\n'
SAMPLE_OUT = '2\n3\n3\n'
CASES = ['5 2\n', '20 19\n26 17\n9 7\n', '7 6\n39 15\n44 37\n', '39 22\n33 16\n', '38 32\n19 7\n', '46 32\n22 14\n17 6\n', '37 4\n46 10\n21 21\n', '24 19\n7 6\n33 24\n37 3\n24 4\n', '23 12\n27 25\n23 14\n3 2\n32 20\n', '18 12\n30 17\n', '24 13\n25 9\n22 7\n21 3\n', '13 13\n41 24\n', '7 3\n5 5\n', '34 14\n36 9\n8 1\n32 9\n', '46 32\n7 1\n13 11\n15 12\n', '31 11\n43 8\n50 2\n23 6\n', '46 44\n3 2\n21 6\n31 31\n', '33 13\n34 13\n', '21 9\n23 14\n', '7 3\n7 4\n46 12\n']
REFERENCE_SOURCE = '# https://blog.csdn.net/hejnhong/article/details/105211551\ndef divide_k(n, k):\n    # dp[i][j]为将i划分为j个正整数的划分方法数量\n    dp = [[0]*(k+1) for _ in range(n+1)]\n    for i in range(n+1):\n        dp[i][1] = 1\n    for i in range(1, n+1):\n        for j in range(1, k+1):\n            if i >= j:\n                # dp[i-1][j-1]为包含1的划分的数量\n                # 若不包含1，我们对每个数-1仍为正整数，划分数量为dp[i-j][j]\n                dp[i][j] = dp[i-j][j]+dp[i-1][j-1]\n    return dp[n][k]\n\n\ndef divide_dif(n):\n    # dp[i][j]表示将数字 i 划分，其中最大的数字不大于 j 的方法数量\n    dp = [[0] * (n + 1) for _ in range(n + 1)]\n    for i in range(1, n + 1):\n        for j in range(1, n + 1):\n            # 比i大的数没用\n            if i < j:\n                dp[i][j] = dp[i][i]\n            # 多了一种：不划分\n            elif i == j:\n                dp[i][j] = dp[i][j - 1] + 1\n            # 用/不用j\n            else:\n                dp[i][j] = dp[i][j - 1] + dp[i - j][j - 1]\n    return dp[n][n]\n\n\n# 关于分拆数的一个结论，https://zhuanlan.zhihu.com/p/21440865\n# 一个数的奇分拆总是等于互异分拆\ndef divide_odd(n):\n    # dp[i][j]整数i的划分里最大的数是j\n    dp = [[0] * (n + 1) for _ in range(n + 1)]\n    dp[0][0] = 1\n    for i in range(1, n + 1):\n        for j in range(1, n + 1):\n            if j % 2 == 0:\n                dp[i][j] = dp[i][j-1]\n            else:\n                if i < j:\n                    dp[i][j] = dp[i][i]\n                elif i == j:\n                    dp[i][j] = dp[i][j - 1] + 1\n                # 用/不用j\n                else:\n                    dp[i][j] = dp[i][j - 1] + dp[i - j][j]\n\n    return dp[n][n]\n\n\nwhile True:\n    try:\n        n, k = map(int, input().split())\n        print(divide_k(n, k))\n        print(divide_dif(n))\n        print(divide_odd(n))\n    except EOFError:\n        break\n\n'
assert CASES[0] == SAMPLE_IN
random.seed(4119)
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index in range(20):
    content = CASES[index]
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
