"""12029 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
第 20 组起为针对性大规模/边界数据（见 designed_cases）。
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 12029
SAMPLE_IN = '1\n5 5\n1 1 1 1 1\n1 0 0 0 1\n1 0 1 0 1\n1 0 0 0 1\n1 1 1 1 1\n3 3\n2\n1 1\n2 2\n'
SAMPLE_OUT = 'No\n'
REFERENCE_SOURCE = 'from collections import deque\nimport sys\ninput = sys.stdin.read\n\n# 判断坐标是否有效\ndef is_valid(x, y, m, n):\n    return 0 <= x < m and 0 <= y < n\n\n# 广度优先搜索模拟水流\ndef bfs(start_x, start_y, start_height, m, n, h, water_height):\n    dx = [-1, 1, 0, 0]\n    dy = [0, 0, -1, 1]\n    q = deque([(start_x, start_y, start_height)])\n    water_height[start_x][start_y] = start_height\n\n    while q:\n        x, y, height = q.popleft()\n        for i in range(4):\n            nx, ny = x + dx[i], y + dy[i]\n            if is_valid(nx, ny, m, n) and h[nx][ny] < height:\n                if water_height[nx][ny] < height:\n                    water_height[nx][ny] = height\n                    q.append((nx, ny, height))\n\n# 主函数\ndef main():\n    data = input().split()  # 快速读取所有输入数据\n    idx = 0\n    k = int(data[idx])\n    idx += 1\n    results = []\n\n    for _ in range(k):\n        m, n = map(int, data[idx:idx + 2])\n        idx += 2\n        h = []\n        for i in range(m):\n            h.append(list(map(int, data[idx:idx + n])))\n            idx += n\n        water_height = [[0] * n for _ in range(m)]\n\n        i, j = map(int, data[idx:idx + 2])\n        idx += 2\n        i, j = i - 1, j - 1\n\n        p = int(data[idx])\n        idx += 1\n\n        for _ in range(p):\n            x, y = map(int, data[idx:idx + 2])\n            idx += 2\n            x, y = x - 1, y - 1\n\n            bfs(x, y, h[x][y], m, n, h, water_height)\n\n        results.append("Yes" if water_height[i][j] > 0 else "No")\n\n    sys.stdout.write("\\n".join(results) + "\\n")\n\nif __name__ == "__main__":\n    main()\n'

def g12029(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        m, n = r.randint(3, 8), r.randint(3, 8); grid = [[r.randint(0, 100) for _ in range(n)] for _ in range(m)]
        i, j = r.randint(1, m), r.randint(1, n); points = [(r.randint(1, m), r.randint(1, n)) for _ in range(r.randint(1, min(5, m*n)))]
        cases.append(f"{m} {n}\n" + "\n".join(" ".join(map(str, row)) for row in grid) + f"\n{i} {j}\n{len(points)}\n" + "\n".join(f"{x} {y}" for x, y in points))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"

def valid(text):
    """题面输入契约：K 组；每组 M N (0<M,N<=200)，M 行各 N 个高度 (0<=H<=1000)，
    I J (0<I<=M, 0<J<=N)，P (0<P<=M*N)，P 行 X Y (0<X<=M, 0<Y<=N)。逐行核对 token 数。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def ints(line, cnt):
        t = line.split()
        if len(t) != cnt or not all(x.isdigit() for x in t):
            return None
        return list(map(int, t))
    pos = 0
    def take(cnt):
        nonlocal pos
        if pos >= len(lines):
            return None
        v = ints(lines[pos], cnt)
        pos += 1
        return v
    k = take(1)
    if not k or k[0] < 1:
        return False
    for _ in range(k[0]):
        mn = take(2)
        if not mn:
            return False
        m, n = mn
        if not (0 < m <= 200 and 0 < n <= 200):
            return False
        for _ in range(m):
            row = take(n)
            if row is None or not all(0 <= h <= 1000 for h in row):
                return False
        ij = take(2)
        if not ij or not (0 < ij[0] <= m and 0 < ij[1] <= n):
            return False
        pc = take(1)
        if not pc or not (0 < pc[0] <= m * n):
            return False
        for _ in range(pc[0]):
            xy = take(2)
            if not xy or not (0 < xy[0] <= m and 0 < xy[1] <= n):
                return False
    return pos == len(lines)


def fmt_group(grid, hq, points):
    m, n = len(grid), len(grid[0])
    return (f"{m} {n}\n" + "\n".join(" ".join(map(str, row)) for row in grid)
            + f"\n{hq[0]} {hq[1]}\n{len(points)}\n" + "\n".join(f"{x} {y}" for x, y in points))


def fmt_case(groups):
    return str(len(groups)) + "\n" + "\n".join(fmt_group(*g) for g in groups) + "\n"


