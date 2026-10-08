"""7218 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 7218
SAMPLE_IN = '3\n3 4\n.S..\n###.\n..E.\n3 4\n.S..\n.E..\n....\n3 4\n.S..\n####\n..E.\n'
SAMPLE_OUT = '5\n1\noop!\n'
REFERENCE_SOURCE = 'from collections import deque\n\ndef solve_maze():\n    T = int(input())\n    for _ in range(T):\n        R, C = map(int, input().split())\n        maze = [list(input().strip()) for _ in range(R)]\n\n        # 找起点 S\n        for i in range(R):\n            for j in range(C):\n                if maze[i][j] == \'S\':\n                    start = (i, j)\n                if maze[i][j] == \'E\':\n                    end = (i, j)\n\n        # BFS\n        queue = deque()\n        visited = [[False] * C for _ in range(R)]\n        queue.append((start[0], start[1], 0))  # (row, col, distance)\n        visited[start[0]][start[1]] = True\n\n        found = False\n\n        while queue:\n            x, y, dist = queue.popleft()\n            if (x, y) == end:\n                print(dist)\n                found = True\n                break\n\n            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n                nx, ny = x + dx, y + dy\n                if 0 <= nx < R and 0 <= ny < C:\n                    if not visited[nx][ny] and maze[nx][ny] != \'#\':\n                        visited[nx][ny] = True\n                        queue.append((nx, ny, dist + 1))\n\n        if not found:\n            print("oop!")\n\n# 调用主函数\nsolve_maze()\n'

def valid(text):
    """题面契约：首行 T（1<=T<=10）；每组首行 R C（2<=R,C<=200），随后 R 行、每行 C 个字符，
    字符只有 S/E/#/.，且有且仅有一个 S 和一个 E。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if not lines[0].isdigit():
        return False
    T = int(lines[0])
    if not 1 <= T <= 10:
        return False
    p = 1
    for _ in range(T):
        if p >= len(lines):
            return False
        t = lines[p].split(' ')
        if len(t) != 2 or not all(x.isdigit() for x in t):
            return False
        R, C = map(int, t)
        if not (2 <= R <= 200 and 2 <= C <= 200):
            return False
        rows = lines[p + 1:p + 1 + R]
        if len(rows) != R or any(len(x) != C or set(x) - set('SE#.') for x in rows):
            return False
        g = ''.join(rows)
        if g.count('S') != 1 or g.count('E') != 1:
            return False
        p += 1 + R
    return p == len(lines)


def _maze(r, R, C, loops):
    """随机生成树迷宫（偶数坐标为结点），再随机打掉 loops 比例的墙。"""
    g = [['#'] * C for _ in range(R)]
    st = [(0, 0)]; g[0][0] = '.'
    while st:
        x, y = st[-1]
        nb = [(x + dx, y + dy, dx, dy) for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2))
              if 0 <= x + dx < R and 0 <= y + dy < C and g[x + dx][y + dy] == '#']
        if not nb:
            st.pop(); continue
        nx, ny, dx, dy = r.choice(nb)
        g[x + dx // 2][y + dy // 2] = '.'; g[nx][ny] = '.'; st.append((nx, ny))
    for x in range(R):
        for y in range(C):
            if g[x][y] == '#' and r.random() < loops:
                g[x][y] = '.'
    return g


def _dist(g, s, e):
    from collections import deque
    R, C = len(g), len(g[0]); d = {s: 0}; q = deque([s])
    while q:
        x, y = q.popleft()
        for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= a < R and 0 <= b < C and g[a][b] != '#' and (a, b) not in d:
                d[(a, b)] = d[(x, y)] + 1; q.append((a, b))
    return d.get(e), d


def _one(r, R, C, kind):
    """生成一张图。kind: open / random / maze / far / enclosed / adjacent / wallcut"""
    if kind in ('maze', 'mazefar'):
        g = _maze(r, R, C, r.choice([0.0, 0.02, 0.1]))
    elif kind == 'open':
        g = [['.'] * C for _ in range(R)]
    elif kind == 'wallcut':
        # 一道贯穿的墙，可能留一个缺口
        g = [['.'] * C for _ in range(R)]
        w = r.randint(1, C - 2) if C >= 3 else 0
        for x in range(R):
            g[x][w] = '#'
        if r.random() < 0.5:
            g[r.randrange(R)][w] = '.'
    else:
        dens = r.uniform(0.15, 0.42)
        g = [['#' if r.random() < dens else '.' for _ in range(C)] for _ in range(R)]
    free = [(x, y) for x in range(R) for y in range(C) if g[x][y] != '#'] or [(0, 0)]
    if kind == 'adjacent':
        x, y = r.randrange(R), r.randrange(C)
        nb = [(a, b) for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)) if 0 <= a < R and 0 <= b < C]
        s, e = (x, y), r.choice(nb)
    elif kind in ('far', 'mazefar'):
        # 起点在一个可达连通块里，终点取离它最远的格
        s = r.choice(free)
        _, d = _dist(g, s, None)
        mx = max(d.values())
        e = r.choice([p for p, v in d.items() if v == mx]) if mx > 0 else r.choice([p for p in free if p != s] or [(R - 1, C - 1)])
    else:
        s = r.choice(free)
        e = r.choice([p for p in free if p != s] or [(x, y) for x in range(R) for y in range(C) if (x, y) != s])
    if kind == 'enclosed':
        # 用墙把终点四周封死，起点那边连通块很大
        for a, b in ((e[0] + 1, e[1]), (e[0] - 1, e[1]), (e[0], e[1] + 1), (e[0], e[1] - 1)):
            if 0 <= a < R and 0 <= b < C and (a, b) != s:
                g[a][b] = '#'
    g[s[0]][s[1]] = 'S'; g[e[0]][e[1]] = 'E'
    return f"{R} {C}\n" + "\n".join("".join(x) for x in g)


def g7218(r, i):
    if i <= 3:
        # 最小规模：2×2 … 6×6，含相邻、不可达
        T = 10
        maps = [_one(r, r.randint(2, 6), r.randint(2, 6), r.choice(['random', 'adjacent', 'enclosed', 'wallcut', 'open']))
                for _ in range(T)]
    elif i <= 8:
        T = r.randint(1, 10)
        maps = [_one(r, r.randint(10, 80), r.randint(10, 80), r.choice(['random', 'maze', 'far', 'enclosed', 'wallcut']))
                for _ in range(T)]
    elif i <= 13:
        # 单组满规模：迷宫长路 / 终点被封
        T = 1
        R, C = [(200, 200), (200, 200), (200, 200), (2, 200), (200, 2)][i - 9]
        maps = [_one(r, R, C, ['mazefar', 'far', 'enclosed', 'mazefar', 'mazefar'][i - 9])]
    else:
        # T=10 组满规模，混合
        T = 10
        kinds = ['mazefar', 'far', 'random', 'enclosed', 'open', 'wallcut', 'maze', 'far', 'random', 'mazefar']
        r.shuffle(kinds)
        maps = [_one(r, r.randint(190, 200), r.randint(190, 200), k) for k in kinds]
    return str(T) + "\n" + "\n".join(maps) + "\n"


def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g7218(random.Random(NUMBER + i + attempt * 1000), i)
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
