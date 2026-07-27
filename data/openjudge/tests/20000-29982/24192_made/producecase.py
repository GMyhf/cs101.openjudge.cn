import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/24192/\n# Accepted submission: 52740123\n# Source: http://cs101.openjudge.cn/practice/solution/52740123/\n# License: not declared on the submission page; no license is inferred.\n\nn, m = map(int, input().split())\ntotal = n * m\nans = (total + 1) // 2\nprint(ans)'
SAMPLE='5 7\n'
GENERATOR_NAME='g24192'
def g24192(r): return f"{r.randint(1,1000000)} {r.randint(1,1000000)}\n"

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
