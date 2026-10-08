import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/20197/\n# Accepted submission: 52540070\n# Source: http://cs101.openjudge.cn/practice/solution/52540070/\n# License: not declared on the submission page; no license is inferred.\n\nn,m=map(int,input().split())\ncnt=0\nwhile m!=n:\n    m,n=min(m,n),max(m,n)-min(m,n)\n    cnt+=1\ncnt+=1\nprint(cnt)'
SAMPLE='5 3\n'
GENERATOR_NAME='g20197'

# 题面：一行两个整数 N M，1 <= N, M <= 3000。


def valid(text):
    import re
    m = re.fullmatch(r"([1-9]\d*) ([1-9]\d*)\n", text)
    return bool(m) and all(1 <= int(v) <= 3000 for v in m.groups())


# 边界：1×1、N==M（答案 1）、1×3000 / 3000×1（答案 3000，步数最多）、3000×3000、
# 相邻 Fibonacci 数（商全为 1、辗转次数最多）、互素的相邻数、整除关系
_SPECIAL = [(1, 1), (3000, 3000), (1, 3000), (3000, 1), (1597, 2584), (2584, 1597), (2999, 3000),
            (3000, 2999), (1500, 3000), (2, 3000), (2999, 2), (1777, 1777), (987, 1597), (1, 2), (2, 1)]


def g20197(r, s):
    if s <= len(_SPECIAL):
        return "%d %d\n" % _SPECIAL[s - 1]
    if s % 4 == 0:     # 一边很小、另一边很大
        a, b = r.randint(1, 30), r.randint(2000, 3000)
        if r.random() < .5:
            a, b = b, a
        return f"{a} {b}\n"
    return f"{r.randint(1, 3000)} {r.randint(1, 3000)}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[g20197(random.Random(s), s) for s in range(1, 40)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
