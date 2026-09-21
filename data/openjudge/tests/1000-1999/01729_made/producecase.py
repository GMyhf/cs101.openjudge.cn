#!/usr/bin/env python3
"""01729 Jack —— 生成器、输入契约、special judge 验证与数据构建。

2026-09-17 新建。题面「If several pairs of routes are possible, any one will do」，判法是同目录的
`checker.py`：逐组模拟两条路线（合法移动、不进对方的家和学校、到校即止），重算这对路线的
最近距离，要求等于参考答案的最优值、且打印的两位小数与之相同。

题面契约：多组，每组 n（n <= 30）接 n 行 n 个字符（`. * H S h s`），以一行 0 结束；
H/S/h/s 各恰好一个；「You may assume there is at least one solution」—— 两人各自都能走到学校
（Jack 不经过 `* h s`，Jill 不经过 `* H S`）。`valid()` 逐条反查。

移动模型从题面逐句读出（checker.py 顶部有完整一段）：每分钟必须走一步、不能原地等；
到校即停在学校，距离继续按学校位置算。样例输出 `6.71` 只在「先到的人停在学校继续计距离」
时才是这对路线的最近距离（t=13 时 Jack 刚到 S、Jill 已在 s 停了 1 分钟，d²=45），
构建时对第 0 组断言这一点。

`SHAPES` 按「这题会怎么错」排：
  · `open`      —— 大空地（n 到 30），最优路线对极多；逐字比对 .out 必然冤判。
  · `tiny`      —— n=2..4，四个字母挤在一起；n=2 时整张图就是四个字母。
  · `cross`     —— H 在 s 旁、h 在 S 旁：两人必须交错而过，最优值取决于错开时机。
  · `maze`      —— 走廊迷宫 + 少量打通：路线很长（最长 250 步以上），要绕路「拖时间」。
                   题面要求每分钟都走，不能原地等；「允许原地等」的写法算出的值偏大，
                   打印的路线又没法表达等待（实测 21 份里挂 13 份）。
  · `corridor`  —— Jill 的家在一条横贯全图的走廊左端，Jack 的家或学校放在走廊中间，周围随机打通：
                   忽略「H/S 对 Jill 不可通行」的写法会穿过去（实测这类错解 21 份里挂 8 份）。
  · `blobs`     —— 大块 `*` 障碍，随机密度。
  · `symmetric` —— 左右/中心对称地图，许多对称的等价最优解（并列）。
每份 1..8 组混排；n=30 的组放在后面几份。

参考值用两套独立实现核对：samplecode.py（位集二分 + 分层 BFS 倒推），以及这里的
`_oracle_upper()`：显式状态 BFS 证明「最优值的下一个可能距离」不可达；
下界由 checker 模拟参考路线得到（checker 接受即说明这对路线达到了最优值）。
"""
from __future__ import annotations

import random
import subprocess
import sys
import tempfile
from collections import deque
from pathlib import Path

NUMBER = 1729
HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
CHECKER = HERE / "checker.py"
INPUT_DOMAIN = "an n by n square grid (n <= 30) ... A line containing 0 follows the last case. You may assume there is at least one solution."
SAMPLE = """10
..........
...H......
.**...s...
.**.......
.**.......
.**.......
.**.......
.**.......
...S..h..*
..........
0
"""
SAMPLE_OUT = "6.71\nWWWSSSSSSSEEE\nNEEENNNNNWWW\n"
SHAPES = ("open", "tiny", "cross", "maze", "corridor", "blobs", "symmetric")
MAX_N = 30


def _reach(grid, n, start, goal, forbidden):
    seen = {start}
    q = deque([start])
    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            return True
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen and grid[nr][nc] != "*" and grid[nr][nc] not in forbidden:
                seen.add((nr, nc)); q.append((nr, nc))
    return False


def solvable(grid, n):
    where = {grid[r][c]: (r, c) for r in range(n) for c in range(n)}
    return (_reach(grid, n, where["H"], where["S"], "hs") and _reach(grid, n, where["h"], where["s"], "HS"))


def _place(r, grid, n, letters, cells=None):
    free = cells if cells is not None else [(i, j) for i in range(n) for j in range(n) if grid[i][j] == "."]
    for ch, (i, j) in zip(letters, r.sample(free, len(letters))):
        grid[i][j] = ch


