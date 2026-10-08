import random
REFERENCE='# External reference: /practice/29662/statistics/\n# Accepted submission: 52727805\n# Source: http://cs101.openjudge.cn/practice/solution/52727805/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n# 修正：N,M<=50 时连通陆地可达 2500 格，递归 DFS 超过默认 1000 层上限会 RecursionError\nsys.setrecursionlimit(20000)\nn,m=map(int,input().split())\ngraph=[[1]*(m+2)]\nfor i in range(n):\n    graph.append([1]+list(map(int,input().split()))+[1])\ngraph.append([1]*(m+2))\ndire=[(0,1),(0,-1),(1,0),(-1,0)]\nans=[[0]*(m+2) for i in range(n+2)]\ndef dfs(x,y):\n    ans[x][y]=1\n    for dx,dy in dire:\n        nx,ny=x+dx,y+dy\n        if 0<=nx<n+1 and 0<=ny<m+1 and ans[nx][ny]==0 and graph[nx][ny]==1:\n            dfs(nx,ny)\nfor i in range(m+2):\n    if ans[0][i]==0:\n        dfs(0,i)\nfor i in range(1,n+1):\n    if ans[i][0]==0:\n        dfs(i,0)\n    if ans[i][m+1]==0:\n        dfs(i,m+1)\nfor i in range(m+2):\n    if ans[n+1][i]==0:\n        dfs(n+1,i)\nfor k in range(1,n+1):\n    print(" ".join(str(i) for i in ans[k][1:m+1]))'
SAMPLE='4 5\n1 1 0 0 0\n1 1 0 0 0\n0 0 1 0 0\n0 0 0 1 1\n'
GENERATOR_NAME='g29662'
def g29662(r):
    n, m = r.randint(1, 30), r.randint(1, 30)
    rows = [[r.randint(0, 1) for _ in range(m)] for _ in range(n)]
    return f"{n} {m}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"

from pathlib import Path
import random, subprocess, sys, tempfile


def valid(text):
    """题面：第一行 N M（1<=N,M<=50）；之后 N 行，每行 M 个数字（0 或 1），空格分隔。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    head = lines[0].split(" ")
    if len(head) != 2 or not all(t.isdigit() for t in head):
        return False
    n, m = map(int, head)
    if not (1 <= n <= 50 and 1 <= m <= 50) or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        toks = line.split(" ")
        if len(toks) != m or any(t not in ("0", "1") for t in toks):
            return False
    return True


def _grid(rows):
    return f"{len(rows)} {len(rows[0])}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"


def _snake(n, m, off):
    """在 [off, n-off) x [off, m-off) 内画一条蛇形的连通陆地（偶数相对行整行为陆地，两端交替连接），连通块很深。"""
    g = [[0] * m for _ in range(n)]
    top, bottom, left, right = off, n - 1 - off, off, m - 1 - off
    for t, i in enumerate(range(top, bottom + 1)):
        if t % 2 == 0:
            for j in range(left, right + 1): g[i][j] = 1
        else:
            g[i][right if t % 4 == 1 else left] = 1
    return g


def special_case(index):
    """第 25..39 组：补 1x1、单行/单列、全 0/全 1、50x50 满规模、深递归蛇形、仅对角相邻（不连通）等情形。"""
    r = random.Random(296620 + index)
    k = index - 25
    if k == 0:
        return "1 1\n1\n"
    if k == 1:
        return "1 50\n" + " ".join(str(r.randint(0, 1)) for _ in range(50)) + "\n"
    if k == 2:
        return _grid([[r.randint(0, 1)] for _ in range(50)])
    if k == 3:
        return "3 3\n0 0 0\n0 1 0\n0 0 0\n"                 # 唯一孤岛被沉没
    if k == 4:
        return _grid([[1] * 50 for _ in range(50)])          # 全陆地，与边缘相连，不变
    if k == 5:
        return _grid([[0] * 50 for _ in range(50)])          # 全水
    if k == 6:                                               # 内部全 1、边缘全 0：整块沉没
        return _grid([[1 if 0 < i < 49 and 0 < j < 49 else 0 for j in range(50)] for i in range(50)])
    if k == 7:                                               # 从边缘出发的蛇形长陆地（递归很深），整体保留
        return _grid(_snake(49, 50, 0))
    if k == 8:                                               # 内部蛇形长陆地，不碰边缘，整体沉没
        return _grid(_snake(50, 50, 1))
    if k == 9:                                               # 棋盘格：只有对角相邻，内部的 1 全部沉没
        return _grid([[(i + j) % 2 for j in range(50)] for i in range(50)])
    if k == 10:                                              # 边框陆地 + 内部与边框仅对角相邻的岛
        g = [[1 if i in (0, 49) or j in (0, 49) else 0 for j in range(50)] for i in range(50)]
        for i in range(2, 48, 3):
            for j in range(2, 48, 3):
                g[i][j] = 1
        g[1][1] = 0
        return _grid(g)
    p = [0.3, 0.45, 0.55, 0.6, 0.7][k - 11] if k < 16 else 0.5
    return _grid([[1 if r.random() < p else 0 for _ in range(50)] for _ in range(50)])

REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) if seed < 25 else special_case(seed) for seed in range(1, 40)]
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
