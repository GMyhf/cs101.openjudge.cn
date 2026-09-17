#!/usr/bin/env python3
"""Codeforces 2228D Sanae, Cross and Color -- generator, input contract, oracle, build.

Written for this repository as a hand-off artifact; no external license.

Shapes target the ways solutions go wrong:
  * counting integer (k1, k2) pairs instead of distinct colorings -- coordinates with
    gaps (sparse values, points clustered at the frame x/y in {1, n});
  * off-by-one in the valid y-cut interval (inclusive R, or counting y values not cuts);
  * checking only "left/right and top/bottom non-empty" instead of all four quadrants
    (diagonals, staircases, L-shapes where the answer is 0 or small);
  * 32-bit overflow: an X shape at n = 2e5 gives (n/2 - 1)^2 ~ 1e10;
  * n = 4 minimum (every 4-subset of the 4x4 grid, exhaustively), t = 1e4 small tests,
    all points on one column/row, only two distinct x or y values.
The largest n is 2e5 (not the statement's 2e6) to keep each .in under ~3 MB.
Oracle: for every integer k1, k2 in 0..n build the literal coloring tuple, keep those
using all four colors, and count distinct tuples.  Run on every test with n <= ORACLE_N;
a case counts as oracle-checked only if all of its tests are.
"""
from __future__ import annotations
import itertools
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
SAMPLE = """5
4
1 1
2 2
3 3
4 4
4
1 4
4 1
1 1
4 4
8
7 2
5 7
2 7
1 3
6 7
3 6
7 5
1 6
8
6 1
3 6
1 4
1 1
4 2
5 5
3 4
4 1
6
5 5
5 4
3 5
1 5
5 3
2 2
"""
SAMPLE_OUT = "0\n1\n12\n8\n4\n"
MAXN_STATEMENT = 2000000
BIG = 200000
ORACLE_N = 30


def fmt(tests):
    out = [str(len(tests))]
    for pts in tests:
        out.append(str(len(pts)))
        out.extend(f"{x} {y}" for x, y in pts)
    return "\n".join(out) + "\n"


def rand_points(r, n, xr=None, yr=None):
    """n distinct points with x in xr, y in yr (defaults 1..n); requires capacity."""
    xs = xr or (1, n); ys = yr or (1, n)
    seen = set()
    while len(seen) < n:
        seen.add((r.randint(*xs), r.randint(*ys)))
    pts = list(seen); r.shuffle(pts)
    return pts


def perm_points(r, n):
    p = list(range(1, n + 1)); r.shuffle(p)
    pts = [(i + 1, p[i]) for i in range(n)]; r.shuffle(pts)
    return pts


def x_shape(r, n):
    m = n // 2
    pts = set()
    for i in range(1, m + 1):
        pts.add((i, i)); pts.add((i, m + 1 - i))
    extra = n - len(pts)
    while extra > 0:
        q = (r.randint(1, n), r.randint(1, n))
        if q not in pts:
            pts.add(q); extra -= 1
    pts = list(pts); r.shuffle(pts)
    return pts


def frame(r, n):
    pts = set()
    cand = [1, 2, n - 1, n]
    while len(pts) < n:
        if r.random() < 0.5:
            pts.add((r.choice(cand), r.randint(1, n)))
        else:
            pts.add((r.randint(1, n), r.choice(cand)))
    pts = list(pts); r.shuffle(pts)
    return pts


def staircase(r, n):
    # monotone-ish chain: few valid crosses, many near-misses
    pts = set(); x = y = 1
    while len(pts) < n:
        pts.add((x, y))
        if r.random() < 0.5 and x < n:
            x += 1
        elif y < n:
            y += 1
        else:
            x = min(n, x + 1)
        if x == n and y == n:
            x, y = r.randint(1, n), r.randint(1, n)
    pts = list(pts); r.shuffle(pts)
    return pts


def small_mixed(r, count, lo, hi):
    tests = []
    for _ in range(count):
        n = r.randint(lo, hi)
        k = r.randrange(6)
        if k == 0:
            pts = rand_points(r, n)
        elif k == 1:
            pts = perm_points(r, n)
        elif k == 2:
            pts = x_shape(r, n)
        elif k == 3:
            pts = frame(r, n)
        elif k == 4:
            pts = staircase(r, n)
        else:
            c = r.randint(2, n)
            pts = rand_points(r, n, (1, max(c, 2)), (1, n)) if r.random() < 0.5 else rand_points(r, n, (1, n), (1, max(c, 2)))
        tests.append(pts)
    return tests


