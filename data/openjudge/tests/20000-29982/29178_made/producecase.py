import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/29178/\n# Accepted submission: 52734219\n# Source: http://cs101.openjudge.cn/practice/solution/52734219/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\na = list(map(int, input().split()))\ncnt = 0\n\nfor i in range(n):\n    if i == 0:\n        # 第一个\n        if a[i] > a[i+1]:\n            cnt += 1\n    elif i == n-1:\n        # 最后一个\n        if a[i] > a[i-1]:\n            cnt += 1\n    else:\n        # 中间\n        if a[i] > a[i-1] and a[i] > a[i+1]:\n            cnt += 1\n\nprint(cnt)'
SAMPLE='5\n8 12 7 3 6\n'
EXTRA_CASE=None
GENERATOR_NAME='g29178'
import re
_INT = re.compile(r'-?(0|[1-9][0-9]*)$')

def valid(text):
    """题面：第一行 n（2 ≤ n ≤ 100），第二行 n 个整数（题面未给水位范围，只核整数）。"""
    if not text.endswith('\n'): return False
    L = text[:-1].split('\n')
    if len(L) != 2: return False
    h = L[0].split(' '); a = L[1].split(' ')
    if len(h) != 1 or not _INT.match(h[0]) or any(not _INT.match(x) for x in a): return False
    return 2 <= int(h[0]) <= 100 and len(a) == int(h[0])

def g29178(r):
    n = r.randint(2, 100); return f"{n}\n" + " ".join(str(r.randint(-1000, 1000)) for _ in range(n)) + "\n"

def _fmt(a):
    return f"{len(a)}\n" + " ".join(map(str, a)) + "\n"

def extra_cases():
    r = random.Random(291780)
    out = ['7\n8 2 3 1 1 2 1\n', '5\n1 2 3 3 2\n', '2\n1 2\n']   # 题面样例 2~4
    out += [_fmt([2, 1]), _fmt([5, 5]), _fmt([7] * 100)]
    out.append(_fmt(list(range(1, 101))))                          # 严格递增：仅最东端
    out.append(_fmt(list(range(100, 0, -1))))                      # 严格递减：仅最西端
    out.append(_fmt([1 if i % 2 == 0 else 0 for i in range(100)]))  # 锯齿：50 个波峰
    out.append(_fmt([0 if i % 2 == 0 else 1 for i in range(99)]))
    out.append(_fmt([3, 3, 1, 4, 4, 2, 5, 1, 1]))                  # 平台不算波峰
    for _ in range(6):                                             # 小值域，大量相等相邻
        n = r.randint(2, 100); out.append(_fmt([r.randint(0, 2) for _ in range(n)]))
    out.append(_fmt([r.choice([-10**9, 10**9, r.randint(-10**9, 10**9)]) for _ in range(100)]))
    out.append(_fmt([-5, -3, -4, -1, -2]))                         # 全负数
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path(__file__).parent/'data'; d.mkdir(exist_ok=True)
    cases=[SAMPLE]+([EXTRA_CASE] if EXTRA_CASE else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]
    for c in extra_cases():
        assert c not in cases, c
        cases.append(c)
    for c in cases: assert valid(c), c
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
