import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = "from collections import deque\ndire = [[-1, 0], [1, 0], [0, -1], [0, 1]]\ndef bfs(matrix, start, end, row, col):\n    q = deque([start])\n    visited = [[False]*col for _ in range(row)]\n    visited[start[0]][start[1]] = True\n    while q:\n        x, y = q.popleft()\n        if x == end[0] and y == end[1]:\n            break\n        for dx, dy in dire:\n            nx, ny = x+dx, y+dy\n            if 0 <= nx < row and 0 <= ny < col and matrix[nx][ny] != '1' and not visited[nx][ny]:\n                q.append((nx, ny))\n                visited[nx][ny] = (x, y)\n    res = []\n    pos = end\n    while pos != start:\n        res.append(pos)\n        pos = visited[pos[0]][pos[1]]\n    res.append(pos)\n    res.reverse()\n    return res\nX, Y = map(int, input().split())\nmatrix = [[x for x in input()] for _ in range(X)]\nfor i in range(X):\n    for j in range(Y):\n        if matrix[i][j] == 'R':\n            start = (i, j)\n        elif matrix[i][j] == 'C':\n            end = (i, j)\n        elif matrix[i][j] == 'Y':\n            key = (i, j)\nres_1 = bfs(matrix, start, key, X, Y)\nres_2 = bfs(matrix, key, end, X, Y)\nfor i, j in res_1+res_2[1:]:\n    print(i+1, j+1)"
SAMPLE = '5 7\n1R10001\n1010101\n1000011\n101100C\n1Y00011\n'
GENERATOR_NAME = 'g7209'
def g7209(r):
    rows,cols=r.randint(3,8),r.randint(3,8); cells=[(i,j) for i in range(rows) for j in range(cols)]
    a,y,c=r.sample(cells,3); g=[["0"]*cols for _ in range(rows)]
    for p,ch in ((a,"R"),(y,"Y"),(c,"C")): g[p[0]][p[1]]=ch
    return f"{rows} {cols}\n"+"\n".join("".join(x) for x in g)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
