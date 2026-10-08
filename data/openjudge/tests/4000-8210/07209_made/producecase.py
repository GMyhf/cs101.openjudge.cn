import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = "from collections import deque\ndire = [[-1, 0], [1, 0], [0, -1], [0, 1]]\ndef bfs(matrix, start, end, row, col):\n    q = deque([start])\n    visited = [[False]*col for _ in range(row)]\n    visited[start[0]][start[1]] = True\n    while q:\n        x, y = q.popleft()\n        if x == end[0] and y == end[1]:\n            break\n        for dx, dy in dire:\n            nx, ny = x+dx, y+dy\n            if 0 <= nx < row and 0 <= ny < col and matrix[nx][ny] != '1' and not visited[nx][ny]:\n                q.append((nx, ny))\n                visited[nx][ny] = (x, y)\n    res = []\n    pos = end\n    while pos != start:\n        res.append(pos)\n        pos = visited[pos[0]][pos[1]]\n    res.append(pos)\n    res.reverse()\n    return res\nX, Y = map(int, input().split())\nmatrix = [[x for x in input()] for _ in range(X)]\nfor i in range(X):\n    for j in range(Y):\n        if matrix[i][j] == 'R':\n            start = (i, j)\n        elif matrix[i][j] == 'C':\n            end = (i, j)\n        elif matrix[i][j] == 'Y':\n            key = (i, j)\nres_1 = bfs(matrix, start, key, X, Y)\nres_2 = bfs(matrix, key, end, X, Y)\nfor i, j in res_1+res_2[1:]:\n    print(i+1, j+1)"
SAMPLE = '5 7\n1R10001\n1010101\n1000011\n101100C\n1Y00011\n'
GENERATOR_NAME = 'g7209'


def valid(text):
    """题面契约：第一行两个整数 X<100、Y<100（行、列）；随后 X 行、每行 Y 个字符的地图，
    字符只有 1/0/R/C/Y，入口 R、出口 C、钥匙 Y 各恰好一个。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    t = lines[0].split(' ')
    if len(t) != 2 or not all(x.isdigit() for x in t):
        return False
    X, Y = map(int, t)
    if not (1 <= X < 100 and 1 <= Y < 100) or len(lines) != X + 1:
        return False
    rows = lines[1:]
    if any(len(r) != Y or set(r) - set('01RCY') for r in rows):
        return False
    s = ''.join(rows)
    return s.count('R') == 1 and s.count('C') == 1 and s.count('Y') == 1


def _bfs(g, s, block):
    """返回 (dist, ways)，ways 截断到 2。"""
    from collections import deque
    X, Y = len(g), len(g[0])
    dist = {s: 0}; ways = {s: 1}; q = deque([s])
    while q:
        x, y = q.popleft()
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            z = (x + dx, y + dy)
            if 0 <= z[0] < X and 0 <= z[1] < Y and g[z[0]][z[1]] != '1' and z not in block:
                if z not in dist:
                    dist[z] = dist[(x, y)] + 1; ways[z] = ways[(x, y)]; q.append(z)
                elif dist[z] == dist[(x, y)] + 1:
                    ways[z] = min(2, ways[z] + ways[(x, y)])
    return dist, ways


def _unique(g, R, K, C):
    """拿钥匙再出门的最快路线是否唯一；且不论“拿钥匙前能否踩出口格”两种读法都一样。"""
    d1, w1 = _bfs(g, R, set())
    if K not in d1 or w1[K] != 1:
        return False
    d1b, w1b = _bfs(g, R, {C})
    if d1b.get(K) != d1[K] or w1b[K] != 1:
        return False
    d2, w2 = _bfs(g, K, set())
    return C in d2 and w2[C] == 1


def _maze(r, X, Y):
    """随机生成树迷宫：偶数坐标格为结点，DFS 打通，路径天然唯一。"""
    g = [['1'] * Y for _ in range(X)]
    st = [(0, 0)]; g[0][0] = '0'
    while st:
        x, y = st[-1]
        nb = [(x + dx, y + dy, dx, dy) for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2))
              if 0 <= x + dx < X and 0 <= y + dy < Y and g[x + dx][y + dy] == '1']
        if not nb:
            st.pop(); continue
        nx, ny, dx, dy = r.choice(nb)
        g[x + dx // 2][y + dy // 2] = '0'; g[nx][ny] = '0'; st.append((nx, ny))
    return g


def _render(g):
    return f"{len(g)} {len(g[0])}\n" + "\n".join("".join(x) for x in g) + "\n"


def g7209(r, i):
    if i <= 4:
        # 极小规模：单行 / 单列，钥匙在入口背后，须折返
        n = r.randint(3, 12)
        cells = ['0'] * n
        a, b, c = sorted(r.sample(range(n), 3))
        order = r.choice([('Y', 'R', 'C'), ('C', 'R', 'Y')])
        for p, ch in zip((a, b, c), order):
            cells[p] = ch
        g = [cells] if i % 2 else [[ch] for ch in cells]
        return _render(g)
    if i <= 14:
        # 小随机图：带障碍，拒绝采样保证路线唯一
        while True:
            X, Y = r.randint(2, 12), r.randint(2, 12)
            dens = r.uniform(0.25, 0.45)
            g = [['1' if r.random() < dens else '0' for _ in range(Y)] for _ in range(X)]
            free = [(x, y) for x in range(X) for y in range(Y)]
            if len(free) < 3:
                continue
            R, K, C = r.sample(free, 3)
            for p, ch in ((R, 'R'), (K, 'Y'), (C, 'C')):
                g[p[0]][p[1]] = ch
            if _unique(g, R, K, C) and abs(R[0]-K[0]) + abs(R[1]-K[1]) + abs(K[0]-C[0]) + abs(K[1]-C[1]) >= 4:
                return _render(g)
    # 迷宫：中等到满规模 99×99，再随机打通一些墙形成环（仍保证唯一）
    if i <= 24:
        X, Y = r.randint(15, 60), r.randint(15, 60)
    elif i <= 35:
        X, Y = r.randint(85, 99), r.randint(85, 99)
    else:
        X, Y = 99, 99
    g = _maze(r, X, Y)
    free = [(x, y) for x in range(X) for y in range(Y) if g[x][y] == '0']
    while True:
        R, K, C = r.sample(free, 3)
        if i >= 25:
            d, _ = _bfs(g, R, set())
            if d[K] < (X + Y) // 2:
                continue
        for p, ch in ((R, 'R'), (K, 'Y'), (C, 'C')):
            g[p[0]][p[1]] = ch
        if _unique(g, R, K, C):  # 树上 R→钥匙 的路线不得经过出口
            break
        for p in (R, K, C):
            g[p[0]][p[1]] = '0'
    walls = [(x, y) for x in range(X) for y in range(Y) if g[x][y] == '1']
    r.shuffle(walls)
    loops = r.choice([0, 20, 60])
    for (x, y) in walls[:loops * 3]:
        if loops <= 0:
            break
        g[x][y] = '0'
        if _unique(g, R, K, C):
            loops -= 1
        else:
            g[x][y] = '1'
    assert _unique(g, R, K, C)
    return _render(g)


def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed), seed) for seed in range(1, 40)]
    for i,text in enumerate(cases):
        assert valid(text), i
        g=[list(x) for x in text.split('\n')[1:-1]]
        pos={ch:(a,b) for a,row in enumerate(g) for b,ch in enumerate(row) if ch in 'RYC'}
        assert _unique(g,pos['R'],pos['Y'],pos['C']), i
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
