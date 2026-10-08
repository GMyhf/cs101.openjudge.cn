"""7743 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 33 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import re
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

_INT = re.compile(r"-?(0|[1-9][0-9]*)")


def valid(text):
    """题面契约：首行 m n（m < 100，n < 100，行列数至少为 1），其后恰 m 行、每行 n 个整数，单空格分隔。
    题面未给元素取值范围，只核是整数。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    head = lines[0].split(" ")
    if len(head) != 2 or not all(re.fullmatch(r"[1-9][0-9]*", t) for t in head):
        return False
    m, n = map(int, head)
    if not (1 <= m < 100 and 1 <= n < 100) or len(lines) != m + 1:
        return False
    for line in lines[1:]:
        row = line.split(" ")
        if len(row) != n or not all(_INT.fullmatch(t) and t != "-0" for t in row):
            return False
    return True


def matrix_case(r, m, n, lo, hi):
    return f"{m} {n}\n" + "\n".join(" ".join(str(r.randint(lo, hi)) for _ in range(n)) for _ in range(m)) + "\n"


# 追加的边界/规模组：单行、单列、1x1、2xN、满规模 99x99（原 20 组最大只有 15x15，且没有单行单列）
EXTRA_SHAPES = [
    (1, 1, -1000, 1000), (1, 99, -1000, 1000), (99, 1, -1000, 1000), (1, 2, -50, 50), (2, 1, -50, 50),
    (2, 2, -50, 50), (2, 99, -1000, 1000), (99, 2, -1000, 1000), (3, 1, -50, 50), (1, 3, -50, 50),
    (99, 99, -1000000, 1000000), (99, 98, 0, 1000000), (98, 99, -1000000, 0),
]


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
    for j, (m, n, lo, hi) in enumerate(EXTRA_SHAPES):
        value = matrix_case(random.Random(NUMBER * 100 + j), m, n, lo, hi)
        assert value not in cases
        cases.append(value)
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
    assert all(valid(c) for c in cases), "有数据越出题面约束"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
