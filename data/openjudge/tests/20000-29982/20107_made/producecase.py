import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20107 statistics, Accepted solution 22600399.\n# Source: http://cs101.openjudge.cn/practice/solution/22600399/\n# Statistics: http://cs101.openjudge.cn/practice/20107/statistics/\n# License: not declared on submission page; no license inferred\nd=int(input())\nn,T=map(int,input().split())\nz=[[0 for i in range(135)] for i in range(135)]\ntimes=[]\nfor i in range(n):\n    times.append(list(map(int,input().split())))\n    z[times[i][0]][times[i][1]]=i+1\n    times[i].remove(times[i][0])\n    times[i].remove(times[i][0])\n    \ndef take(x1,x2,y1,y2,t):\n    s=0\n    if(x1<0):\n        x1=0\n    if(y1<0):\n        y1=0\n    if(x2>128):\n        x2=128\n    if(y2>128):\n        y2=128\n    for i in range(x1,x2+1):\n        for j in range(y1,y2+1):\n            if(z[i][j]>0):\n                s+=times[z[i][j]-1][t]\n    return s\n\nmaxn=-1\nnum=0\nt0=0\nfor i in range(0,129):\n    for j in range(0,129):\n        for t in range(0,T):\n            a=take(i-d,i+d,j-d,j+d,t)\n            if(maxn<a):\n                maxn=a\n                num=1\n                t0=t\n            elif(maxn==a):\n                num+=1\n\nprint(num,t0,maxn)\n'
SAMPLE='1\n2 1\n4 4 10\n6 6 20\n'
GENERATOR_NAME='g20107'
def g20107(r):
    d, k, t = r.randint(1, 2), r.randint(1, 8), r.randint(1, 2)
    coords = r.sample([(x, y) for x in range(20, 121, 10) for y in range(20, 121, 10)], k)
    rows = [f"{x} {y} " + " ".join(str(r.randint(0, 100)) for _ in range(t)) for x, y in coords]
    return f"{d}\n{k} {t}\n" + "\n".join(rows) + "\n"

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
