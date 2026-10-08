import random
REFERENCE='# External reference: /practice/29853/statistics/\n# Accepted submission: 52288129\n# Source: http://cs101.openjudge.cn/practice/solution/52288129/\n# License: not declared on the submission page; no license is inferred.\n\nn=int(input())\na=[int(i) for i in input().split()]\nb=[int(i) for i in input().split()]\nminb=min(b)\nmaxb=max(b)\ncalc=[max(abs(minb-i),abs(maxb-i)) for i in a]\nprint(min(calc))'
SAMPLE='2\n1 10\n2 20\n'
GENERATOR_NAME='g29853'
def g29853(r):
    # 题面：1<=N<=1000，1<=Ai<=10^3，1<=Bi<=10^3。
    n = r.randint(1, 100); a = [r.randint(1, 1000) for _ in range(n)]; b = [r.randint(1, 1000) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

from pathlib import Path
import random, subprocess, sys, tempfile


def valid(text):
    """题面契约：第一行 N（1<=N<=1000）；第二行恰 N 个 Ai，第三行恰 N 个 Bi，1<=Ai,Bi<=10^3。"""
    if not text.endswith("\n"):
        return False
    rows = text[:-1].split("\n")
    if len(rows) != 3:
        return False
    try:
        if rows[0] != rows[0].strip():
            return False
        n = int(rows[0])
        a = [int(x) for x in rows[1].split(" ")]
        b = [int(x) for x in rows[2].split(" ")]
    except ValueError:
        return False
    if not 1 <= n <= 1000 or len(a) != n or len(b) != n:
        return False
    return all(1 <= x <= 1000 for x in a + b)


def fmt(a, b):
    return f"{len(a)}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"


def extra_cases():
    """追加：N=1 边界、值域两端、全相等（答案 0）、N=1000 满规模；
    以及 B 只取两端、A 集中在中点附近的组，卡「只看 A 的中位数/平均数」之类的写法。"""
    r = random.Random(298530)
    out = [fmt([1], [1000]), fmt([7], [7]), fmt([1000], [1]),
           fmt([5, 5], [5, 5]), fmt([1, 1000], [1, 1000])]
    out.append(fmt([r.randint(1, 1000) for _ in range(1000)], [r.randint(1, 1000) for _ in range(1000)]))
    out.append(fmt([1000] * 1000, [1] * 1000))
    out.append(fmt([500] * 1000, [500] * 1000))
    out.append(fmt([r.randint(1, 1000) for _ in range(1000)], [r.choice([1, 1000]) for _ in range(1000)]))
    out.append(fmt([r.randint(400, 600) for _ in range(1000)], [r.randint(300, 700) for _ in range(1000)]))
    out.append(fmt([r.choice([1, 1000]) for _ in range(1000)], [r.randint(1, 1000) for _ in range(1000)]))
    out.append(fmt([r.randint(1, 1000) for _ in range(999)], [r.randint(450, 550) for _ in range(999)]))
    return out


def brute(text):
    """独立 oracle：按回合做极小极大搜索（仅小 N），小蓝先删，交替到各剩一道。"""
    from functools import lru_cache
    rows = text.split("\n")
    a = tuple(sorted(map(int, rows[1].split())))
    b = tuple(sorted(map(int, rows[2].split())))

    @lru_cache(None)
    def go(a, b, turn):
        if len(a) == 1 and len(b) == 1:
            return abs(a[0] - b[0])
        if turn == 0:
            return min(go(a[:i] + a[i + 1:], b, 1) for i in range(len(a)))
        return max(go(a, b[:i] + b[i + 1:], 0) for i in range(len(b)))
    return go(a, b, 0)
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=extra_cases()
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
