import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def dfs(mx, visited, x, y):\n    # 如果到达右下角，返回True\n    if x == n - 1 and y == n - 1:\n        return True\n\n    # 定义向右和向下的移动方向\n    directions = [(0, 1), (1, 0)]\n\n    for dx, dy in directions:\n        nx = x + dx\n        ny = y + dy\n        # 检查新坐标是否在矩阵范围内，是否已经访问过，以及是否可以通过\n        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and mx[nx][ny] == 0:\n            visited[nx][ny] = True\n            if dfs(mx, visited, nx, ny):\n                return True\n            visited[nx][ny] = False\n\n    return False\n\n# 读取输入\nn = int(input())\nmx = [list(map(int, input().split())) for _ in range(n)]\n\n# 初始化访问标记数组\nvisited = [[False] * n for _ in range(n)]\n\n# 起始点 (0, 0) 必须是可以通过的\nif mx[0][0] == 1:\n    print('No')\nelse:\n    visited[0][0] = True\n    if dfs(mx, visited, 0, 0):\n        print('Yes')\n    else:\n        print('No')\n"
SAMPLE_IN = '5\n0 0 1 1 0\n0 0 0 0 0\n0 1 1 1 0\n0 1 1 1 0\n0 1 1 1 0\n'
SAMPLE_OUT = 'Yes\n'
def generate_case(r):
    n = r.randint(2, 14)
    grid = [[0 if r.random() < .72 else 1 for _ in range(n)] for _ in range(n)]
    grid[0][0] = grid[-1][-1] = 0
    if r.random() < .55:
        for i in range(n):
            grid[i][i] = 0
    else:
        grid[0][1] = grid[1][0] = 1
    assert grid[0][0] == grid[-1][-1] == 0
    return str(n) + "\n" + "\n".join(" ".join(map(str, row)) for row in grid) + "\n"


def valid(text):
    # 题面：第一行 N（2<=N<=20），接下来 N 行每行 N 个以空格分隔的 0/1；保证 (0,0) 与 (N-1,N-1) 为 0
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0] != str(int(lines[0])): return False
    n = int(lines[0])
    if not 2 <= n <= 20 or len(lines) != n + 1: return False
    grid = []
    for line in lines[1:]:
        row = line.split(" ")
        if len(row) != n or any(t not in ("0", "1") for t in row): return False
        grid.append(row)
    return grid[0][0] == "0" and grid[-1][-1] == "0"

def oracle(text):
    # 独立的 DP：只向右/向下能否到达
    lines = text.split("\n"); n = int(lines[0])
    g = [lines[1 + i].split() for i in range(n)]
    ok = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == "0":
                ok[i][j] = (i == 0 and j == 0) or (i > 0 and ok[i-1][j]) or (j > 0 and ok[i][j-1])
    return "Yes\n" if ok[-1][-1] else "No\n"

def ref_within_budget(text, budget=200000):
    # 与 REFERENCE_SOURCE 同一算法（回溯 DFS，失败会撤销 visited）的计数版
    lines = text.split("\n"); n = int(lines[0])
    mx = [list(map(int, lines[1 + i].split())) for i in range(n)]
    visited = [[False] * n for _ in range(n)]; calls = [0]
    def dfs(x, y):
        calls[0] += 1
        if calls[0] > budget: raise OverflowError
        if x == n - 1 and y == n - 1: return True
        for dx, dy in ((0, 1), (1, 0)):
            nx, ny = x + dx, y + dy
            if nx < n and ny < n and not visited[nx][ny] and mx[nx][ny] == 0:
                visited[nx][ny] = True
                if dfs(nx, ny): return True
                visited[nx][ny] = False
        return False
    try:
        dfs(0, 0)
    except OverflowError:
        return False
    return True

def fmt(grid):
    return str(len(grid)) + "\n" + "\n".join(" ".join(map(str, row)) for row in grid) + "\n"

def generate_big(r, want):
    # N=20 满规模：随机障碍 + 按需求打通一条单调路径或用墙封死
    n = 20
    while True:
        p = r.choice([.2, .3, .4, .5])
        grid = [[0 if r.random() > p else 1 for _ in range(n)] for _ in range(n)]
        if want == "Yes":
            i = j = 0
            while (i, j) != (n - 1, n - 1):
                grid[i][j] = 0
                if i == n - 1 or (j < n - 1 and r.random() < .5): j += 1
                else: i += 1
        else:
            # 一条反对角方向的墙：i+j==d 的格子全为 1，必然无法通过
            d = r.randint(3, 2 * n - 5)
            for i in range(n):
                if 0 <= d - i < n: grid[i][d - i] = 1
        grid[0][0] = grid[-1][-1] = 0
        c = fmt(grid)
        if oracle(c) == want + "\n": return c

FIXED = [
    fmt([[0, 0], [0, 0]]),
    fmt([[0, 1], [1, 0]]),
    fmt([[0, 1], [0, 0]]),
    fmt([[0] * 20 for _ in range(20)]),
    fmt([[0] * 3, [1, 1, 0], [1, 1, 0]]),
]

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        cases = []
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(23937 + index + attempt * 1000))
                    if content not in cases: break
                else: raise AssertionError("insufficient diversity")
            cases.append(content)
        cases += [c for c in FIXED if c not in cases]
        seed = 0
        while len(cases) < 40:
            want = "Yes" if len(cases) % 2 else "No"
            c = generate_big(random.Random(239370 + seed), want); seed += 1
            if c in cases: continue
            # 参考解是带回溯的 DFS：过滤掉会让它指数爆炸的输入（按调用步数，不按计时，保证可复现）
            if not ref_within_budget(c): continue
            cases.append(c)
        for index, content in enumerate(cases):
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            assert result.stdout == oracle(content), index
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
