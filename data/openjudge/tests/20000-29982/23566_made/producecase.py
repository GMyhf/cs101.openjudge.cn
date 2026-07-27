import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23566/\n# Accepted submission: 52178654\n# Source: http://cs101.openjudge.cn/practice/solution/52178654/\n# License: not declared on the submission page; no license is inferred.\n\nn,m=map(int,input().split())\nlis=[0 for i in range(m)]\ntotal=0\nfor i in range(n):\n    x,y=map(int,input().split())\n    lis[x-1]+=y\ntotal=sum(lis)\ntotal-=(total//200)*30\nfor i in range(m):\n    s=input()\n    ptr=0\n    while "0"<=s[ptr]<="9":\n        ptr+=1\n    if lis[i]>=int(s[0:ptr]):\n        total-=int(s[ptr+1:len(s)])\nprint(total)'
SAMPLE='2 2\n1 100\n2 100\n100-20\n200-50\n'
GENERATOR_NAME='g23566'
def g23566(r):
    n,m=r.randint(2,20),r.randint(2,8); items=[(r.randint(1,m),r.randint(1,300)) for _ in range(n)]
    coupons=[(q,r.randint(1,q)) for q in [r.randint(1,1000) for _ in range(m)]]
    return f"{n} {m}\n"+"\n".join(f"{a} {b}" for a,b in items)+"\n"+"\n".join(f"{a}-{b}" for a,b in coupons)+"\n"

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
