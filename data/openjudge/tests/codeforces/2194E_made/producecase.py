#!/usr/bin/env python3
"""Codeforces 2194E The Turtle Strikes Back -- generator, input contract, oracle and data build.

Written for this repository as a hand-off artifact; no external license.

Statement: t (1..1e4) tests; each "n m" (1 <= n, m <= 1e6, n*m <= 1e6), then n rows of m ints
in [-1e9, 1e9], at least one value non-negative; sum n*m <= 1e6.  Raphael negates exactly one
cell, Michelangelo then takes the max right/down path (1,1)->(n,m); print the min he can get.

The reference is C++ (samplecode.cpp, compiled with g++ -O2 during build): Python needs several
seconds for n*m = 1e6.

Shapes (how solutions go wrong):
  * tiny_multi   -- t=1e4 random tiny grids (all oracle-checked).
  * lines        -- 1xk / kx1 grids: every anti-diagonal has ONE cell, so "best path avoiding
                    the cell" must be -inf, not 0 (kills a 0-initialised top-2).
  * one_nonneg   -- everything negative except one cell (guarantee edge), including zeros; 1x1.
  * ties         -- 0/1 grids with many equal-value optimal paths (top-2 must allow t1 == t2).
  * overflow     -- |a| = 1e9 so path sums leave 32-bit range.
  * self_diag    -- using the diagonal max including the cell itself is wrong.
  * upper bound  -- 1000x1000, 1x1e6, 1e6x1 (single digits to keep .in <= 3 MB),
                    500x500 and 2x100000 with full-range values, t=1e4 x 100 cells.
Oracle: literal brute force -- try every cell, negate it, run the O(nm) max-path DP; used on every
test with n*m <= ORACLE_CELLS.
"""
from __future__ import annotations
import random
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "samplecode.cpp"
SAMPLE = "2\n3 3\n1 -2 3\n4 -5 2\n1 6 -1\n2 4\n-1 -1 -1 1\n-1 -1 -1 -1\n"
SAMPLE_OUT = "3\n-5\n"
LIM = 10 ** 9
ORACLE_CELLS = 40


def grid_text(g):
    return f"{len(g)} {len(g[0])}\n" + "".join(" ".join(map(str, row)) + "\n" for row in g)


def fix_nonneg(r, g):
    if not any(x >= 0 for row in g for x in row):
        i = r.randrange(len(g)); j = r.randrange(len(g[0])); g[i][j] = abs(g[i][j])
    return g


def rand_grid(r, n, m, lo, hi):
    return fix_nonneg(r, [[r.randint(lo, hi) for _ in range(m)] for _ in range(n)])


def one_nonneg(r, n, m, lo=-LIM, hi=-1):
    g = [[r.randint(lo, hi) for _ in range(m)] for _ in range(n)]
    g[r.randrange(n)][r.randrange(m)] = r.choice([0, r.randint(0, LIM)])
    return g


def self_diag(r, n, m):
    # one dominant "highway" path of big values; everything else modest.
    g = [[r.randint(-20, 20) for _ in range(m)] for _ in range(n)]
    i = j = 0
    while True:
        g[i][j] = r.randint(50, 100)
        if i == n - 1 and j == m - 1:
            break
        if i == n - 1 or (j < m - 1 and r.random() < 0.5): j += 1
        else: i += 1
    return fix_nonneg(r, g)


def pack(grids):
    return f"{len(grids)}\n" + "".join(map(grid_text, grids))


