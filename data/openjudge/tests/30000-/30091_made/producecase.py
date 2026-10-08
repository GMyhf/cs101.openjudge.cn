import random
REFERENCE='# External reference: /practice/30091/statistics/\n# Accepted submission: 52732776\n# Source: http://cs101.openjudge.cn/practice/solution/52732776/\n# License: not declared on the submission page; no license is inferred.\n\nL = int(input())\nN = int(input())\nif N == 0:\n    print(0, 0)\nelse:\n    pos = list(map(int, input().split()))\n    min_ans = 0\n    max_ans = 0\n    for x in pos:\n        t1 = min(x, L + 1 - x)\n        t2 = max(x, L + 1 - x)\n        if t1 > min_ans:\n            min_ans = t1\n        if t2 > max_ans:\n            max_ans = t2\n    print(min_ans, max_ans)'
SAMPLE='4\n2\n1 3\n'
GENERATOR_NAME='g30091'
CPP=False
def valid(text):
    # 题面：第一行 L，第二行 N，第三行 N 个互异坐标；1<=L<=5000，0<=N<=5000，N<=L
    if not text.endswith('\n'): return False
    lines = text[:-1].split('\n')
    if len(lines) not in (2, 3): return False
    try:
        if lines[0].strip() != lines[0] or lines[1].strip() != lines[1]: return False
        L = int(lines[0]); n = int(lines[1])
    except ValueError: return False
    if not (1 <= L <= 5000 and 0 <= n <= 5000 and n <= L): return False
    if n == 0: return len(lines) == 2 or lines[2] == ''
    if len(lines) != 3: return False
    tok = lines[2].split(' ')
    if len(tok) != n: return False
    try: pos = [int(x) for x in tok]
    except ValueError: return False
    return all(1 <= x <= L for x in pos) and len(set(pos)) == n

def fmt(L, p):
    # N=0 时仍保留空的第三行，按行 input() 读三行的写法不会 EOFError
    return f"{L}\n{len(p)}\n{' '.join(map(str,p))}\n"

def g30091(r):
    L, n = r.randint(2, 5000), r.randint(0, 30)
    n = min(n, L)
    p = sorted(r.sample(range(1, L + 1), n)) if n else []
    return fmt(L, p)

def g30091_big(r, L, n, sort=False):
    p = r.sample(range(1, L + 1), n)
    if sort: p.sort()
    return fmt(L, p)

def extra_cases():
    r = random.Random(30091)
    out = []
    out.append(fmt(1, []))            # L=1, N=0
    out.append(fmt(1, [1]))           # L=1, N=1
    out.append(fmt(5000, []))         # N=0 大 L
    out.append(fmt(5000, list(range(1, 5001))))          # N=L=5000 满
    out.append(fmt(5000, list(range(5000, 0, -1))))      # 逆序满
    out.append(g30091_big(r, 5000, 5000))                # 乱序满
    out.append(g30091_big(r, 5000, 4999))
    out.append(g30091_big(r, 4999, 2500))
    out.append(fmt(5000, [2500]))     # 正中间偏左
    out.append(fmt(5000, [2501]))
    out.append(fmt(4999, [2500]))     # 奇数长度正中
    out.append(fmt(5000, [5000, 1]))  # 两端，乱序
    out.append(fmt(5000, [1]))
    out.append(fmt(5000, [5000]))
    out.append(fmt(2, [2, 1]))
    out.append(fmt(3, [2]))
    for _ in range(4):                # 乱序中等规模
        L = r.randint(1000, 5000); out.append(g30091_big(r, L, r.randint(1, min(L, 3000))))
    return out

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]+extra_cases()
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
