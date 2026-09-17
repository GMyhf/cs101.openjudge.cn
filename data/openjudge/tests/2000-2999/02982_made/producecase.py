#!/usr/bin/env python3
"""02982 Sudoku —— 生成器、输入契约、special judge 验证与数据构建。

2026-09-17 新建。题面「If solutions is not unique, then the program may print any one of them」，
所以判法是同目录的 `checker.py`（行/列/宫都是 1..9 排列、已给数字不变），不是逐字比对。

题面契约：第一行测试组数（没给上界），每组 9 行、每行恰好 9 个十进制数字，0 表示空格。
题面没说「保证有解」，但要求打印解，这里只产有解的盘面（参考解被 checker 接受即是证明）。

`SHAPES` 按「这题会怎么错 / checker 会怎么错」排：
  · `empty`         —— 全 0 盘面，解极多；逐字比对 .out 的判法在这里必然冤判。
  · `sparse`        —— 只给 3~12 个数，解很多。
  · `unique`        —— 从满盘逐格挖空到「再挖就不唯一」的极小唯一解盘面（通常 22~28 个提示）。
  · `many`          —— 随机挖掉 45~64 格、不保唯一。
  · `deadly`        —— 先挖掉一个「致命矩形」（两行两列、跨两宫的 a b / b a），再挖到
                       恰好 2 个解：只接受其中一个的 checker 会冤判一半。
  · `full_or_one`   —— 已经填满（0 个空格）或只差 1 格：原样输出 / 只填一格。
  · `hole_unit`     —— 整行 / 整列 / 整宫挖空，再随机挖几格。
  · `top_empty`     —— 唯一解盘面，挖空时优先挖前几行：不做 MRV、从左上角顺序回溯的写法
                       分支最多，但仍受下面的朴素回溯门槛约束（不刻意卡时限）。
门槛（2026-09-17 补）：每个盘面都要让学生最常见的写法 —— 空格按行优先、逐格试 1..9 或 9..1、
扫行/列/宫判合法、不做 MRV（`naive_nodes()`）—— 升序、降序各自在 10 万个递归结点内解出，
否则重抽。第一版只卡了参考解自己的 MRV 结点数，有 6 份数据朴素回溯要 300 万结点以上，
降序写法在 20 秒 CPU 上 TLE。
  · `batch`         —— 一份里上百组各种形状混排：只解第一组、组间状态没清空的挂。
第 0 组是题面样例；构建时断言参考解输出与题面样例输出逐字相同，且被 checker 接受。
"""
from __future__ import annotations

import random
import subprocess
import sys
import tempfile
from pathlib import Path

NUMBER = 2982
HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
CHECKER = HERE / "checker.py"
INPUT_DOMAIN = ("The input data will start with the number of the test cases. For each test case, 9 lines follow, "
                "corresponding to the rows of the table. On each line a string of exactly 9 decimal digits is given")
SAMPLE = """1
103000509
002109400
000704000
300502006
060000050
700803004
000401000
009205800
804000107
"""
SAMPLE_OUT = """143628579
572139468
986754231
391542786
468917352
725863914
237481695
619275843
854396127
"""
SEARCH_BUDGET = 20_000
SHAPES = ("empty", "sparse", "unique", "many", "deadly", "full_or_one", "hole_unit", "top_empty", "batch")


class TooHard(Exception):
    pass


