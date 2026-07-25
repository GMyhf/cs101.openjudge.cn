"""7743 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 7743
SAMPLE_IN = '3 3\n3 4 1\n3 7 1\n2 0 1\n'
SAMPLE_OUT = '15\n'
REFERENCE_SOURCE = 'import sys\n\ndata = iter(sys.stdin.read().strip().split())\ntry:\n    m = int(next(data))\n    n = int(next(data))\nexcept StopIteration:\n    # 输入不足\n    print(0)\n    sys.exit()\n\n# 读取矩阵（假设输入格式正确，恰好有 m*n 个整数）\nmatrix = [[int(next(data)) for _ in range(n)] for _ in range(m)]\n\ntotal = 0\nif m == 0 or n == 0:\n    total = 0\nelif m == 1:\n    # 只有一行，边缘就是这一整行\n    total = sum(matrix[0])\nelif n == 1:\n    # 只有一列，边缘就是这一整列\n    total = sum(row[0] for row in matrix)\nelse:\n    # 普通情况：首行 + 末行 + 中间行的首列和末列\n    total += sum(matrix[0])      # 第一行\n    total += sum(matrix[-1])     # 最后一行\n    for i in range(1, m-1):\n        total += matrix[i][0] + matrix[i][-1]\n\nprint(total)\n'

def g7743(r):
    m, n = r.randint(2, 15), r.randint(2, 15)
    return f"{m} {n}\n" + "\n".join(" ".join(str(r.randint(-50, 50)) for _ in range(n)) for _ in range(m)) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g7743(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases

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
