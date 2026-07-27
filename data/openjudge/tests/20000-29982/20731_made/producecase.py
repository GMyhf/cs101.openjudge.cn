import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/20731/\n# Accepted submission: 52201327\n# Source: http://cs101.openjudge.cn/practice/solution/52201327/\n# License: not declared on the submission page; no license is inferred.\n\nm,n=map(int,input().split())\nmatrix=[]\nfor i in range(m):\n    matrix.append(list(map(int,input().split())))\nx,y=map(int,input().split())\nx,y=x-1,y-1\nif (x==0 and y==m-1) or (x!=0 and y!=m-1):\n    ans=sum(matrix[0])+sum(matrix[m-1])\n    for i in range(1,m-1):\n        ans+=matrix[i][0]+matrix[i][n-1]\nelse:\n    matrix[x],matrix[y]=matrix[y],matrix[x]\n    ans=sum(matrix[0])+sum(matrix[m-1])\n    for i in range(1,m-1):\n        ans+=matrix[i][0]+matrix[i][n-1]\nprint(ans)'
SAMPLE='3 3\n3 4 1\n3 7 1\n2 0 1\n1 2\n'
GENERATOR_NAME='g20731'
def g20731(r):
    m, n = r.randint(2, 8), r.randint(2, 8)
    rows = [[r.randint(-20, 20) for _ in range(n)] for _ in range(m)]
    x, y = r.sample(range(1, m + 1), 2)
    return f"{m} {n}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + f"\n{x} {y}\n"

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
