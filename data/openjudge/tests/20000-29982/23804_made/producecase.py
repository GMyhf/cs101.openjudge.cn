import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23804/\n# Accepted submission: 52740130\n# Source: http://cs101.openjudge.cn/practice/solution/52740130/\n# License: not declared on the submission page; no license is inferred.\n\nn, m = map(int, input().split())\nans = input().split()\nfor _ in range(m):\n    stu = input().split()\n    cnt = 0\n    for a, s in zip(ans, stu):\n        if a == s:\n            cnt += 1\n    print(cnt)'
SAMPLE='4 2\nA B C D\nA C B D\nD A B B\n'
GENERATOR_NAME='g23804'
def g23804(r):
    n,m=r.randint(2,15),r.randint(1,8); ans=[r.choice("ABCD") for _ in range(n)]
    rows=[" ".join(r.choice("ABCD") for _ in range(n)) for _ in range(m)]
    return f"{n} {m}\n"+" ".join(ans)+"\n"+"\n".join(rows)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
