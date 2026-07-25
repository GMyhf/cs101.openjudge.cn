"""4080 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4080
SAMPLE_IN = '4\n1 1 3 5\n'
SAMPLE_OUT = '17\n'
REFERENCE_SOURCE = 'import heapq\n\ndef min_weighted_path_length(n, weights):\n    heapq.heapify(weights)\n    total = 0\n    while len(weights) > 1:\n        a = heapq.heappop(weights)\n        b = heapq.heappop(weights)\n        combined = a + b\n        total += combined\n        heapq.heappush(weights, combined)\n    return total\n\n# 读取输入\nn = int(input())\nweights = list(map(int, input().split()))\nprint(min_weighted_path_length(n, weights))\n'

def g4080(r):
    n = r.randint(1, 30); return f"{n}\n" + " ".join(str(r.randint(1, 1000)) for _ in range(n)) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4080(random.Random(NUMBER + i)) for i in range(1, 20)]

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
