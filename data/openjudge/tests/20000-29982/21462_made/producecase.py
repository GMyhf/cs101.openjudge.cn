import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/21462/\n# Accepted submission: 52213098\n# Source: http://cs101.openjudge.cn/practice/solution/52213098/\n# License: not declared on the submission page; no license is inferred.\n\nn=int(input())\nmatrix=[]\nfor i in range(n):\n    matrix.append(list(map(int,input().split())))\ndirections=[(1,0),(0,1),(-1,0),(0,-1)]\nx,y=0,0\nans=''\nd=0\ndx,dy=1,0\nvisited=set()\nwhile matrix[x][y]!=0:\n    ans+=chr(matrix[x][y])\n    visited.add((x,y))\n    nx,ny=x+dx,y+dy\n    if (not 0<=nx<n) or (not 0<=ny<n) or (nx,ny) in visited:\n        d=(d+1)%4\n        dx,dy=directions[d]\n        x,y=x+dx,y+dy\n    else:\n        x,y=nx,ny\nprint(ans)"
SAMPLE='3\n104 101 109\n97 0 111\n110 100 115\n'
GENERATOR_NAME='g21462'
def g21462(r):
    n = r.randint(2, 8)
    text = "HELLOCS"
    cells = [(i // n, i % n) for i in range(r.randint(1, n * n - 1))]
    grid = [[0] * n for _ in range(n)]
    for i, (x, y) in enumerate(cells):
        grid[x][y] = ord(text[i % len(text)])
    return f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in grid) + "\n"

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
