import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/22548/\n# Accepted submission: 52510538\n# Source: http://cs101.openjudge.cn/practice/solution/52510538/\n# License: not declared on the submission page; no license is inferred.\n\nprice=[int(i) for i in input().split()]\nupstack=[]\nm=0\nfor p in price:\n    while upstack and upstack[-1]>=p:\n        upstack.pop()\n    upstack.append(p)\n    m=max(m,upstack[-1]-upstack[0])\nprint(m)'
SAMPLE='7 1 5 3 6 4\n'
GENERATOR_NAME='g22548'
def g22548(r):
    n=r.randint(2,40); a=[r.randint(0,10000) for _ in range(n)]
    if r.random()<.5: a.sort(reverse=True)
    return " ".join(map(str,a))+"\n"

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
