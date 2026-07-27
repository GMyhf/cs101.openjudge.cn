import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19984 statistics, Accepted solution 22475453.\n# Source: http://cs101.openjudge.cn/practice/solution/22475453/\n# Statistics: http://cs101.openjudge.cn/practice/19984/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nf=[-1]*(n+1)\np=[]\nf[0]=float(input())\nfor i in range(n):\n    p.append(tuple(map(float,input().split())))\nf[1]=(2*f[0]+100)/p[0][0]\nb=[0]*n\nfor i in range(1,n):\n    for j in range(i+1):\n        if p[i][j]==0:\n            continue\n        if f[i+1]==-1:\n            f[i+1]=(f[i]+f[j]+100-(1-p[i][j])*f[i-1])/p[i][j]\n            b[i]=j\n        elif f[i+1]>(f[i]+f[j]+100-(1-p[i][j])*f[i-1])/p[i][j]:\n            f[i+1]=(f[i]+f[j]+100-(1-p[i][j])*f[i-1])/p[i][j]\n            b[i]=j\nprint(\' \'.join(map(str,b)))\nprint("%.2f" % f[n])\n'
SAMPLE='2\n100\n1\n0.8 0.95\n'
GENERATOR_NAME='g19984'
def g19984(r):
    n = r.randint(2, 8)
    rows = []
    for i in range(n):
        rows.append(" ".join(f"{r.uniform(.15, .95):.4f}" for _ in range(i + 1)))
    return f"{n}\n{r.randint(50, 500)}\n" + "\n".join(rows) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
