"""4145 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4145
SAMPLE_IN = '3 1\n5 0 2\n5 1 6\n4 2\n1 2 7 9\n5 6 7 9\n0 0\n'
SAMPLE_OUT = '83\n100\n'
REFERENCE_SOURCE = "# 蒋子轩23工学院\ndef can_achieve(target,a,b,k):\n    diffs=[a[i]-target*b[i] for i in range(len(a))]\n    diffs.sort()\n    #放弃k场考试后可以达到target\n    return sum(diffs[k:])>=0\ndef max_avg_score(k,a,b):\n    l,r=0,100\n    while r-l>1e-5:\n    \t#非整数二分\n        m=(l+r)/2\n        if can_achieve(m,a,b,k):\n            l=m\n        else:\n            r=m\n    return m*100\nwhile True:\n    n,k=map(int,input().split())\n    if n==0 and k==0:\n        break\n    a = list(map(int, input().split()))\n    b = list(map(int, input().split()))\n    print(f'{max_avg_score(k,a,b):.0f}')\n"

def g4145(r):
    parts = []
    for _ in range(r.randint(1, 3)):
        n = r.randint(2, 20); k = r.randint(1, n - 1)
        a = [r.randint(1, 1_000_000_000) for _ in range(n)]
        b = [x + r.randint(0, 1_000_000_000 - x) for x in a]
        parts.append(f"{n} {k}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)))
    return "\n".join(parts) + "\n0 0\n"

def build_cases():
    return [SAMPLE_IN] + [g4145(random.Random(NUMBER + i)) for i in range(1, 20)]

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
