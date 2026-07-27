import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23654/\n# Accepted submission: 52485897\n# Source: http://cs101.openjudge.cn/practice/solution/52485897/\n# License: not declared on the submission page; no license is inferred.\n\nx=int(input())\nlis=[]\nwhile True:\n    x+=1\n    lis=list(str(x))\n    zan=0\n    for i in range(4):\n        zan+=int(lis[i])\n    if zan==20:\n        print(x)\n        break'
SAMPLE='1892\n'
GENERATOR_NAME='g23654'
def g23654(r): return f"{r.randint(1000,9000)}\n"

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
