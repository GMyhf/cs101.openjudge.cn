"""3441 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 3441
SAMPLE_IN = '6\n-45 22 42 -16\n-41 -27 56 30\n-36 53 -37 77\n-36 30 -75 -46\n26 -38 -10 62\n-32 -54 -6 45\n'
SAMPLE_OUT = '5\n'
REFERENCE_SOURCE = "# https://docs.python.org/3/library/array.html\nimport array as arr\n\nn = int(input())\na = arr.array('i', [0]*(n+1))\nb = arr.array('i', [0]*(n+1))\nc = arr.array('i', [0]*(n+1))\nd = arr.array('i', [0]*(n+1))\n\nfor i in range(n):\n    a[i],b[i],c[i],d[i] = map(int, input().split())\n\n\ndict1 = {}\nfor i in range(n):\n    for j in range(n):\n        if not a[i]+b[j] in dict1:\n            dict1[a[i] + b[j]] = 0\n        dict1[a[i] + b[j]] += 1\n\nans = 0\nfor i in range(n):\n    for j in range(n):\n        if -(c[i]+d[j]) in dict1:\n            ans += dict1[-(c[i]+d[j])]\n\nprint(ans)\n"

def g3441(r):
    n = r.choice([2, 4, 8, 12]); rows = [[r.randint(-20, 20) for _ in range(4)] for _ in range(n)]
    return str(n) + "\n" + "\n".join(" ".join(map(str, x)) for x in rows) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g3441(random.Random(NUMBER + i)) for i in range(1, 20)]

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
