import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="import sys,itertools\ndef solve():\n    a=list(map(int,sys.stdin.read().split())); p=0; n,m=a[p],a[p+1]; p+=2\n    g=[a[p+i*m:p+(i+1)*m] for i in range(n)]; p+=n*m\n    v=[a[p+i*(m+1):p+(i+1)*(m+1)] for i in range(n)]; p+=n*(m+1)\n    h=[a[p+i*m:p+(i+1)*m] for i in range(n+1)]\n    k=n*m; need={i*m+j for i in range(n) for j in range(m) if g[i][j]}; ans=10**30\n    for mask in range(1<<k):\n        if any(not(mask>>u&1) for u in need): continue\n        seen={next(iter(need))}; q=list(seen)\n        for u in q:\n            i,j=divmod(u,m)\n            for z in (u-1 if j else -1, u+1 if j+1<m else -1,\n                      u-m if i else -1, u+m if i+1<n else -1):\n                if z >= 0 and mask>>z&1 and z not in seen:\n                    seen.add(z); q.append(z)\n        if len(seen) != bin(mask).count('1'): continue\n        cost=0\n        for i in range(n):\n            for j in range(m):\n                u=i*m+j\n                if j==0 and mask>>u&1: cost+=v[i][0]\n                if j==m-1 and mask>>u&1: cost+=v[i][m]\n                if i==0 and mask>>u&1: cost+=h[0][j]\n                if i==n-1 and mask>>u&1: cost+=h[n][j]\n                if j+1<m and ((mask>>u&1)!=(mask>>(u+1)&1)): cost+=v[i][j+1]\n                if i+1<n and ((mask>>u&1)!=(mask>>(u+m)&1)): cost+=h[i+1][j]\n        ans=min(ans,cost)\n    print(ans)\nif __name__=='__main__': solve()\n"
SAMPLE='3 3\n1 0 0\n1 0 0\n0 0 1\n1 4 9 4\n1 6 6 6\n1 2 2 9\n1 1 1\n4 4 4\n2 4 2\n6 6 6\n'
GENERATOR_NAME='g21520'
def g21520(r):
    n, m = r.randint(2, 3), r.randint(2, 3)
    cells = [[0] * m for _ in range(n)]
    villages = r.randint(1, min(5, n * m))
    for x, y in r.sample([(x, y) for x in range(n) for y in range(m)], villages):
        cells[x][y] = 1
    cells[0][0] = 1
    vertical = [[r.randint(1, 12) for _ in range(m + 1)] for _ in range(n)]
    horizontal = [[r.randint(1, 12) for _ in range(m)] for _ in range(n + 1)]
    return (f"{n} {m}\n" + "\n".join(" ".join(map(str, row)) for row in cells) + "\n" +
            "\n".join(" ".join(map(str, row)) for row in vertical) + "\n" +
            "\n".join(" ".join(map(str, row)) for row in horizontal) + "\n")

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
