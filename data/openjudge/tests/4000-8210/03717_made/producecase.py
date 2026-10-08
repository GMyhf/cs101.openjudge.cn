"""3717 移动路线 测试数据生成器：固定种子，重跑可逐字节复现 data/。

题面约束：一行两个整数 m n（0<m+n<=20），m、n 是方格矩阵的行数和列数，故 m,n>=1。

2026-10 审计修正：原 39 组随机数据里没有 1 1（原地不动、答案 1），也没有答案最大的
10 10（48620）/ 9 11 / 11 9。现在固定加入这些边界，其余仍按固定种子随机补足 40 组。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

REFERENCE_SOURCE = 'import sys\nm,n=map(int,sys.stdin.read().split()); dp=[1]*n\nfor _ in range(m-1):\n    for j in range(1,n): dp[j]+=dp[j-1]\nprint(dp[n-1])'
SAMPLE_IN = '2 3\n'
SAMPLE_OUT = '3\n'


def valid(text):
    if not re.fullmatch(r"(\d+) (\d+)\n", text):
        return False
    m, n = map(int, text.split())
    return m >= 1 and n >= 1 and 0 < m + n <= 20 and text == f"{m} {n}\n"


def g3717(r):
    m = r.randint(1, 19)
    n = r.randint(1, 20 - m)
    return f"{m} {n}\n"


def build_cases():
    cases = [SAMPLE_IN]
    for m, n in [(1, 1), (10, 10), (9, 11), (11, 9), (1, 19), (19, 1), (1, 2), (2, 1), (3, 2), (8, 12)]:
        cases.append(f"{m} {n}\n")
    index = 0
    while len(cases) < 40:
        index += 1
        c = g3717(random.Random(3717 + index))
        if c not in cases:
            cases.append(c)
    return cases


def main():
    cases = build_cases()
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        for index, content in enumerate(cases):
            result = subprocess.run(["python3", handle.name], input=content, text=True,
                                    capture_output=True, timeout=10, check=True)
            if index == 0:
                assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
