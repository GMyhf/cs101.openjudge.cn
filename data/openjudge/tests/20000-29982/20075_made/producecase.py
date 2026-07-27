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