def _maze(r, n):
    grid = [["*"] * n for _ in range(n)]
    start = (r.randrange(0, n, 2), r.randrange(0, n, 2))
    grid[start[0]][start[1]] = "."
    stack = [start]
    while stack:
        i, j = stack[-1]
        opts = [(i + di, j + dj, i + di // 2, j + dj // 2) for di, dj in ((2, 0), (-2, 0), (0, 2), (0, -2))
                if 0 <= i + di < n and 0 <= j + dj < n and grid[i + di][j + dj] == "*"]
        if not opts:
            stack.pop(); continue
        a, b, x, y = r.choice(opts)
        grid[x][y] = grid[a][b] = "."
        stack.append((a, b))
    for _ in range(r.randint(0, n)):
        grid[r.randrange(n)][r.randrange(n)] = "."
    return grid


def _map(r, shape):
    while True:
        if shape == "tiny":
            n = r.randint(2, 4)
            grid = [["*" if r.random() < 0.15 else "." for _ in range(n)] for _ in range(n)]
            cells = [(i, j) for i in range(n) for j in range(n)]
            _place(r, grid, n, "HShs", cells)
        elif shape == "open":
            n = r.randint(20, MAX_N)
            grid = [["*" if r.random() < 0.05 else "." for _ in range(n)] for _ in range(n)]
            _place(r, grid, n, "HShs")
        elif shape == "blobs":
            n = r.randint(8, MAX_N)
            grid = [["."] * n for _ in range(n)]
            for _ in range(r.randint(2, 8)):
                i0, j0 = r.randrange(n), r.randrange(n)
                h, w = r.randint(1, n // 2), r.randint(1, n // 2)
                for i in range(i0, min(n, i0 + h)):
                    for j in range(j0, min(n, j0 + w)):
                        grid[i][j] = "*"
            _place(r, grid, n, "HShs")
        elif shape == "cross":
            n = r.randint(5, MAX_N)
            grid = [["*" if r.random() < 0.1 else "." for _ in range(n)] for _ in range(n)]
            a = (r.randrange(n), r.randrange(n // 3 + 1))
            b = (r.randrange(n), n - 1 - r.randrange(n // 3 + 1))
            spots = {}
            for ch, (i, j) in (("H", a), ("h", b)):
                spots[ch] = (i, j)
            ok = spots["H"] != spots["h"]
            if not ok:
                continue
            grid[a[0]][a[1]] = "H"; grid[b[0]][b[1]] = "h"
            near = lambda p: [(p[0] + di, p[1] + dj) for di in (-1, 0, 1) for dj in (-2, -1, 0, 1, 2)
                              if 0 <= p[0] + di < n and 0 <= p[1] + dj < n and grid[p[0] + di][p[1] + dj] in ".*"]
            ns, nS = near(a), near(b)
            if not ns or not nS:
                continue
            i, j = r.choice(ns); grid[i][j] = "s"
            nS = [p for p in near(b) if grid[p[0]][p[1]] in ".*"]
            if not nS:
                continue
            i, j = r.choice(nS); grid[i][j] = "S"
        elif shape == "maze":
            n = r.randint(9, MAX_N)
            grid = _maze(r, n)
            _place(r, grid, n, "HShs")
        elif shape == "corridor":
            n = r.randint(6, MAX_N)
            grid = [["*"] * n for _ in range(n)]
            row = r.randrange(1, n - 1)
            for j in range(n):
                grid[row][j] = "."
            for i in range(n):
                if r.random() < 0.6:
                    grid[i][r.randrange(n)] = "."
            for i in range(n):          # 上下各一块空地
                for j in range(n):
                    if (i < row - 1 or i > row + 1) and r.random() < 0.55:
                        grid[i][j] = "."
            # Jill 的家在左端，Jack 的家/学校卡在走廊中间
            grid[row][0] = "h"
            grid[row][n - 1] = "s" if r.random() < 0.5 else "."
            mid = r.randrange(1, n - 1)
            grid[row][mid] = r.choice("HS")
            other = "S" if grid[row][mid] == "H" else "H"
            _place(r, grid, n, other + ("" if grid[row][n - 1] == "s" else "s"))
        elif shape == "symmetric":
            n = r.randint(6, MAX_N)
            half = [["*" if r.random() < 0.12 else "." for _ in range((n + 1) // 2)] for _ in range(n)]
            grid = [row_[:] + row_[:n // 2][::-1] for row_ in half]
            i, j = r.randrange(n), r.randrange(n // 2)
            k, l = r.randrange(n), r.randrange(n // 2)
            if (i, j) == (k, l):
                continue
            grid[i][j], grid[i][n - 1 - j] = "H", "h"
            grid[k][l], grid[k][n - 1 - l] = "S", "s"
        else:
            raise KeyError(shape)
        text = ["".join(row_) for row_ in grid]
        if all(sum(x.count(ch) for x in text) == 1 for ch in "HShs") and solvable(text, n):
            return n, text


def generate(number, seed):
    assert number == NUMBER
    r = random.Random(number * 1_000_003 + seed)
    if seed <= 14:
        shape = SHAPES[(seed - 1) % len(SHAPES)]
        count = r.randint(1, 8) if shape in ("tiny", "cross", "corridor", "symmetric") else r.randint(1, 4)
        maps = [_map(r, shape) for _ in range(count)]
    elif seed <= 17:
        maps = [_map(r, r.choice(SHAPES)) for _ in range(8)]
    else:  # 大图压一下
        maps = [_map(r, s) for s in ("open", "maze", "blobs")]
        maps = [m for m in maps] + [_map(r, "symmetric") for _ in range(seed - 17)]
    return "".join(f"{n}\n" + "".join(x + "\n" for x in rows) for n, rows in maps) + "0\n"


def parse(text):
    lines = text.split("\n")
    p, cases = 0, []
    while True:
        n = int(lines[p]); p += 1
        if n == 0:
            return cases, lines[p:]
        cases.append((n, lines[p:p + n])); p += n


def valid(number, text):
    if not text.endswith("\n") or "\r" in text:
        return False
    try:
        cases, rest = parse(text)
    except (ValueError, IndexError):
        return False
    if rest != [""] or not cases:
        return False
    for n, rows in cases:
        if not (2 <= n <= MAX_N) or len(rows) != n:
            return False
        if any(len(x) != n or set(x) - set(".*HShs") for x in rows):
            return False
        if any(sum(x.count(ch) for x in rows) != 1 for ch in "HShs"):
            return False
        if not solvable(rows, n):
            return False
    return True


def _oracle_upper(n, rows, thr):
    """显式状态 BFS：只走 d² >= thr 的状态，能否从 (H,h) 到 (S,s)。与 samplecode 的位集写法独立。"""
    where = {rows[r][c]: (r, c) for r in range(n) for c in range(n)}
    H, S, h, s = where["H"], where["S"], where["h"], where["s"]

    def moves(p, goal, forbidden):
        if p == goal:
            return [p]
        out = []
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (p[0] + dr, p[1] + dc)
            if 0 <= q[0] < n and 0 <= q[1] < n and rows[q[0]][q[1]] != "*" and rows[q[0]][q[1]] not in forbidden:
                out.append(q)
        return out

    def ok(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 >= thr

    if not ok(H, h):
        return False
    jack_moves = {}
    jill_moves = {}
    start = (H, h)
    seen = {start}
    q = deque([start])
    while q:
        a, b = q.popleft()
        if a == S and b == s:
            return True
        ma = jack_moves.get(a)
        if ma is None:
            ma = jack_moves[a] = moves(a, S, "hs")
        mb = jill_moves.get(b)
        if mb is None:
            mb = jill_moves[b] = moves(b, s, "HS")
        for a2 in ma:
            for b2 in mb:
                st = (a2, b2)
                if st not in seen and ok(a2, b2):
                    seen.add(st); q.append(st)
    return False


def check(case, output, answer):
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for name, data in (("in", case), ("out", output), ("ans", answer)):
            p = Path(tmp) / name
            p.write_text(data, encoding="utf-8")
            paths.append(str(p))
        res = subprocess.run([sys.executable, "-I", str(CHECKER), *paths], capture_output=True, text=True, timeout=60)
    if res.returncode not in (0, 42):
        raise SystemExit(f"checker 出错（退出码 {res.returncode}）：{res.stdout}{res.stderr[-500:]}")
    return res.returncode == 0, res.stdout.strip()


def _build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    for path in out.glob("*"):
        path.unlink()
    cases = [SAMPLE] + [generate(NUMBER, seed) for seed in range(1, 40)]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    for index, case in enumerate(cases):
        if not valid(NUMBER, case):
            raise SystemExit(f"case {index} violates the input contract")
        result = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, timeout=120, check=True)
        if index == 0:
            if result.stdout.split()[0] != SAMPLE_OUT.split()[0]:
                raise SystemExit(f"第 0 组最优值与题面样例不符：{result.stdout!r}")
            ok, message = check(case, SAMPLE_OUT, result.stdout)
            if not ok:
                raise SystemExit(f"checker 不接受题面样例输出：{message}")
        ok, message = check(case, result.stdout, result.stdout)
        if not ok:
            raise SystemExit(f"case {index}: checker 不接受参考解输出：{message}")
        values = result.stdout.split()[0::3]
        for (n, rows), value in zip(parse(case)[0], values):
            d2 = round(float(value) ** 2)
            nxt = min(v for v in (dr * dr + dc * dc for dr in range(n) for dc in range(n)) if v > d2) \
                if d2 < 2 * (n - 1) ** 2 else None
            if nxt is not None and _oracle_upper(n, rows, nxt):
                raise SystemExit(f"case {index}: 最优值 {value} 不是最大 —— d²>={nxt} 也可达")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    _build()
