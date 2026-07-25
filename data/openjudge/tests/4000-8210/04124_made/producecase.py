"""4124 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4124
SAMPLE_IN = '4\n0 10 20 999\n5 0 90 30\n99 50 0 10\n999 1 2 0\n'
SAMPLE_OUT = '100\n'
REFERENCE_SOURCE = 'import sys\n\ndef solve():\n    data = sys.stdin.read().strip().split()\n    if not data:\n        return\n    it = iter(data)\n    N = int(next(it))\n    cost = [[int(next(it)) for _ in range(N)] for _ in range(N)]\n\n    INF = 10**12\n    # dp[mask][i]: 已访问mask，最后在i的最小花费\n    dp = [[INF] * N for _ in range(1 << N)]\n    dp[1][0] = 0  # 起点(编号0)\n\n    for mask in range(1 << N):\n        for i in range(N):\n            if dp[mask][i] == INF:\n                continue\n            for j in range(N):\n                if mask >> j & 1:  # j 已经访问过\n                    continue\n                new_mask = mask | (1 << j)\n                dp[new_mask][j] = min(dp[new_mask][j],\n                                      dp[mask][i] + cost[i][j])\n\n    print(dp[(1 << N) - 1][N - 1])\n\nif __name__ == "__main__":\n    solve()\n'

def g4124(r):
    n = 16 if r.random() < .12 else r.randint(3, 12)
    matrix = []
    for i in range(n):
        row = [0 if i == j else r.randint(1, 9999) for j in range(n)]
        matrix.append(" ".join(map(str, row)))
    return str(n) + "\n" + "\n".join(matrix) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4124(random.Random(NUMBER + i)) for i in range(1, 20)]

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
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
