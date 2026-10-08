"""4115 鸣人和佐助 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

第 0 组为题面样例 1，第 1 组为题面样例 2；其余覆盖最小规模（1x2 / 2x1）、
T=0、-1（被厚墙围住 / T 不够）、长蛇形路径、以及 199x199 满规模的随机图与迷宫，
其中若干组专门卡「visited 只记坐标、不记剩余查克拉」的写法。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4115
SAMPLE_IN = '4 4 1\n#@##\n**##\n###+\n****\n'
SAMPLE_OUT = '6\n'
SAMPLE2_IN = '4 4 2\n#@##\n**##\n###+\n****\n'
SAMPLE2_OUT = '4\n'
REFERENCE_SOURCE = "# 夏天明 元培学院\n\nfrom collections import deque\n\nM, N, T = map(int, input().split())\ngraph = [list(input()) for i in range(M)]\ndirec = [(0,1), (1,0), (-1,0), (0,-1)]\nstart, end = None, None\nfor i in range(M):\n    for j in range(N):\n        if graph[i][j] == '@':\n            start = (i, j)\ndef bfs():\n    q = deque([start + (T, 0)])\n    visited = [[-1]*N for i in range(M)]\n    visited[start[0]][start[1]] = T\n    while q:\n        x, y, t, time = q.popleft()\n        time += 1\n        for dx, dy in direc:\n            if 0<=x+dx<M and 0<=y+dy<N:\n                if (elem := graph[x+dx][y+dy]) == '*' and t > visited[x+dx][y+dy]:\n                    visited[x+dx][y+dy] = t\n                    q.append((x+dx, y+dy, t, time))\n                elif elem == '#' and t > 0 and t-1 > visited[x+dx][y+dy]:\n                    visited[x+dx][y+dy] = t-1\n                    q.append((x+dx, y+dy, t-1, time))\n                elif elem == '+':\n                    return time\n    return -1\nprint(bfs())\n"


def valid(text):
    """题面：第一行 M N T（0<M,N<200，0<=T<10），随后 M 行每行 N 个字符，
    字符取自 @ + * #，且鸣人 @、佐助 + 各恰好一个。"""
    if not isinstance(text, str) or not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    head = lines[0].split(" ")
    if len(head) != 3 or not all(re.fullmatch(r"0|[1-9]\d*", x) for x in head):
        return False
    m, n, t = map(int, head)
    if not (0 < m < 200 and 0 < n < 200 and 0 <= t < 10):
        return False
    rows = lines[1:]
    if len(rows) != m or any(not re.fullmatch(r"[@+*#]{%d}" % n, row) for row in rows):
        return False
    body = "".join(rows)
    return body.count("@") == 1 and body.count("+") == 1


def render(grid, t):
    return f"{len(grid)} {len(grid[0])} {t}\n" + "\n".join("".join(row) for row in grid) + "\n"


def place(r, grid, avoid=()):
    m, n = len(grid), len(grid[0])
    cells = [(i, j) for i in range(m) for j in range(n) if (i, j) not in avoid]
    (a, b) = r.sample(cells, 2)
    grid[a[0]][a[1]] = "@"
    grid[b[0]][b[1]] = "+"


def random_grid(r, m, n, density, t):
    grid = [["#" if r.random() < density else "*" for _ in range(n)] for _ in range(m)]
    place(r, grid)
    return render(grid, t)


def corner_grid(r, m, n, density, t):
    # @ 在左上、+ 在右下，距离最远
    grid = [["#" if r.random() < density else "*" for _ in range(n)] for _ in range(m)]
    grid[0][0] = "@"
    grid[m - 1][n - 1] = "+"
    return render(grid, t)


