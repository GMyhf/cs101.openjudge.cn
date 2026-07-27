import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/21516/\n# Accepted submission: 47436368\n# Source: http://cs101.openjudge.cn/practice/solution/47436368/\n# License: not declared on the submission page; no license is inferred.\n\na,b=map(int,input().split());c={i:[]for i in range(a+1)};f={i:0 for i in c};import sys;sys.setrecursionlimit(1<<30)\nfor i in range(b):d,e=map(int,input().split());c[d].append(e)\ndef r(z):\n    global f\n    if f[z]:x={p,f[z]};return x\n    else:f[z]=p;x={p}\n    for k in c[z]:x|=r(k)\n    return x\ndef s(z):global f;a=z if z==f[z]else s(f[z]);f[z]=a;return a\nfor i in c:\n    if 1<len(c[i])and f[i]==0:\n        g=set();p=min(c[i])\n        for j in c[i]:g|=r(j)\n        h=min(s(z)for z in g)\n        for j in g:f[j]=h\nk={i:0 for i in c};g=0\nfor i in c:\n    if f[i]:k[s(i)]+=1\n    else:g+=len(c[i])\nprint(g+sum((k[i]-1)*k[i]for i in k))'
SAMPLE='5 4\n1 2\n1 3\n4 3\n4 5\n'
GENERATOR_NAME='g21516'
def g21516(r):
    n = r.randint(2, 18)
    edges = [(a, b) for a in range(1, n + 1) for b in range(a + 1, n + 1) if r.random() < .18]
    if not edges:
        edges = [(1, 2)]
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges) + "\n"

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
