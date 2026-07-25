"""4977 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4977
SAMPLE_IN = '3\n8\n300 207 155 299 298 170 158 65\n8\n65 158 170 298 299 155 207 300\n10\n2 1 3 4 5 6 7 8 9 10\n'
SAMPLE_OUT = '6\n6\n9\n'
REFERENCE_SOURCE = 'def max_increasing_subsequence(a):\n    n = len(a)\n    dpu = [1] * n\n    for i in range(1, n):\n        for j in range(i):\n            if a[i] > a[j]:\n                dpu[i] = max(dpu[i], dpu[j] + 1)\n    return max(dpu)\n\ndef max_decreasing_subsequence(a):\n    n = len(a)\n    dpd = [1] * n\n    for i in range(1, n):\n        for j in range(i):\n            if a[i] < a[j]:\n                dpd[i] = max(dpd[i], dpd[j] + 1)\n    return max(dpd)\n\ndef main():\n    k = int(input())\n    while k:\n        k -= 1\n        n = int(input())\n        a = list(map(int, input().split()))\n        mxu = max_increasing_subsequence(a)\n        mxd = max_decreasing_subsequence(a)\n        print(max(mxu, mxd))\n\nif __name__ == "__main__":\n    main()\n'

def g4977(r):
    k = r.randint(1, 5); cases = []
    for _ in range(k):
        n = r.randint(2, 90); values = r.sample(range(1, 10000), n)
        cases += [str(n), " ".join(map(str, values))]
    return str(k) + "\n" + "\n".join(cases) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4977(random.Random(NUMBER + i)) for i in range(1, 20)]

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