def dims(r, cells):
    n = r.randint(1, cells); m = r.randint(1, max(1, cells // n))
    return n, m


def generate(seed):
    r = random.Random(2194_0005 * 1000 + seed)
    if seed == 1:   # t=1e4 tiny random
        return pack([rand_grid(r, *dims(r, 12), -10, 10) for _ in range(10000)])
    if seed == 2:   # 1x1 single test
        return pack([[[0]]])
    if seed == 3:   # lines 1xk / kx1 with negatives
        gs = []
        for _ in range(3000):
            k = r.randint(1, 30); lo = r.choice([-10, -LIM]); hi = -lo
            g = rand_grid(r, 1, k, lo, hi)
            gs.append(g if r.random() < 0.5 else [[x] for x in g[0]])
        return pack(gs)
    if seed == 4:   # exactly one non-negative cell, small
        return pack([one_nonneg(r, *dims(r, ORACLE_CELLS)) for _ in range(3000)])
    if seed == 5:   # ties: 0/1 grids and constant grids
        gs = []
        for i in range(3000):
            n, m = dims(r, ORACLE_CELLS)
            gs.append(rand_grid(r, n, m, 0, 1) if i % 3 else [[r.choice([0, 1, 7])] * m for _ in range(n)])
        return pack(gs)
    if seed == 6:   # overflow-sized values, small grids
        gs = []
        for _ in range(2000):
            n, m = dims(r, ORACLE_CELLS)
            gs.append(rand_grid(r, n, m, LIM - 10, LIM) if r.random() < 0.4 else rand_grid(r, n, m, -LIM, LIM))
        return pack(gs)
    if seed == 7:   # highway grids (self-diagonal / greedy traps), small
        return pack([self_diag(r, *dims(r, ORACLE_CELLS)) for _ in range(2500)])
    if seed == 8:   # hand-made
        return pack([[[5]], [[-3, 0]], [[0], [-1]], [[1, 1], [1, 1]], [[LIM] * 6],
                     [[-LIM, LIM], [LIM, -LIM]], [[3, -1, -1], [-1, 3, -1], [-1, -1, 3]]]
                    + [rand_grid(r, 5, 8, -3, 3) for _ in range(500)])
    if seed == 9:   # medium 20x20-ish grids, oracle on small ones only
        return pack([rand_grid(r, r.randint(1, 30), r.randint(1, 30), -100, 100) for _ in range(300)])
    if seed == 10:  # 1000 x 1000 digits
        return pack([rand_grid(r, 1000, 1000, 0, 9)])
    if seed == 11:  # 1 x 1e6 with negatives (single digits)
        return pack([rand_grid(r, 1, 10 ** 6, -9, 9)])
    if seed == 12:  # 1e6 x 1
        return pack([[[r.randint(0, 9)] for _ in range(10 ** 6)]])
    if seed == 13:  # 500 x 500 full range
        return pack([rand_grid(r, 500, 500, -LIM, LIM)])
    if seed == 14:  # 2 x 100000 near-max values (overflow), plus a column
        return pack([rand_grid(r, 2, 100000, LIM // 2, LIM), [[LIM] for _ in range(50000)]])
    if seed == 15:  # t = 1e4, 100 cells each
        gs = []
        for _ in range(10000):
            n = r.choice([1, 2, 4, 5, 10, 20, 25, 50, 100]); gs.append(rand_grid(r, n, 100 // n, -9, 9))
        return pack(gs)
    if seed == 16:  # large highway grid
        return pack([self_diag(r, 700, 700)])
    if seed == 17:  # large mostly negative, one non-negative
        return pack([one_nonneg(r, 300, 1000, -9, -1), one_nonneg(r, 1, 1, -9, -1)])
    if seed == 18:  # large 0/1 grid (ties)
        return pack([rand_grid(r, 1000, 1000, 0, 1)])
    if seed == 19:  # wide rectangle with big values
        return pack([rand_grid(r, 30, 8000, -LIM, LIM)])
    # seed 20: mixed small adversarial, t = 1e4
    gs = []
    for i in range(10000):
        k = i % 4; n, m = dims(r, 16)
        gs.append([rand_grid(r, 1, m, -LIM, LIM), one_nonneg(r, n, m), self_diag(r, n, m), rand_grid(r, n, m, 0, 2)][k])
    return pack(gs)


def valid(text):
    try:
        if not text.endswith("\n"):
            return False
        lines = text.split("\n")[:-1]; li = 0
        t = int(lines[li]); li += 1
        if not 1 <= t <= 10000 or lines[0] != str(t):
            return False
        total = 0
        for _ in range(t):
            nm = lines[li].split(); li += 1
            if len(nm) != 2:
                return False
            n, m = map(int, nm)
            if not (1 <= n <= 10 ** 6 and 1 <= m <= 10 ** 6 and n * m <= 10 ** 6):
                return False
            total += n * m; nonneg = False
            for _ in range(n):
                row = list(map(int, lines[li].split())); li += 1
                if len(row) != m or min(row) < -LIM or max(row) > LIM:
                    return False
                nonneg = nonneg or max(row) >= 0
            if not nonneg:
                return False
        return li == len(lines) and total <= 10 ** 6
    except (ValueError, IndexError):
        return False


def parse(text):
    tok = text.split(); p = 1; res = []
    for _ in range(int(tok[0])):
        n, m = int(tok[p]), int(tok[p + 1]); p += 2
        res.append((n, m, list(map(int, tok[p:p + n * m])))); p += n * m
    return res


def brute(n, m, a):
    def best(b):
        f = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                c = [f[i - 1][j]] if i else []
                if j: c.append(f[i][j - 1])
                f[i][j] = (max(c) if c else 0) + b[i * m + j]
        return f[n - 1][m - 1]
    res = None
    for k in range(n * m):
        b = a[:]; b[k] = -b[k]; v = best(b)
        res = v if res is None else min(res, v)
    return res


def build():
    out = HERE / "data"; out.mkdir(exist_ok=True)
    for f in out.glob("*"):
        f.unlink()
    tmp = Path(tempfile.mkdtemp()); exe = tmp / "ref"
    subprocess.run(["g++", "-O2", "-o", str(exe), str(SOURCE)], check=True)
    cases = [SAMPLE] + [generate(s) for s in range(1, 40)]
    if len(set(cases)) != len(cases):
        raise SystemExit("duplicate inputs")
    checked_cases = 0
    for idx, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {idx} violates the input contract")
        res = subprocess.run([str(exe)], input=case, text=True, capture_output=True, check=True, timeout=60)
        if idx == 0 and res.stdout.split() != SAMPLE_OUT.split():
            raise SystemExit(f"sample mismatch: {res.stdout!r}")
        got = res.stdout.split(); tests = parse(case)
        if len(got) != len(tests):
            raise SystemExit(f"case {idx}: wrong number of answers")
        checked = 0
        for i, (n, m, a) in enumerate(tests):
            if n * m <= ORACLE_CELLS:
                if int(got[i]) != brute(n, m, a):
                    raise SystemExit(f"case {idx} test {i}: oracle disagreement")
                checked += 1
        checked_cases += checked > 0
        print(f"case {idx}: {len(tests)} tests, {checked} oracle-checked", file=sys.stderr)
        (out / f"{idx}.in").write_text(case); (out / f"{idx}.out").write_text(res.stdout)
    exe.unlink(); tmp.rmdir()
    print(f"oracle-checked cases: {checked_cases}", file=sys.stderr)


if __name__ == "__main__":
    build()
