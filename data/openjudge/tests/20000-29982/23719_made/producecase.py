import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/23719/\n# Accepted submission: 52527361\n# Source: http://cs101.openjudge.cn/practice/solution/52527361/\n# License: not declared on the submission page; no license is inferred.\n\na,b=map(float,input().split())\nprint(f'{a*b/666.667:.4f}')"
SAMPLE='126.35 300.72\n'
GENERATOR_NAME='g23719'
def g23719(r): return f"{r.uniform(.1,1000):.5f} {r.uniform(.1,1000):.5f}\n"

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
