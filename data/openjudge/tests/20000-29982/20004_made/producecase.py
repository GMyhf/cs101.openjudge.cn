import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/20004 statistics, Accepted solution 43218123.\n# Source: http://cs101.openjudge.cn/practice/solution/43218123/\n# Statistics: http://cs101.openjudge.cn/practice/20004/statistics/\n# License: not declared on submission page; no license inferred\nr=[float(i[:-1])/100 for i in input().split()]\nt=[1+r[0]]\nfor i in r[1:]:\n    t.append(t[-1]*(1+i))\nl=len(t)\nmmin=[(t[-1],l-1)]\nfor i in range(1,len(r)):\n    if t[l-i-1]<mmin[i-1][0]:\n        mmin.append((t[l-i-1],l-i-1))\n    else:\n        mmin.append(mmin[i-1])\nans,pos=0,0\nfor i in range(len(t)):\n    if ans<(t[i]-mmin[l-i-1][0])/t[i]:\n        ans=(t[i]-mmin[l-i-1][0])/t[i]\n        pos=mmin[l-i-1][1]-i\nprint(f'{-1*ans*100:.1f}% {pos}')\n"
SAMPLE='3.5407% -7.1619% -6.8417% -5.6495% 9.0260% 7.7859% -0.6648% -0.8765% -0.5759% -7.8740%\n'
GENERATOR_NAME='g20004'
def g20004(r):
    return " ".join(f"{r.uniform(-9.9, 9.9):.4f}%" for _ in range(r.randint(11, 30))) + "\n"

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
