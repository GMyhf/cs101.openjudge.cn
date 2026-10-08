"""4075 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 21 组数据。

2026-10 审计：原数据 M<=4、n<=8，离题面 M<=100、n<=100 太远，也没有 M=1/n=1 以外的边界组合。
现第 1..9 组保留原随机小组，其余换成边界与大规模组（M=100、n=100，单组 .in 控制在 1MB 内）。

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

def valid(text):
    """题面：第一行 M（1<=M<=100）；每个矩阵先一行 n（1<=n<=100），再 n 行、每行 n 个整数（空格分隔）。
    题面未给元素取值范围，只核为整数。"""
    try:
        lines = text.split("\n")
        while lines and lines[-1].strip() == "":
            lines.pop()
        rows = [ln.split() for ln in lines]
        if not rows or len(rows[0]) != 1:
            return False
        M = int(rows[0][0])
        if not 1 <= M <= 100:
            return False
        p = 1
        for _ in range(M):
            if p >= len(rows) or len(rows[p]) != 1:
                return False
            n = int(rows[p][0]); p += 1
            if not 1 <= n <= 100 or p + n > len(rows):
                return False
            for q in range(p, p + n):
                if len(rows[q]) != n:
                    return False
                for tok in rows[q]:
                    int(tok)
            p += n
        return p == len(rows)
    except ValueError:
        return False


def fmt(mats):
    lines = [str(len(mats))]
    for mat in mats:
        lines.append(str(len(mat)))
        lines += [" ".join(map(str, row)) for row in mat]
    return "\n".join(lines) + "\n"


def rmat(r, n, lo, hi):
    return [[r.randint(lo, hi) for _ in range(n)] for _ in range(n)]


def g4075(r):
    cases = r.randint(1, 4); lines = [str(cases)]
    for _ in range(cases):
        n = r.randint(1, 8); lines.append(str(n))
        lines += [" ".join(str(r.randint(-9, 9)) for _ in range(n)) for _ in range(n)]
    return "\n".join(lines) + "\n"

def build_cases():
    cases = [SAMPLE_IN] + [g4075(random.Random(NUMBER + i)) for i in range(1, 10)]
    r = random.Random(NUMBER * 7)
    cases.append(fmt([[[r.randint(-10 ** 9, 10 ** 9)]]]))                      # M=1, n=1
    cases.append(fmt([[[r.randint(0, 9)]] for _ in range(100)]))               # M=100, 全是 1x1
    cases.append(fmt([rmat(r, 100, 0, 9)]))                                     # 单个 100x100
    cases.append(fmt([rmat(r, 100, -10 ** 9, 10 ** 9)]))                        # 大数、负数
    cases.append(fmt([[[i * 100 + j for j in range(100)] for i in range(100)]]))  # 可辨认的位置，查转置/逆时针
    cases.append(fmt([rmat(r, r.randint(1, 30), -99, 99) for _ in range(100)]))  # M=100, n 混合
    cases.append(fmt([rmat(r, n, 0, 9) for n in range(1, 61)]))                 # n 从 1 到 60
    cases.append(fmt([rmat(r, 100, 0, 9) for _ in range(2)] + [rmat(r, 2, 0, 9)]))
    cases.append(fmt([rmat(r, 2, 1, 4), rmat(r, 3, 1, 9), rmat(r, 1, 5, 5), rmat(r, 4, -5, 5)]))
    cases.append(fmt([rmat(r, n, 0, 9) for n in (100, 1, 99, 2, 98)]))
    cases.append(fmt([rmat(r, 100, 0, 9) for _ in range(50)]))                 # 接近 1MB 的最大组
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
    assert len(set(cases)) == len(cases), "组间不得重复"
    for i, c in enumerate(cases):
        assert valid(c), f"第 {i} 组越出题面约束"
        assert len(c.encode()) <= 1 << 20, f"第 {i} 组 .in 超过 1MB"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
