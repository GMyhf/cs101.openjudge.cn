import random
REFERENCE='# External reference: /practice/29662/statistics/\n# Accepted submission: 52727805\n# Source: http://cs101.openjudge.cn/practice/solution/52727805/\n# License: not declared on the submission page; no license is inferred.\n\nn,m=map(int,input().split())\ngraph=[[1]*(m+2)]\nfor i in range(n):\n    graph.append([1]+list(map(int,input().split()))+[1])\ngraph.append([1]*(m+2))\ndire=[(0,1),(0,-1),(1,0),(-1,0)]\nans=[[0]*(m+2) for i in range(n+2)]\ndef dfs(x,y):\n    ans[x][y]=1\n    for dx,dy in dire:\n        nx,ny=x+dx,y+dy\n        if 0<=nx<n+1 and 0<=ny<m+1 and ans[nx][ny]==0 and graph[nx][ny]==1:\n            dfs(nx,ny)\nfor i in range(m+2):\n    if ans[0][i]==0:\n        dfs(0,i)\nfor i in range(1,n+1):\n    if ans[i][0]==0:\n        dfs(i,0)\n    if ans[i][m+1]==0:\n        dfs(i,m+1)\nfor i in range(m+2):\n    if ans[n+1][i]==0:\n        dfs(n+1,i)\nfor k in range(1,n+1):\n    print(" ".join(str(i) for i in ans[k][1:m+1]))'
SAMPLE='4 5\n1 1 0 0 0\n1 1 0 0 0\n0 0 1 0 0\n0 0 0 1 1\n'
GENERATOR_NAME='g29662'
def g29662(r):
    n, m = r.randint(1, 30), r.randint(1, 30)
    rows = [[r.randint(0, 1) for _ in range(m)] for _ in range(n)]
    return f"{n} {m}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
