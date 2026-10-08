# 20741 两座孤岛最短距离：n×n 的 01 方阵，恰好 2 个四连通孤岛，求最少填几个 0 才能连通两岛。
# 题面没给 n 上限，沿用原生成器的 n<=100（总时限 60ms）。固定种子，可逐字节复现。
import random
import re
import sys
from collections import deque
from pathlib import Path

SAMPLE = "3\n110\n000\n001\n"
MAXN = 100
D4 = ((0, 1), (0, -1), (1, 0), (-1, 0))


def components(n, g):
    seen = [[False] * n for _ in range(n)]
    comps = []
    for i in range(n):
        for j in range(n):
            if g[i][j] == "1" and not seen[i][j]:
                seen[i][j] = True
                q = [(i, j)]
                for x, y in q:
                    for dx, dy in D4:
                        a, b = x + dx, y + dy
                        if 0 <= a < n and 0 <= b < n and g[a][b] == "1" and not seen[a][b]:
                            seen[a][b] = True
                            q.append((a, b))
                comps.append(q)
    return comps


def valid(text):
    lines = text.split("\n")
    if lines[-1] != "":
        return False
    lines = lines[:-1]
    if not lines or not re.fullmatch(r"[1-9][0-9]*", lines[0]):
        return False
    n = int(lines[0])
    if not 2 <= n <= MAXN or len(lines) != n + 1:
        return False
    g = lines[1:]
    if any(not re.fullmatch(r"[01]{%d}" % n, r) for r in g):
        return False
    return len(components(n, g)) == 2


def solve(text):
    """独立参考：从岛 A 多源 BFS（非递归），走到岛 B 时经过的水格数。"""
    L = text.split()
    n = int(L[0])
    g = L[1 : n + 1]
    A, B = components(n, g)
    inb = set(B)
    dist = {c: 0 for c in A}
    q = deque(A)
    while q:
        x, y = q.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and (a, b) not in dist:
                if (a, b) in inb:
                    return dist[(x, y)]
                dist[(a, b)] = dist[(x, y)] + 1
                q.append((a, b))
    raise AssertionError


def fmt(g):
    return f"{len(g)}\n" + "\n".join("".join(r) for r in g) + "\n"


def empty(n):
    return [["0"] * n for _ in range(n)]


def walk_map(r, n, frac):
    """两岛随机游走生长（原生成器思路），直到恰好 2 个岛。"""
    while True:
        g = empty(n)
        p1 = (r.randrange(n), r.randrange(n))
        p2 = (r.randrange(n), r.randrange(n))
        if abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) < 3:
            continue
        for s in (p1, p2):
            g[s[0]][s[1]] = "1"
            x, y = s
            for _ in range(r.randint(1, max(1, int(n * n * frac)))):
                dx, dy = r.choice(D4)
                if 0 <= x + dx < n and 0 <= y + dy < n:
                    x, y = x + dx, y + dy
                    g[x][y] = "1"
                else:
                    x, y = s
        if len(components(n, g)) == 2:
            return g


