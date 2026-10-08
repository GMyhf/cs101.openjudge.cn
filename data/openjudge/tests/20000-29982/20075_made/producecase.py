import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/20075 statistics, Accepted solution 51319354.\n# Source: http://cs101.openjudge.cn/practice/solution/51319354/\n# Statistics: http://cs101.openjudge.cn/practice/20075/statistics/\n# License: not declared on submission page; no license inferred\nfrom collections import deque\ndire = [(-1, 0), (1, 0), (0, -1), (0, 1)]\ndef bfs(sx, sy):\n    q = deque([(sx, sy, 0)])\n    visited = [[0]*n for _ in range(m)]\n    visited[sx][sy] = 1\n    if matrix[sx][sy] == 2:\n        return 'NO'\n    while q:\n        x, y, step = q.popleft()\n        if matrix[x][y] == 1:\n            return step\n        for dx, dy in dire:\n            nx, ny = x + dx, y + dy\n            if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny]:\n                if matrix[nx][ny] == 2:\n                    visited[nx][ny] = 1\n                    continue\n                else:\n                    q.append((nx, ny, step+1))\n                    visited[nx][ny] = 1\n    return 'NO'\nm, n, p = map(int, input().split())\nmatrix = [[int(x) for x in input().split()] for _ in range(m)]\nfor _ in range(p):\n    y, x = map(int, input().split())\n    print(bfs(x-1, y-1))\n"
SAMPLE='3 4 1\n0 0 2 0\n0 2 1 0\n0 0 0 0\n1 1\n'
GENERATOR_NAME='g20075'
def g20075(r):
    m, n = r.randint(3, 8), r.randint(3, 8)
    grid = [[0 if r.random() < .7 else 2 for _ in range(n)] for _ in range(m)]
    target = (r.randrange(m), r.randrange(n))
    grid[target[0]][target[1]] = 1
    starts = []
    for _ in range(r.randint(5, 15)):
        starts.append((r.randrange(m), r.randrange(n)))
    return f"{m} {n} {len(starts)}\n" + "\n".join(
        " ".join(map(str, row)) for row in grid
    ) + "\n" + "\n".join(f"{y + 1} {x + 1}" for x, y in starts) + "\n"

def valid(text):
    """题面：首行 m n p（m<=100，n<=100，0<p<=1000）；m 行各 n 个 0/1/2；
    p 行坐标 "x y"（x 横坐标即列号 1..n，y 纵坐标即行号 1..m，保证在地图上）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    head = lines[0].split(" ")
    if len(head) != 3 or not all(t.isdigit() for t in head):
        return False
    m, n, p = map(int, head)
    if not (1 <= m <= 100 and 1 <= n <= 100 and 1 <= p <= 1000):
        return False
    if len(lines) != 1 + m + p:
        return False
    for row in lines[1:1 + m]:
        tok = row.split(" ")
        if len(tok) != n or any(t not in ("0", "1", "2") for t in tok):
            return False
    for row in lines[1 + m:]:
        tok = row.split(" ")
        if len(tok) != 2 or not all(t.isdigit() for t in tok):
            return False
        x, y = map(int, tok)
        if not (1 <= x <= n and 1 <= y <= m):
            return False
    return True


def _fmt(grid, starts):
    """starts 是 (行, 列)，0 起；输出为 "列+1 行+1"。"""
    m, n = len(grid), len(grid[0])
    return f"{m} {n} {len(starts)}\n" + "\n".join(
        " ".join(map(str, row)) for row in grid
    ) + "\n" + "\n".join(f"{c + 1} {rr + 1}" for rr, c in starts) + "\n"


def g_big(r, m, n, wall, treasures, p, far=False):
    grid = [[2 if r.random() < wall else 0 for _ in range(n)] for _ in range(m)]
    for _ in range(treasures):
        grid[r.randrange(m)][r.randrange(n)] = 1
    if far:
        grid[0][0] = 1
        starts = [(r.randrange(m // 2, m), r.randrange(n // 2, n)) for _ in range(p)]
    else:
        starts = [(r.randrange(m), r.randrange(n)) for _ in range(p)]
    return _fmt(grid, starts)


def g_snake(r, m, n, p):
    """蛇形迷宫：奇数行整行是墙、交替在左/右端留口，宝藏在起点另一端，最短路极长。"""
    grid = [[0] * n for _ in range(m)]
    for i in range(1, m, 2):
        grid[i] = [2] * n
        grid[i][n - 1 if (i // 2) % 2 == 0 else 0] = 0
    grid[m - 1][n - 1 if ((m - 1) // 2) % 2 == 0 else 0] = 1
    starts = [(0, 0)] + [(2 * r.randrange((m + 1) // 2), r.randrange(n)) for _ in range(p - 1)]
    return _fmt(grid, starts)


def build_extra():
    r = random.Random(20075 * 31)
    cases = [
        "5 5 5\n0 0 2 2 0\n2 0 0 0 2\n0 0 2 0 2\n0 2 2 1 2\n0 0 2 2 2\n1 1\n2 1\n1 5\n4 4\n5 1\n",  # 题面样例 2
        "1 1 1\n1\n1 1\n",                    # 起点即宝藏 -> 0
        "1 1 1\n2\n1 1\n",                    # 起点即陷阱 -> NO
        "1 5 3\n0 0 0 0 1\n1 1\n5 1\n3 1\n",   # 单行走廊
        "4 1 2\n0\n2\n0\n1\n1 1\n1 3\n",      # 单列，被陷阱隔开
    ]
    cases.append(g_big(r, 100, 100, 0.3, 5, 1000))
    cases.append(g_big(r, 100, 100, 0.0, 1, 600, far=True))
    cases.append(g_big(r, 100, 100, 0.45, 3, 1000))
    cases.append(g_big(r, 100, 100, 0.6, 20, 1000))     # 陷阱多，大量 NO
    cases.append(g_big(r, 37, 100, 0.25, 2, 500))
    cases.append(g_snake(r, 99, 100, 300))
    cases.append(g_snake(r, 100, 99, 300))
    return cases


def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases += build_extra()
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
