#!/usr/bin/env python3
"""Codeforces 2227F It Just Keeps Going Sideways -- generator, input contract, oracle and build.

Written for this repo as a hand-off artifact.

Statement: t (1<=t<=1e4) tests; each has n (1<=n<=2e5) and a_1..a_n with 1<=a_i<=n;
sum of n <= 2e5.  Gravity pulls right; at most one a_i may be decreased by 1 first.
Output the maximum total movement distance sum |j - i| over all remaining cubes.

Shapes (seed -> how solutions go wrong):
  1   n=1, a=[1] (removing the only cube: answer 0).
  2   EXHAUSTIVE: every array for n=1..5 (3413 tests) -- all small corner cases.
  3   t=1e4, n in 1..6, random.
  4   many n in 6..12 random.
  5   many non-decreasing arrays (base 0; only plateau at the end can gain).
  6   many non-increasing arrays (long equal-suffix-minimum runs).
  7   many constant arrays / constant with one dip.
  8   plateau traps: blocks of equal heights; the best column to decrement (max of
      i + #{a_j >= a_i}) is often not the last column nor a global minimum.
  9   valleys and mountains (like sample 1), values from a small range.
  10  many n~40, values in 1..3 (lots of ties).
  11  mixed structured tests, n up to 30 (oracle-checked).
  12  n=2e5 uniform random.
  13  n=2e5 random permutation.
  14  n=2e5 strictly decreasing (answer ~1.3e15: 32-bit overflow).
  15  n=2e5: a=[n]*(n-1)+[1] (total ~ 4e10 > 2^31).
  16  n=2e5 plateau structure, best decrement far from the end.
  17  n=2e5 non-decreasing with a long flat tail.
  18  4 tests of n=5e4, structured.
  19  t=1e4 tests with n=20 (sum n = 2e5), structured mix (too slow for the oracle).
  20  n=2e5 all a_i = n (only decrementing a_n helps: answer n-1).
The oracle rebuilds the grid for "no operation" and for every possible decrement,
physically slides cubes one cell at a time until nothing moves, and sums |final
column - original column| over all cubes.  It is run on every file whose cost estimate fits the budget.
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
5
1 2 3 2 1
7
5 4 1 1 1 1 3
6
1 2 3 4 5 6
6
4 1 6 3 2 6
7
1 3 2 7 2 3 1
"""
SAMPLE_OUT = "9\n37\n0\n17\n29\n"
MAXN = 200_000
ORACLE_BUDGET = 200_000_000


def rnd(r, n, lo=1, hi=None):
    hi = n if hi is None else min(hi, n)
    return [r.randint(lo, hi) for _ in range(n)]


def plateau(r, n):
    """Blocks of equal values with increasing block values towards the right, noise
    above the running suffix minimum -- several flat suffix-minimum runs."""
    if n <= 2:
        return rnd(r, n)
    k = r.randint(1, min(5, n)); cuts = sorted(r.sample(range(1, n), min(k - 1, n - 1)))
    bounds = [0] + cuts + [n]
    levels = sorted(r.sample(range(1, n + 1), len(bounds) - 1))
    a = []
    for b in range(len(bounds) - 1):
        lv = levels[b]
        for _ in range(bounds[b + 1] - bounds[b]):
            a.append(lv if r.random() < 0.7 else r.randint(lv, n))
    return a


def structured(r, n):
    s = r.randrange(7)
    if s == 0: return sorted(rnd(r, n))
    if s == 1: return sorted(rnd(r, n), reverse=True)
    if s == 2: return [r.randint(1, n)] * n
    if s == 3: return plateau(r, n)
    if s == 4:
        m = r.randint(0, n); x = sorted(rnd(r, n))
        return x[:m] + sorted(x[m:], reverse=True)
    if s == 5: return rnd(r, n, 1, 3)
    return rnd(r, n)


def fill(r, total, lo, hi, maker, tmax=10_000):
    tests = []; used = 0
    while len(tests) < tmax:
        n = r.randint(lo, hi)
        if used + n > total:
            break
        tests.append(maker(r, n)); used += n
    return tests