def count_solutions(grid, limit, budget=None):
    """位掩码 MRV 计数，数到 limit 为止。grid 是 81 个 int 的列表（会被原样还原）。
    budget 给出时，搜索结点超过它就抛 TooHard。"""
    rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9
    for i, v in enumerate(grid):
        if v:
            r, c = divmod(i, 9)
            bit = 1 << v
            if (rows[r] | cols[c] | boxes[r // 3 * 3 + c // 3]) & bit:
                return 0
            rows[r] |= bit; cols[c] |= bit; boxes[r // 3 * 3 + c // 3] |= bit
    empty = [i for i in range(81) if not grid[i]]
    found = 0
    nodes = 0

    def dfs():
        nonlocal found, nodes
        nodes += 1
        if budget is not None and nodes > budget:
            raise TooHard()
        best, best_mask, best_count = -1, 0, 10
        for i in empty:
            if grid[i]:
                continue
            r, c = divmod(i, 9)
            mask = 0b1111111110 & ~(rows[r] | cols[c] | boxes[r // 3 * 3 + c // 3])
            n = bin(mask).count("1")
            if n < best_count:
                best, best_mask, best_count = i, mask, n
                if n <= 1:
                    break
        if best < 0:
            found += 1
            return found >= limit
        r, c = divmod(best, 9)
        b = r // 3 * 3 + c // 3
        while best_mask:
            bit = best_mask & -best_mask
            best_mask ^= bit
            rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit; grid[best] = bit.bit_length() - 1
            stop = dfs()
            rows[r] ^= bit; cols[c] ^= bit; boxes[b] ^= bit; grid[best] = 0
            if stop:
                return True
        return False

    dfs()
    return found


def solved_grid(r):
    """随机满盘：从空盘出发，逐格随机放一个不冲突的数，冲突则回溯（MRV 选格、候选随机序）。"""
    grid = [0] * 81
    rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9

    def dfs():
        best, best_mask, best_count = -1, 0, 10
        for i in range(81):
            if grid[i]:
                continue
            row, col = divmod(i, 9)
            mask = 0b1111111110 & ~(rows[row] | cols[col] | boxes[row // 3 * 3 + col // 3])
            n = bin(mask).count("1")
            if n < best_count:
                best, best_mask, best_count = i, mask, n
        if best < 0:
            return True
        row, col = divmod(best, 9)
        b = row // 3 * 3 + col // 3
        digits = [d for d in range(1, 10) if best_mask >> d & 1]
        r.shuffle(digits)
        for d in digits:
            bit = 1 << d
            rows[row] |= bit; cols[col] |= bit; boxes[b] |= bit; grid[best] = d
            if dfs():
                return True
            rows[row] ^= bit; cols[col] ^= bit; boxes[b] ^= bit; grid[best] = 0
        return False

    dfs()
    return grid


def minimize(r, grid, keep_count, order=None):
    """按 order 逐格尝试挖空，保持解数 == keep_count。"""
    cells = order if order is not None else r.sample(range(81), 81)
    for i in cells:
        if not grid[i]:
            continue
        v = grid[i]; grid[i] = 0
        if count_solutions(grid, keep_count + 1) != keep_count:
            grid[i] = v
    return grid


def deadly_puzzle(r):
    while True:
        g = solved_grid(r)
        cands = []
        for r1 in range(9):
            for r2 in range(r1 + 1, 9):
                if r1 // 3 != r2 // 3:
                    continue
                for c1 in range(9):
                    for c2 in range(c1 + 1, 9):
                        if c1 // 3 == c2 // 3:
                            continue
                        a, b = g[r1 * 9 + c1], g[r1 * 9 + c2]
                        if g[r2 * 9 + c1] == b and g[r2 * 9 + c2] == a:
                            cands.append((r1, r2, c1, c2))
        if cands:
            break
    r1, r2, c1, c2 = r.choice(cands)
    for i in (r1 * 9 + c1, r1 * 9 + c2, r2 * 9 + c1, r2 * 9 + c2):
        g[i] = 0
    return minimize(r, g, 2)


NAIVE_BUDGET = 100_000


def naive_nodes(grid, descending, budget=NAIVE_BUDGET):
    """学生最常见的写法：空格按行优先排好，逐格试 1..9（或 9..1），扫行/列/宫判合法，不做 MRV。
    返回递归调用次数（每次调用 solve(i) 记一个结点）；超过 budget 返回 None。"""
    rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9
    for i, v in enumerate(grid):
        if v:
            rr, cc = divmod(i, 9)
            rows[rr] |= 1 << v; cols[cc] |= 1 << v; boxes[rr // 3 * 3 + cc // 3] |= 1 << v
    empty = [(i // 9, i % 9, i // 9 // 3 * 3 + i % 9 // 3) for i in range(81) if not grid[i]]
    digits = range(9, 0, -1) if descending else range(1, 10)
    nodes = 0

    def solve(k):
        nonlocal nodes
        nodes += 1
        if nodes > budget:
            raise TooHard()
        if k == len(empty):
            return True
        rr, cc, bb = empty[k]
        used = rows[rr] | cols[cc] | boxes[bb]
        for v in digits:
            bit = 1 << v
            if not used & bit:
                rows[rr] |= bit; cols[cc] |= bit; boxes[bb] |= bit
                found = solve(k + 1)
                rows[rr] ^= bit; cols[cc] ^= bit; boxes[bb] ^= bit
                if found:
                    return True
        return False

    try:
        if not solve(0):
            return None
    except TooHard:
        return None
    return nodes


def puzzle(r, shape):
    """按形状出一个盘面；参考解同款搜索（MRV）超过 SEARCH_BUDGET 个结点、或朴素行优先回溯
    升序/降序任一超过 NAIVE_BUDGET 个结点的重抽 —— 随机挖空常挖出对朴素回溯极不友好的盘面，
    题面与原题数据都没有这种刻意卡时限的意图。"""
    while True:
        g = _puzzle(r, shape)
        try:
            count_solutions(list(g), 1, SEARCH_BUDGET)
        except TooHard:
            continue
        if naive_nodes(g, False) is None or naive_nodes(g, True) is None:
            continue
        return g


def _puzzle(r, shape):
    if shape == "empty":
        return [0] * 81
    g = solved_grid(r)
    if shape == "sparse":
        keep = set(r.sample(range(81), r.randint(3, 12)))
        return [g[i] if i in keep else 0 for i in range(81)]
    if shape == "unique":
        return minimize(r, g, 1)
    if shape == "many":
        for i in r.sample(range(81), r.randint(45, 64)):
            g[i] = 0
        return g
    if shape == "deadly":
        return deadly_puzzle(r)
    if shape == "full_or_one":
        if r.random() < 0.5:
            g[r.randrange(81)] = 0
        return g
    if shape == "hole_unit":
        kind, k = r.randrange(3), r.randrange(9)
        for i in range(81):
            row, col = divmod(i, 9)
            if (kind == 0 and row == k) or (kind == 1 and col == k) or (kind == 2 and row // 3 * 3 + col // 3 == k):
                g[i] = 0
        for i in r.sample(range(81), r.randint(0, 20)):
            g[i] = 0
        return g
    if shape == "top_empty":
        order = list(range(27)); r.shuffle(order)
        rest = list(range(27, 81)); r.shuffle(rest)
        return minimize(r, g, 1, order + rest)
    raise KeyError(shape)


def fmt(puzzles):
    return f"{len(puzzles)}\n" + "".join("".join(map(str, p[k * 9:k * 9 + 9])) + "\n" for p in puzzles for k in range(9))


def generate(number, seed):
    assert number == NUMBER
    r = random.Random(number * 1_000_003 + seed)
    plan = {
        1: ["empty"],
        2: ["sparse"] * 6,
        3: ["unique"] * 5,
        4: ["unique"] * 12,
        5: ["many"] * 8,
        6: ["many", "sparse", "empty"] * 4,
        7: ["deadly"] * 6,
        8: ["deadly", "unique"] * 5,
        9: ["full_or_one"] * 10,
        10: ["hole_unit"] * 9,
        11: ["top_empty"] * 6,
        12: ["top_empty", "unique", "deadly"] * 4,
        13: ["empty", "full_or_one", "empty"],
        14: ["hole_unit", "many"] * 7,
    }
    if seed in plan:
        shapes = plan[seed]
    elif seed <= 17:  # batch：几十到上百组混排
        pool = ("sparse", "many", "full_or_one", "hole_unit", "empty", "unique", "deadly")
        shapes = [r.choice(pool) for _ in range(r.randint(40, 100))]
    else:
        pool = SHAPES[:-1]
        shapes = [pool[(seed + i) % len(pool)] for i in range(r.randint(8, 20))]
    return fmt([puzzle(r, s) for s in shapes])


def valid(number, text):
    if not text.endswith("\n") or "\r" in text:
        return False
    lines = text.split("\n")[:-1]
    if not lines or not lines[0].isdigit():
        return False
    t = int(lines[0])
    if t < 1 or len(lines) != 1 + 9 * t:
        return False
    for k in range(t):
        rows = lines[1 + 9 * k:10 + 9 * k]
        if not all(len(x) == 9 and x.isdigit() and x.isascii() for x in rows):
            return False
        if count_solutions([int(ch) for x in rows for ch in x], 1) != 1:   # 有解（且已给数字不冲突）
            return False
    return True


def check(case, output, answer):
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for name, data in (("in", case), ("out", output), ("ans", answer)):
            p = Path(tmp) / name
            p.write_text(data, encoding="utf-8")
            paths.append(str(p))
        res = subprocess.run([sys.executable, "-I", str(CHECKER), *paths], capture_output=True, text=True, timeout=30)
    if res.returncode not in (0, 42):
        raise SystemExit(f"checker 崩溃：{res.stderr[-500:]}")
    return res.returncode == 0, res.stdout.strip()


def _build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    for path in out.glob("*"):
        path.unlink()
    cases = [SAMPLE] + [generate(NUMBER, seed) for seed in range(1, 21)]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    for index, case in enumerate(cases):
        if not valid(NUMBER, case):
            raise SystemExit(f"case {index} violates the input contract")
        result = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, timeout=120, check=True)
        if index == 0:
            if result.stdout != SAMPLE_OUT:
                raise SystemExit(f"第 0 组与题面样例输出不符：{result.stdout!r}")
            ok, message = check(case, SAMPLE_OUT, SAMPLE_OUT)
            if not ok:
                raise SystemExit(f"checker 不接受题面样例输出：{message}")
        ok, message = check(case, result.stdout, result.stdout)
        if not ok:
            raise SystemExit(f"case {index}: checker 不接受参考解输出：{message}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    _build()
