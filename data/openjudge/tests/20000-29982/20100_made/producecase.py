import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20100 statistics, Accepted solution 43253417.\n# Source: http://cs101.openjudge.cn/practice/solution/43253417/\n# Statistics: http://cs101.openjudge.cn/practice/20100/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nv=list(map(int,input().split()))\nr=list(map(int,input().split()))\nt=list(map(int,input().split()))\nvm=0\ntm=1<<30\ncnt=0\nfor i in range(n-1):\n    v[i]/=t[i]\nfor i in range(n-1):\n    if (v[i]>vm or t[i]<tm) and t[i]<r[i]:\n        cnt+=1\n    vm=max(vm,v[i])\n    tm=min(tm,t[i])\nprint(cnt)\n'
SAMPLE='4\n6 6 6\n3 4 5\n1 4 6\n'
GENERATOR_NAME='g20100'
def g20100(r):
    n = r.randint(2, 10)
    distances = [r.randint(1, 10000) for _ in range(n - 1)]
    record = [r.randint(1, 10000) for _ in range(n - 1)]
    monster = [r.randint(1, 10000) for _ in range(n - 1)]
    return f"{n}\n{' '.join(map(str, distances))}\n{' '.join(map(str, record))}\n{' '.join(map(str, monster))}\n"

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