def generate(seed, attempt=0):
    r = random.Random(2227_0006_000 + seed * 7919 + attempt)
    if seed == 1: tests = [[1]]
    elif seed == 2:
        tests = [list(p) for n in range(1, 6) for p in itertools.product(range(1, n + 1), repeat=n)]
    elif seed == 3: tests = fill(r, 40_000, 1, 6, rnd)
    elif seed == 4: tests = fill(r, 30_000, 6, 12, rnd, 3000)
    elif seed == 5: tests = fill(r, 20_000, 2, 15, lambda r, n: sorted(rnd(r, n, 1, r.randint(1, n))), 2000)
    elif seed == 6: tests = fill(r, 20_000, 2, 15, lambda r, n: sorted(rnd(r, n, 1, r.randint(1, n)), reverse=True), 2000)
    elif seed == 7:
        def mk(r, n):
            a = [r.randint(1, n)] * n
            if r.random() < 0.5 and a[0] > 1:
                a[r.randrange(n)] -= r.randint(1, a[0] - 1)
            return a
        tests = fill(r, 20_000, 1, 15, mk, 2000)
    elif seed == 8: tests = fill(r, 20_000, 5, 20, plateau, 1500)
    elif seed == 9:
        def mk(r, n):
            x = sorted(rnd(r, n, 1, 4)); m = r.randint(0, n)
            y = x[:m] + sorted(x[m:], reverse=True)
            return y if r.random() < 0.5 else [max(y) + 1 - v for v in y]
        tests = fill(r, 20_000, 3, 20, mk, 1500)
    elif seed == 10: tests = fill(r, 20_000, 30, 50, lambda r, n: rnd(r, n, 1, 3), 500)
    elif seed == 11: tests = fill(r, 20_000, 10, 30, structured, 600)
    elif seed == 12: tests = [rnd(r, MAXN)]
    elif seed == 13: a = list(range(1, MAXN + 1)); r.shuffle(a); tests = [a]
    elif seed == 14: tests = [list(range(MAXN, 0, -1))]
    elif seed == 15: tests = [[MAXN] * (MAXN - 1) + [1]]
    elif seed == 16:
        a = [r.randint(150_000, MAXN) for _ in range(MAXN)]
        for i in range(20_000, 120_000):
            a[i] = 100_000 if r.random() < 0.9 else r.randint(100_000, MAXN)
        a[119_999] = 100_000
        for i in range(120_000, MAXN):
            a[i] = r.randint(100_001, MAXN)
        a[-1] = 100_001; a[-2] = 100_001
        tests = [a]
    elif seed == 17:
        a = sorted(rnd(r, 150_000, 1, 150_000)) + [150_000] * 50_000; tests = [a]
    elif seed == 18: tests = [structured(r, 50_000) for _ in range(3)] + [plateau(r, 50_000)]
    elif seed == 19: tests = [structured(r, 20) for _ in range(10_000)]
    else: tests = [[MAXN] * MAXN]
    return f"{len(tests)}\n" + "".join(f"{len(a)}\n{' '.join(map(str, a))}\n" for a in tests)


def parse(text):
    tok = text.split(); t = int(tok[0]); p = 1; tests = []
    for _ in range(t):
        n = int(tok[p]); p += 1
        tests.append(list(map(int, tok[p:p + n]))); p += n
    return tests


def valid(text):
    if not text.endswith("\n"):
        return False
    rows = text.split("\n")[:-1]
    try:
        if rows[0] != str(int(rows[0])): return False
        t = int(rows[0])
        if not 1 <= t <= 10_000 or len(rows) != 1 + 2 * t: return False
        total = 0
        for i in range(t):
            nrow, arow = rows[1 + 2 * i], rows[2 + 2 * i]
            if nrow != str(int(nrow)): return False
            n = int(nrow)
            if not 1 <= n <= 200_000: return False
            a = arow.split(" ")
            if len(a) != n or any(x != str(int(x)) for x in a): return False
            if not all(1 <= int(x) <= n for x in a): return False
            total += n
        return total <= 200_000
    except (ValueError, IndexError):
        return False


def settle(a):
    """Return {cube_id: final column}; cube id = (original column, height)."""
    n = len(a); H = max(a) if a else 0
    final = {}
    for h in range(1, H + 1):
        row = [(i, h) if a[i] >= h else None for i in range(n)]
        moved = True
        while moved:
            moved = False
            for c in range(n - 2, -1, -1):
                if row[c] is not None and row[c + 1] is None:
                    row[c + 1], row[c] = row[c], None; moved = True
        for c, cube in enumerate(row):
            if cube is not None:
                final[cube] = c
    return final


def metric(a):
    return sum(abs(c - i) for (i, h), c in settle(a).items())


def oracle_one(a):
    best = metric(a)
    for i in range(len(a)):
        b = a[:]; b[i] -= 1
        best = max(best, metric(b))
    return best


def oracle(text):
    return [oracle_one(a) for a in parse(text)]


def oracle_feasible(text):
    return sum(len(a) ** 3 * max(a) for a in parse(text)) <= ORACLE_BUDGET


def build():
    out = HERE / "data"; out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 40):
        attempt = 0; case = generate(seed)
        while case in cases:
            attempt += 1; case = generate(seed, attempt)
        cases.append(case)
    checked = 0
    for idx, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"invalid case {idx}")
        if len(case.encode()) > 3_000_000:
            raise SystemExit(f"case {idx} input too large")
        ans = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                             capture_output=True, check=True).stdout
        if idx == 0 and ans.split() != SAMPLE_OUT.split():
            raise SystemExit("reference disagrees with official sample output")
        if len(ans.encode()) > 1_000_000:
            raise SystemExit(f"case {idx} output too large")
        if oracle_feasible(case):
            if list(map(int, ans.split())) != oracle(case):
                raise SystemExit(f"oracle disagreement on case {idx}")
            checked += 1
        (out / f"{idx}.in").write_text(case, encoding="utf-8")
        (out / f"{idx}.out").write_text(ans, encoding="utf-8")
    print(f"built {len(cases)} cases, oracle-checked {checked}")


if __name__ == "__main__":
    build()
