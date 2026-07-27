import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/21532/\n# Accepted submission: 52201278\n# Source: http://cs101.openjudge.cn/practice/solution/52201278/\n# License: not declared on the submission page; no license is inferred.\n\nn=int(input())\ni=6\nwhile n%i!=0:\n    i+=1\nprint(n//i)'
SAMPLE='231\n'
GENERATOR_NAME='g21532'
def g21532(r):
    a, b = r.sample(range(1, 2000), 2)
    c = r.randint(1, 10 ** 6)
    return f"{a + b + c}\n"

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
