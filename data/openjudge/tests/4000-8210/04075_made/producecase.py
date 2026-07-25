"""4075 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4075
SAMPLE_IN = '1\n2\n1 2\n3 4\n'
SAMPLE_OUT = '3 1\n4 2\n'
REFERENCE_SOURCE = 'def rotate_matrix_90(matrix):\n    n = len(matrix)\n    return [[matrix[n - j - 1][i] for j in range(n)] for i in range(n)]\n\ndef print_matrix(matrix):\n    for row in matrix:\n        print(\' \'.join(map(str, row)))\n\ndef main():\n    M = int(input())\n    results = []\n    for _ in range(M):\n        n = int(input())\n        matrix = [list(map(int, input().split())) for _ in range(n)]\n        rotated = rotate_matrix_90(matrix)\n        results.append(rotated)\n    \n    for result in results:\n        print_matrix(result)\n\nif __name__ == "__main__":\n    main()\n\n'

def g4075(r):
    cases = r.randint(1, 4); lines = [str(cases)]
    for _ in range(cases):
        n = r.randint(1, 8); lines.append(str(n))
        lines += [" ".join(str(r.randint(-9, 9)) for _ in range(n)) for _ in range(n)]
    return "\n".join(lines) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4075(random.Random(NUMBER + i)) for i in range(1, 20)]

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