def g_tiny_edges(r):
    """1x1、1xN、Mx1 等最小/退化形状；司令部即放水点（高度>0）也在内。"""
    gs = []
    gs.append(([[5]], (1, 1), [(1, 1)]))                      # 司令部就是放水点 -> Yes
    gs.append(([[3, 7]], (1, 1), [(1, 2)]))                   # 低处被淹 -> Yes
    gs.append(([[7, 3]], (1, 1), [(1, 2)]))                   # 高处不淹 -> No
    gs.append(([[4], [4]], (2, 1), [(1, 1)]))                 # 等高不流 -> No
    gs.append(([[1000], [999], [0]], (3, 1), [(1, 1)]))       # H 上下界
    gs.append(([[0, 0, 0]], (1, 3), [(1, 1)]))                # 放水点高度 0 -> No
    gs.append(([[5, 9, 1]], (1, 3), [(1, 1), (1, 1)]))        # 重复放水点、被高墙挡住 -> No
    row = [r.randint(0, 1000) for _ in range(200)]
    gs.append(([row], (1, r.randint(1, 200)), [(1, r.randint(1, 200)) for _ in range(3)]))
    col = [[r.randint(0, 1000)] for _ in range(200)]
    gs.append((col, (r.randint(1, 200), 1), [(r.randint(1, 200), 1) for _ in range(3)]))
    return fmt_case(gs)


def g_flat_hq(r, m, n, yes):
    """大平原 + 一圈高墙围住司令部；墙上一个缺口决定 Yes/No。"""
    grid = [[r.randint(0, 400) for _ in range(n)] for _ in range(m)]
    ci, cj = m // 2, n // 2
    for i in range(ci - 5, ci + 6):
        for j in range(cj - 5, cj + 6):
            if max(abs(i - ci), abs(j - cj)) == 5:
                grid[i][j] = 1000
    if yes:
        grid[ci - 5][cj] = 300
    grid[ci][cj] = 200
    src = (1, 1)
    grid[0][0] = 900
    return fmt_case([(grid, (ci + 1, cj + 1), [src])])


def g_maze(r, m, n, yes):
    """蛇形走廊：墙 1000、通道 0，放水点 999 在入口，司令部在走廊尽头；No 时末段被一格 999 堵死。"""
    grid = [[1000] * n for _ in range(m)]
    for i in range(0, m, 2):
        for j in range(n):
            grid[i][j] = r.randint(0, 5)
        if i + 2 < m:
            j = n - 1 if (i // 2) % 2 == 0 else 0
            grid[i + 1][j] = r.randint(0, 5)
    last = m - 1 if (m - 1) % 2 == 0 else m - 2
    hq_j = 0 if (last // 2) % 2 == 0 else n - 1
    hq = (last + 1, (n if hq_j == 0 else 1))
    grid[0][0] = 999
    if not yes:
        bj = n // 2
        grid[last][bj] = 999
    return fmt_case([(grid, hq, [(1, 1)])])


def g_all_sources(r, m, n, ascending, count=None):
    """大量放水点，按高度升序（或降序）列出；不做“已淹更高则跳过”剪枝的逐点 BFS 会反复淹同一片。
    count=None 即 P = M*N（取到上限）。升序组的点数控制在参考解（按输入顺序 BFS + 剪枝）能在时限一半内跑完。"""
    grid = [[r.randint(0, 1000) for _ in range(n)] for _ in range(m)]
    cells = [(i + 1, j + 1) for i in range(m) for j in range(n)]
    if count is not None:
        cells = r.sample(cells, count)
    cells.sort(key=lambda c: (grid[c[0] - 1][c[1] - 1], c), reverse=not ascending)
    hq = (r.randint(1, m), r.randint(1, n))
    return fmt_case([(grid, hq, cells)])


def g_staircase(r, m, n, yes):
    """单调递增坡：高度随曼哈顿距离增加，放水点在高处才能流下去。"""
    grid = [[min(1000, (i + j) // 2) for j in range(n)] for i in range(m)]
    hq = (1, 1)
    if yes:
        src = (m, n)
    else:
        src = (1, 1)
        grid[0][0] = 0
        hq = (m, n)
    return fmt_case([(grid, hq, [src])])


def g_many_medium(r, k, size):
    gs = []
    for t in range(k):
        m, n = r.randint(size // 2, size), r.randint(size // 2, size)
        grid = [[r.randint(0, 20) for _ in range(n)] for _ in range(m)]
        pts = [(r.randint(1, m), r.randint(1, n)) for _ in range(r.randint(1, 6))]
        gs.append((grid, (r.randint(1, m), r.randint(1, n)), pts))
    return fmt_case(gs)


COUNT_ASC = 200


def designed_cases():
    r = random.Random(NUMBER * 7)
    return [
        g_tiny_edges(r),
        g_many_medium(r, 30, 30),
        g_flat_hq(r, 200, 200, True),
        g_flat_hq(r, 200, 200, False),
        g_maze(r, 199, 200, True),
        g_maze(r, 200, 199, False),
        g_all_sources(r, 200, 200, True, COUNT_ASC),
        g_all_sources(r, 200, 200, False),
        g_staircase(r, 200, 200, True),
        g_staircase(r, 200, 200, False),
    ]


def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g12029(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    cases += designed_cases()
    assert len(set(cases)) == len(cases)
    assert all(valid(c) for c in cases), "有数据越出题面约束"
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
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
