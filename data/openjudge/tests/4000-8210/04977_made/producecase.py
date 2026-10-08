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

def valid(text):
    """题面契约：首行 K（K<100）；每组两行：N（N<100），随后 N 个互不相同的整数 h（0<h<10000）。"""
    lines = text.split("\n")
    while lines and lines[-1].strip() == "":
        lines.pop()
    try:
        h = lines[0].split()
        if len(h) != 1:
            return False
        k = int(h[0])
        if not 1 <= k < 100 or len(lines) != 1 + 2 * k:
            return False
        for g in range(k):
            a = lines[1 + 2 * g].split()
            if len(a) != 1:
                return False
            n = int(a[0])
            v = [int(x) for x in lines[2 + 2 * g].split()]
            if not 1 <= n < 100 or len(v) != n or len(set(v)) != n:
                return False
            if not all(0 < x < 10000 for x in v):
                return False
    except (ValueError, IndexError):
        return False
    return True


def _seq(r, n, kind):
    v = r.sample(range(1, 10000), n)
    if kind == "inc":
        v.sort()
    elif kind == "dec":
        v.sort(reverse=True)
    elif kind == "zigzag":    # 交错，答案很小
        v.sort()
        lo, hi = v[: n // 2], v[n // 2:]
        v = [x for pair in zip(hi, lo) for x in pair] + (hi[len(lo):] if len(hi) > len(lo) else [])
    elif kind == "valley":    # 先降后升：两个方向各占一半
        v.sort()
        left = sorted(v[0::2], reverse=True); right = sorted(v[1::2])
        v = left + right
    elif kind == "nearinc":   # 大体递增，少量扰动
        v.sort()
        for _ in range(max(1, n // 10)):
            i, j = r.randrange(n), r.randrange(n); v[i], v[j] = v[j], v[i]
    elif kind == "edge":      # 用上 1 与 9999
        v = r.sample(range(2, 9999), max(0, n - 2)) + [1, 9999][: n]
        r.shuffle(v)
    return v


# (K, N 范围, 类型)
PLAN = [
    (1, (1, 1), "rand"), (3, (1, 2), "rand"), (5, (2, 8), "rand"), (5, (5, 20), "inc"),
    (5, (5, 20), "dec"), (6, (10, 30), "zigzag"), (6, (10, 30), "valley"), (8, (20, 60), "rand"),
    (8, (20, 60), "nearinc"), (10, (1, 99), "rand"), (10, (99, 99), "rand"), (5, (99, 99), "inc"),
    (5, (99, 99), "dec"), (99, (99, 99), "rand"), (99, (1, 99), "rand"), (99, (90, 99), "nearinc"),
    (99, (99, 99), "valley"), (50, (1, 99), "edge"), (99, (99, 99), "zigzag"),
]


def g4977(r, plan):
    k, (lo, hi), kind = plan
    cases = []
    for _ in range(k):
        n = r.randint(lo, hi)
        cases += [str(n), " ".join(map(str, _seq(r, n, kind)))]
    return str(k) + "\n" + "\n".join(cases) + "\n"


def build_cases():
    return [SAMPLE_IN] + [g4977(random.Random(NUMBER + i), PLAN[i - 1]) for i in range(1, 20)]


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
    assert all(valid(c) for c in cases)
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
