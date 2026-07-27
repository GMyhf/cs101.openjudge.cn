import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20103 statistics, Accepted solution 43490046.\n# Source: http://cs101.openjudge.cn/practice/solution/43490046/\n# Statistics: http://cs101.openjudge.cn/practice/20103/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nm,l=[-float("inf")],[0]\nfor i in range(n):\n    mi,li=map(int,input().split())\n    m.append(mi)\n    l.append(li)\nm.append(float("inf"))\nl.append(0)\nans=0\nend=-float("inf")\nfor i in range(1,n+1):\n    if m[i-1]<m[i]-l[i] and end<m[i]-l[i] and  m[i]+l[i]<m[i+1]:\n        ans+=1\n        end=m[i]+l[i]\nprint(ans)\n'
SAMPLE='2\n1 3\n3 1\n'
GENERATOR_NAME='g20103'
def g20103(r):
    n = r.randint(2, 15)
    marks = sorted(r.sample(range(1, 200), n))
    return f"{n}\n" + "\n".join(f"{x} {r.randint(1, 30)}" for x in marks) + "\n"

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
