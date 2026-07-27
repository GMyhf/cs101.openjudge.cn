import random
REFERENCE='# External reference: /practice/30086/statistics/\n# Accepted submission: 52211740\n# Source: http://cs101.openjudge.cn/practice/solution/52211740/\n# License: not declared on the submission page; no license is inferred.\n\nn,d=[int(i) for i in input().split()]\nl=[int(i) for i in input().split()]\nl.sort()\nstatus="Yes"\nfor i in range(n):\n    a=l[2*i]\n    b=l[2*i+1]\n    if abs(a-b)>d:\n        status="No"\n        break\nprint(status)'
SAMPLE='6 4\n22 15 32 36 16 30 42 30 39 23 17 18\n'
GENERATOR_NAME='g30086'
CPP=False
def g30086(r):
    n, d = r.randint(1, 30), r.randint(0, 20)
    a = [r.randint(0, 100) for _ in range(2*n)]
    return f"{n} {d}\n{' '.join(map(str,a))}\n"

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