def snake(m, n, t, wall_holes=0, r=None):
    # 蛇形通路：奇数行是 # 墙，只在一端留缺口；可在墙上用 # 代替（需要查克拉打穿抄近路）
    grid = [["*"] * n for _ in range(m)]
    for i in range(1, m, 2):
        for j in range(n):
            grid[i][j] = "#"
        gap = n - 1 if (i // 2) % 2 == 0 else 0
        grid[i][gap] = "*"
    grid[0][0] = "@"
    last = m - 1 if (m - 1) % 2 == 0 else m - 2
    grid[last][n - 1 if (last // 2) % 2 == 1 else 0] = "+"
    return render(grid, t)


def walled_target(r, m, n, thickness, t, density=0.0):
    # + 在中央，周围 thickness 圈全是 #，其余区域随机
    grid = [["#" if r.random() < density else "*" for _ in range(n)] for _ in range(m)]
    cx, cy = m // 2, n // 2
    for i in range(m):
        for j in range(n):
            if max(abs(i - cx), abs(j - cy)) <= thickness:
                grid[i][j] = "#"
    grid[cx][cy] = "+"
    grid[0][0] = "@"
    return render(grid, t)


def trap_grid(r, m, n, t):
    """卡只记坐标的 visited：@ 出发有两条路到同一个关口，
    短路要打 t 个手下（到关口时查克拉为 0），长路全是通路（到关口时查克拉满）。
    关口之后是一段需要 t 个查克拉才能穿过的墙，再后面才是佐助。"""
    grid = [["#"] * n for _ in range(m)]
    # 第 0 行：@ 往右的短路，前 t 格是 #
    grid[0][0] = "@"
    gate = t + 1
    for j in range(1, gate):
        grid[0][j] = "#"
    grid[0][gate] = "*"
    # 长路：沿第 0 列往下到第 2 行，再往右，再往上到关口
    for i in range(1, 3):
        grid[i][0] = "*"
    for j in range(0, gate + 1):
        grid[2][j] = "*"
    grid[1][gate] = "*"
    # 关口往右：t 格 # 墙，然后一路通到 +
    for j in range(gate + 1, gate + 1 + t):
        grid[0][j] = "#"
    for j in range(gate + 1 + t, n):
        grid[0][j] = "*"
    grid[0][n - 1] = "+"
    # 下方其余区域随机填充，不影响主干
    for i in range(4, m):
        for j in range(n):
            grid[i][j] = "#" if r.random() < 0.5 else "*"
    return render(grid, t)


def build_cases():
    cases = [SAMPLE_IN, SAMPLE2_IN]
    cases.append("1 2 0\n@+\n")                     # 2 最小规模，相邻
    cases.append("2 1 0\n+\n@\n")                   # 3 单列
    cases.append("3 3 0\n@#*\n##*\n**+\n")          # 4 T=0 被墙挡住 → -1
    cases.append("1 5 3\n@###+\n")                  # 5 恰好用完查克拉
    cases.append("1 6 3\n@####+\n")                 # 6 差一个查克拉 → -1
    r = random.Random(NUMBER)
    cases.append(trap_grid(r, 12, 30, 3))           # 7 坐标 visited 陷阱（小）
    cases.append(trap_grid(r, 199, 199, 9))         # 8 坐标 visited 陷阱（满规模，T=9）
    cases.append(random_grid(r, 9, 11, 0.4, 2))     # 9 小随机
    cases.append(random_grid(r, 30, 25, 0.55, 4))   # 10 中随机，墙多
    cases.append(walled_target(r, 41, 41, 10, 9, 0.0))  # 11 10 层厚墙，T=9 也打不穿 → -1
    cases.append(walled_target(r, 41, 41, 9, 9, 0.0))   # 12 9 层墙，T=9 恰好打穿
    cases.append(snake(199, 199, 0))                # 13 满规模蛇形长路，T=0
    cases.append(snake(199, 199, 9))                # 14 蛇形 + 查克拉抄近路
    cases.append(corner_grid(r, 199, 199, 0.0, 0))  # 15 全通路，最远角
    cases.append(corner_grid(r, 199, 199, 0.35, 5))  # 16 满规模随机
    cases.append(corner_grid(r, 199, 199, 0.3, 9))  # 17 满规模，墙较多
    cases.append(random_grid(r, 199, 150, 0.4, 7))  # 18 非方阵
    cases.append(corner_grid(r, 199, 199, 0.75, 9))  # 19 墙极多，多半 -1
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
    assert solve_reference(SAMPLE2_IN).split() == SAMPLE2_OUT.split(), "参考解法跑不出样例 2 输出"
    assert len(set(cases)) == len(cases), "存在重复组"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
