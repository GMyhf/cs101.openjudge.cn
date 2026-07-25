"""4121 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4121
SAMPLE_IN = '3\n7\n5 14 -2 4 9 3 17\n6\n6 8 7 4 1 -2\n4\n18 9 5 2\n'
SAMPLE_OUT = '28\n2\n0\n'
REFERENCE_SOURCE = 'def solve():\n    import sys\n    input = sys.stdin.readline\n\n    T = int(input().strip())\n    for _ in range(T):\n        N = int(input().strip())\n        prices = list(map(int, input().split()))\n\n        if N <= 1:\n            print(0)\n            continue\n\n        # 1. 从左到右，计算一次交易的最大利润\n        left = [0] * N\n        min_price = prices[0]\n        for i in range(1, N):\n            min_price = min(min_price, prices[i])\n            left[i] = max(left[i - 1], prices[i] - min_price)\n\n        # 2. 从右到左，计算一次交易的最大利润\n        right = [0] * N\n        max_price = prices[-1]\n        for i in range(N - 2, -1, -1):\n            max_price = max(max_price, prices[i])\n            right[i] = max(right[i + 1], max_price - prices[i])\n\n        # 3. 合并\n        res = 0\n        for i in range(N):\n            res = max(res, left[i] + right[i])\n\n        print(res)\n\nif __name__ == "__main__":\n    solve()\n'

def g4121(r):
    cases = []
    for _ in range(r.randint(1, 5)):
        n = r.randint(2, 100)
        prices = [r.randint(-1_000_000, 1_000_000) for _ in range(n)]
        cases.append(f"{n}\n" + " ".join(map(str, prices)))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4121(random.Random(NUMBER + i)) for i in range(1, 20)]

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
