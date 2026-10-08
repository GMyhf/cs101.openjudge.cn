import random
REFERENCE='# External reference: /practice/30041/statistics/\n# Accepted submission: 52212520\n# Source: http://cs101.openjudge.cn/practice/solution/52212520/\n# License: not declared on the submission page; no license is inferred.\n\nn,m=[int(i) for i in input().split()]\nprev_array=[int(i) for i in input().split()]\nnow_array=prev_array\n\ndp=[[0 for i in range(m)] for j in range(n)]\nfor i in range(m):\n    dp[0][i]=1\nfor i in range(1,n):\n    ptr1=0\n    current=0\n    prev_array=now_array[:]\n    now_array=[int(i) for i in input().split()]\n    for ptr2 in range(m):\n        while ptr1<=m-1 and now_array[ptr2]>=prev_array[ptr1]:\n            current+=dp[i-1][ptr1]\n            ptr1+=1\n        dp[i][ptr2]=current\ns=0\nfor i in dp[-1]:\n    s+=i\nprint(s)'
SAMPLE='3 3\n1 2 3\n2 3 4\n3 4 4\n'
GENERATOR_NAME='g30041'
import re as _re

def valid(text):
    """题面：第一行 n,m∈[1,1000]；接下来 n 行每行 m 个整数，每行已排序（不降）。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if not _re.fullmatch(r'[1-9]\d* [1-9]\d*', lines[0]):
        return False
    n, m = map(int, lines[0].split())
    if not (1 <= n <= 1000 and 1 <= m <= 1000) or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        toks = line.split(' ')
        if len(toks) != m or not all(_re.fullmatch(r'-?(0|[1-9]\d*)', t) and t != '-0' for t in toks):
            return False
        row = list(map(int, toks))
        if any(row[i] > row[i + 1] for i in range(m - 1)):
            return False
    return True

def _fmt(rows):
    return f"{len(rows)} {len(rows[0])}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"

def _rand(r, n, m, lo, hi):
    return [sorted(r.randint(lo, hi) for _ in range(m)) for _ in range(n)]

def _drift(r, n, m, width, step):
    """每行取值窗口随行号缓慢上移，答案非零且很大。"""
    rows = []
    base = 0
    for _ in range(n):
        rows.append(sorted(r.randint(base, base + width) for _ in range(m)))
        base += r.randint(0, step)
    return rows

def g30041(r):
    # 旧版生成器：n,m ≤ 35、值域 [0,100]；新数据见 build_cases()
    n, m = r.randint(1, 35), r.randint(1, 35); rows = []
    for _ in range(n):
        row = sorted(r.randint(0, 100) for _ in range(m)); rows.append(" ".join(map(str, row)))
    return f"{n} {m}\n" + "\n".join(rows) + "\n"

def build_cases():
    r = random.Random(30041)
    cases = [SAMPLE]
    cases.append('1 1\n5\n')                                         # 最小规模 → 1
    cases.append('1 7\n1 1 2 3 5 8 13\n')                            # n=1 → m
    cases.append('5 1\n1\n2\n2\n3\n10\n')                            # m=1 不降 → 1
    cases.append('4 1\n1\n2\n0\n3\n')                                # m=1 断开 → 0
    cases.append('3 3\n7 8 9\n4 5 6\n1 2 3\n')                       # 递减 → 0
    cases.append('3 4\n2 2 2 2\n2 2 2 2\n2 2 2 2\n')                 # 全相等 → m^n
    cases.append('3 3\n-5 0 5\n-5 -5 0\n-1 0 0\n')                   # 负数
    # 小规模随机（便于暴力核对）
    for t in range(8):
        n, m = r.randint(1, 6), r.randint(1, 6)
        cases.append(_fmt(_rand(r, n, m, -5, 10)))
    # 中等随机
    for t in range(6):
        n, m = r.randint(20, 120), r.randint(20, 120)
        cases.append(_fmt(_drift(r, n, m, r.randint(5, 200), r.randint(0, 10)) if t % 2 else _rand(r, n, m, 0, 1000)))
    # 大规模（.in ≤ 1MB）
    cases.append(_fmt([[0] * 250 for _ in range(1000)]))              # 全相等 → 250^1000，大整数
    cases.append(_fmt(_drift(r, 1000, 250, 60, 1)))                    # n=1000
    cases.append(_fmt(_drift(r, 250, 1000, 90, 2)))                    # m=1000
    cases.append(_fmt(_drift(r, 500, 500, 99, 0)))                     # n=m=500，卡 O(n m^2)
    cases.append(_fmt(_rand(r, 250, 250, 0, 99)))
    cases.append(_fmt(_rand(r, 1000, 1, -10 ** 9, 10 ** 9)))           # m=1 大值域
    cases.append(_fmt(sorted([x] for x in r.sample(range(-10 ** 9, 10 ** 9), 1000))))  # m=1 严格递增 → 1
    cases.append(_fmt(_rand(r, 1, 1000, -10 ** 9, 10 ** 9)))           # n=1 → 1000
    cases.append(_fmt(_rand(r, 90, 1000, -10 ** 9, 10 ** 9)))          # 大值域
    rows = _drift(r, 300, 200, 50, 1); rows[150] = [-1] * 200          # 中间一行全部偏小 → 0
    cases.append(_fmt(rows))
    rows = _drift(r, 300, 200, 50, 1); rows[-1] = [rows[-2][0]] * 200   # 末行只与上一行最小值相等
    cases.append(_fmt(rows))
    for t in range(7):
        n = r.choice([300, 400, 500, 700, 1000]); m = min(1000, (250000 if t == 0 else 60000) // n)   # 体积控制：只留 1 组满 25 万格
        cases.append(_fmt(_drift(r, n, m, r.randint(10, 99), r.randint(0, 2))))
    assert len(cases) == 40, len(cases)   # catalog.json 登记了 0..39 共 40 组
    return cases

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert all(valid(c) for c in cases)
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
