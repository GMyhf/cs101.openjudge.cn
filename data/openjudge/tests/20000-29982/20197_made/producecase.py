import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/20197/\n# Accepted submission: 52540070\n# Source: http://cs101.openjudge.cn/practice/solution/52540070/\n# License: not declared on the submission page; no license is inferred.\n\nn,m=map(int,input().split())\ncnt=0\nwhile m!=n:\n    m,n=min(m,n),max(m,n)-min(m,n)\n    cnt+=1\ncnt+=1\nprint(cnt)'
SAMPLE='5 3\n'
GENERATOR_NAME='g20197'
def g20197(r):
    return f"{r.randint(1, 3000)} {r.randint(1, 3000)}\n"

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