def blob_map(r, n, cover, gap=0):
    """两岛各自 BFS 式扩张，大块陆地，保持互不相邻。"""
    while True:
        g = empty(n)
        owner = {}
        seeds = [(r.randrange(n), r.randrange(n)) for _ in range(2)]
        if gap:
            seeds = [(r.randrange(n), r.randrange(n // 2 - gap)), (r.randrange(n), r.randrange(n // 2 + gap, n))]
        if seeds[0] == seeds[1]:
            continue
        front = [[seeds[0]], [seeds[1]]]
        for k, s in enumerate(seeds):
            owner[s] = k
        target = int(n * n * cover)
        tries = 0
        while len(owner) < target and tries < 50 * target:
            tries += 1
            k = r.randrange(2)
            x, y = r.choice(front[k])
            dx, dy = r.choice(D4)
            a, b = x + dx, y + dy
            if not (0 <= a < n and 0 <= b < n) or (a, b) in owner:
                continue
            # 不能贴到另一个岛
            if any(owner.get((a + ex, b + ey)) == 1 - k for ex, ey in D4):
                continue
            # gap>0 时两岛被一条宽 2*gap 的竖直水道隔开（各自形状仍随机）
            if gap and (b >= n // 2 - gap if k == 0 else b < n // 2 + gap):
                continue
            owner[(a, b)] = k
            front[k].append((a, b))
        for (a, b) in owner:
            g[a][b] = "1"
        if len(components(n, g)) == 2:
            return g


def corners(n):
    g = empty(n)
    g[0][0] = g[n - 1][n - 1] = "1"
    return g


def ring_inside(n):
    """岛 A 是一圈外框（内含湖），岛 B 在湖中央。"""
    g = empty(n)
    for i in range(n):
        g[0][i] = g[n - 1][i] = g[i][0] = g[i][n - 1] = "1"
    c = n // 2
    g[c][c] = "1"
    return g


def spiral(n):
    """岛 A 是螺旋长蛇（DFS 递归很深），岛 B 是螺旋中心的单格。"""
    g = empty(n)
    top, left, bot, right = 0, 0, n - 1, n - 1
    while top <= bot and left <= right:
        for j in range(left, right + 1):
            g[top][j] = "1"
        for i in range(top, bot + 1):
            g[i][right] = "1"
        if bot - top >= 2:
            for j in range(left, right + 1):
                g[bot][j] = "1"
        if right - left >= 2 and bot - top >= 4:
            for i in range(top + 2, bot + 1):
                g[i][left] = "1"
            g[top + 2][left + 1] = "1"
        top += 2; left += 2; bot -= 2; right -= 2
        if bot - top < 4 or right - left < 4:
            break
    comps = components(n, g)
    if len(comps) == 1:
        # 在中心空地找一个与蛇不相邻的格子
        cells = sorted(((i, j) for i in range(n) for j in range(n) if g[i][j] == "0"
                        and all(not (0 <= i + a < n and 0 <= j + b < n) or g[i + a][j + b] == "0" for a, b in D4)),
                       key=lambda c: abs(c[0] - n // 2) + abs(c[1] - n // 2))
        i, j = cells[0]
        g[i][j] = "1"
    return g


def combs(n):
    """两把交错的梳子：岛 A 的齿从上往下，岛 B 的齿从下往上，齿间隔 1 列水。"""
    g = empty(n)
    for j in range(n):
        g[0][j] = "1"
        g[n - 1][j] = "1"
    for j in range(0, n, 4):
        for i in range(1, n - 3):
            g[i][j] = "1"
    for j in range(2, n, 4):
        for i in range(3, n - 1):
            g[i][j] = "1"
    return g


def far_lines(n):
    """岛 A 是第 0 行整行，岛 B 是最后一行整行，答案 n-2。"""
    g = empty(n)
    g[0] = ["1"] * n
    g[n - 1] = ["1"] * n
    return g


def main():
    r = random.Random(20741)
    cases = [SAMPLE]
    cases.append(fmt([list("10"), list("01")]))            # 最小 n=2，对角，答案 1
    cases.append(fmt([list("100"), list("000"), list("001")]))  # 单格岛对角，答案 3
    cases.append(fmt(far_lines(3)))                          # 答案 1（中间一行）
    cases.append(fmt(ring_inside(7)))                        # 岛在湖中
    cases.append(fmt(corners(MAXN)))                         # 最远：答案 2n-3
    cases.append(fmt(far_lines(MAXN)))
    cases.append(fmt(ring_inside(MAXN)))
    cases.append(fmt(spiral(MAXN)))                          # 长蛇岛，递归深
    cases.append(fmt(combs(MAXN)))                           # 交错梳子，答案 1
    for n, frac in ((5, 0.2), (8, 0.15), (12, 0.1), (20, 0.1), (30, 0.08), (50, 0.05)):
        cases.append(fmt(walk_map(r, n, frac)))
    for n, cover, gap in ((40, 0.3, 0), (70, 0.3, 4), (MAXN, 0.3, 15), (MAXN, 0.6, 0), (MAXN, 0.7, 2)):
        cases.append(fmt(blob_map(r, n, cover, gap)))
    assert len(cases) == 21 and len(set(cases)) == len(cases)
    data = Path("data")
    data.mkdir(exist_ok=True)
    for i, text in enumerate(cases):
        assert valid(text), i
        (data / f"{i}.in").write_text(text)
        (data / f"{i}.out").write_text(f"{solve(text)}\n")


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
