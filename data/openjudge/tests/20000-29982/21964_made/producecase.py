import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/21964/\n# Accepted submission: 52244442\n# Source: http://cs101.openjudge.cn/practice/solution/52244442/\n# License: not declared on the submission page; no license is inferred.\n\nn,m=map(int,input().split())\nneed=[]\nvalue=[]\nfor i in range(n):\n    a,b=map(int,input().split())\n    need.append(a)\n    value.append(b)\ndp=[0]*(m+1)\nfor i in range(n):\n    w=need[i]\n    for j in range(m,w-1,-1):\n        dp[j]=max(dp[j],dp[j-w]+value[i])\nprint(dp[m])'
SAMPLE='5 1000\n144 990\n487 436\n210 673\n567 58\n1056 897\n'
GENERATOR_NAME='g21964'
def g21964(r):
    n, m = r.randint(1, 30), r.randint(20, 1000)
    return f"{n} {m}\n" + "\n".join(f"{r.randint(1, min(200000, m))} {r.randint(0, 1000)}" for _ in range(n)) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