def generate(seed, attempt=0):
    r = random.Random(2228_0004 * 131 + seed * 104729 + attempt)
    if seed == 1:        # every 4-point set in the 4x4 grid (n = 4 minimum)
        cells = [(x, y) for x in range(1, 5) for y in range(1, 5)]
        tests = [list(c) for c in itertools.combinations(cells, 4)]
        r.shuffle(tests)
        return fmt(tests)
    if seed == 2:        # many small mixed tests, n 4..8
        return fmt(small_mixed(r, 3000, 4, 8))
    if seed == 3:        # n 9..30, mixed shapes, oracle
        return fmt(small_mixed(r, 120, 9, 30))
    if seed == 4:        # answer-0 structures + one column / one row / two columns
        tests = []
        for n in range(4, 31):
            tests.append([(i, i) for i in range(1, n + 1)])
            tests.append([(i, n + 1 - i) for i in range(1, n + 1)])
            tests.append([(1, i) for i in range(1, n + 1)])
            tests.append([(i, n) for i in range(1, n + 1)])
            tests.append(rand_points(r, n, (1, 2), (1, n)))
            tests.append(rand_points(r, n, (1, n), (n - 1, n)))
        for pts in tests:
            r.shuffle(pts)
        return fmt(tests)
    if seed == 5:        # sparse coordinates: few points in a big 1..n box, gaps everywhere
        tests = []
        for _ in range(300):
            n = r.randint(4, 30)
            base = rand_points(r, n)
            tests.append(base)
        return fmt(tests)
    if seed == 6:        # frames and staircases, small (oracle)
        tests = [frame(r, r.randint(4, 30)) for _ in range(150)] + [staircase(r, r.randint(4, 30)) for _ in range(150)]
        r.shuffle(tests)
        return fmt(tests)
    if seed == 7:        # t = 1e4 small tests
        return fmt(small_mixed(r, 10000, 4, 12))
    if seed == 8:        # X shape at max: answer ~ 1e10 (overflow)
        return fmt([x_shape(r, BIG)])
    if seed == 9:        # uniform random at max
        return fmt([rand_points(r, BIG)])
    if seed == 10:       # random permutation at max
        return fmt([perm_points(r, BIG)])
    if seed == 11:       # only 3 distinct x values
        return fmt([rand_points(r, BIG, (1, 3), (1, BIG))])
    if seed == 12:       # only 2 distinct y values
        return fmt([rand_points(r, BIG, (1, BIG), (BIG - 1, BIG))])
    if seed == 13:       # frame at max: many coordinate gaps
        return fmt([frame(r, BIG)])
    if seed == 14:       # staircase at max (mostly zero-width intervals)
        return fmt([staircase(r, BIG)])
    if seed == 15:       # dense 447x447 grid block
        side = 447
        pts = [(x, y) for x in range(1, side + 1) for y in range(1, side + 1)][:BIG]
        r.shuffle(pts)
        return fmt([pts])
    if seed == 16:       # X shape plus noise, several medium tests
        tests = [x_shape(r, 40000) for _ in range(5)]
        return fmt(tests)
    if seed == 17:       # clustered: points concentrated in small x-range and small y-range bands
        n = BIG
        pts = set()
        while len(pts) < n:
            if r.random() < 0.5:
                pts.add((r.randint(1, 500), r.randint(1, n)))
            else:
                pts.add((r.randint(1, n), r.randint(n - 500, n)))
        pts = list(pts); r.shuffle(pts)
        return fmt([pts])
    if seed == 18:       # medium random multi-test, n 1000..20000
        tests = []; used = 0
        while True:
            n = r.randint(1000, 20000)
            if used + n > BIG:
                break
            tests.append(small_mixed(r, 1, n, n)[0]); used += n
        return fmt(tests)
    if seed == 19:       # n = ORACLE_N exactly: X shapes and permutations
        tests = [x_shape(r, 30) for _ in range(60)] + [perm_points(r, 30) for _ in range(60)]
        r.shuffle(tests)
        return fmt(tests)
    # seed 20: t = 1e4, mixed n 4..30
    tests = small_mixed(r, 10000, 4, 30)
    return fmt(tests)


# ---------------------------------------------------------------- contract
def valid(text):
    try:
        lines = text.split("\n")
        if lines[-1] != "":
            return False
        lines = lines[:-1]
        t = int(lines[0])
        if lines[0] != str(t) or not 1 <= t <= 10000:
            return False
        i = 1; total = 0
        for _ in range(t):
            n = int(lines[i]); i += 1
            if lines[i - 1] != str(n) or not 4 <= n <= MAXN_STATEMENT:
                return False
            total += n
            seen = set()
            for _ in range(n):
                parts = lines[i].split(" "); i += 1
                if len(parts) != 2:
                    return False
                x, y = int(parts[0]), int(parts[1])
                if f"{x} {y}" != lines[i - 1] or not (1 <= x <= n and 1 <= y <= n):
                    return False
                if (x, y) in seen:
                    return False
                seen.add((x, y))
        return i == len(lines) and total <= MAXN_STATEMENT
    except (ValueError, IndexError):
        return False


# ---------------------------------------------------------------- oracle
def brute_one(pts):
    n = len(pts)
    if n > ORACLE_N:
        return None
    colorings = set()
    for k1 in range(0, n + 1):
        for k2 in range(0, n + 1):
            col = tuple((0 if x <= k1 else 1) * 2 + (0 if y <= k2 else 1) for x, y in pts)
            if len(set(col)) == 4:
                colorings.add(col)
    return len(colorings)


def parse(text):
    tok = text.split(); p = 1; tests = []
    for _ in range(int(tok[0])):
        n = int(tok[p]); p += 1
        tests.append([(int(tok[p + 2 * j]), int(tok[p + 2 * j + 1])) for j in range(n)]); p += 2 * n
    return tests


def oracle(text):
    res = []
    for pts in parse(text):
        a = brute_one(pts)
        if a is None:
            return None
        res.append(a)
    return res


# ---------------------------------------------------------------- build
def build():
    out = HERE / "data"; out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 21):
        attempt = 0; case = generate(seed)
        while case in cases:
            attempt += 1; case = generate(seed, attempt)
        cases.append(case)
    checked = 0
    for idx, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {idx}: input contract violated")
        ans = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                             capture_output=True, check=True).stdout
        if idx == 0 and ans.split() != SAMPLE_OUT.split():
            raise SystemExit(f"sample mismatch: {ans!r}")
        o = oracle(case)
        if o is not None:
            if list(map(int, ans.split())) != o:
                raise SystemExit(f"case {idx}: oracle disagreement")
            checked += 1
        (out / f"{idx}.in").write_text(case, encoding="utf-8")
        (out / f"{idx}.out").write_text(ans, encoding="utf-8")
        print(f"case {idx}: in={len(case)}B out={len(ans)}B oracle={'yes' if o is not None else 'no'}")
    print(f"oracle-checked {checked}/21")


if __name__ == "__main__":
    build()
