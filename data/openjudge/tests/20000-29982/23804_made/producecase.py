import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23804/\n# Accepted submission: 52740130\n# Source: http://cs101.openjudge.cn/practice/solution/52740130/\n# License: not declared on the submission page; no license is inferred.\n\nn, m = map(int, input().split())\nans = input().split()\nfor _ in range(m):\n    stu = input().split()\n    cnt = 0\n    for a, s in zip(ans, stu):\n        if a == s:\n            cnt += 1\n    print(cnt)'
SAMPLE='4 2\nA B C D\nA C B D\nD A B B\n'
GENERATOR_NAME='g23804'
def g23804(r):
    n,m=r.randint(2,15),r.randint(1,8); ans=[r.choice("ABCD") for _ in range(n)]
    rows=[" ".join(r.choice("ABCD") for _ in range(n)) for _ in range(m)]
    return f"{n} {m}\n"+" ".join(ans)+"\n"+"\n".join(rows)+"\n"

def valid(text):
    """题面：第一行 n m（1<=n<=1000，1<=m<=1000）；第二行 n 个 A/B/C/D；其后 m 行，每行 n 个 A/B/C/D，空格分隔。"""
    import re
    lines=text.split('\n')
    if lines and lines[-1]=='': lines.pop()
    if not lines: return False
    t=lines[0].split()
    if len(t)!=2 or not all(re.fullmatch(r'[0-9]+',v) for v in t): return False
    n,m=map(int,t)
    if not (1<=n<=1000 and 1<=m<=1000) or len(lines)!=m+2: return False
    for l in lines[1:]:
        t=l.split()
        if len(t)!=n or any(v not in ('A','B','C','D') for v in t): return False
    return True

def g_sized(r,n,m,mode='rand'):
    ans=[r.choice("ABCD") for _ in range(n)]
    rows=[]
    for j in range(m):
        if mode=='allright' or (mode=='mixed' and j%3==0): row=list(ans)
        elif mode=='allwrong' or (mode=='mixed' and j%3==1): row=[r.choice([c for c in "ABCD" if c!=x]) for x in ans]
        else: row=[r.choice("ABCD") for _ in range(n)]
        rows.append(" ".join(row))
    return f"{n} {m}\n"+" ".join(ans)+"\n"+"\n".join(rows)+"\n"

def build_cases():
    cases=[SAMPLE]+[g23804(random.Random(s)) for s in range(1,25)]
    # 边界与规模：n、m 取 1；全对/全错；n=1000 满规模（n=m=1000 输入约 2MB，超出单组 1MB，取 1000x500 与 500x1000）
    spec=[(1,1,'rand'),(1,1,'allwrong'),(1,7,'mixed'),(7,1,'allright'),(1000,1,'mixed'),(1,1000,'mixed'),
          (20,20,'allright'),(20,20,'allwrong'),(300,300,'mixed'),(1000,100,'rand'),(100,1000,'mixed'),
          (999,200,'mixed'),(1000,500,'mixed'),(500,1000,'rand'),(1000,500,'rand')]
    cases+=[g_sized(random.Random(23804*100+i),n,m,mode) for i,(n,m,mode) in enumerate(spec)]
    return cases

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=build_cases()
    assert len(cases)==40 and len(set(cases))==40 and all(valid(c) for c in cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
