#!/usr/bin/env python3
"""Codeforces 2205D Simons and Beating Peaks -- generator, input contract, oracle, build.

Written for this repository.  Run `python3 producecase.py` from this directory.

Input: t (1..5e4); each test: n (3..5e5) and a permutation of 1..n; sum n <= 5e5.
Output: one integer per test (minimum number of operations).

Shapes (seed -> what it attacks):
  1  all 6 permutations of n=3
  2  all permutations of n=4,5,6 (864 tests)
  3  t=50000, n in 3..9 random                     (max t, multi-test handling)
  4  t=3000, n in 7..10 random
  5  t=400, n in 10..12 random, skewed Cartesian trees (kills "delete smaller side" greedy)
  6  increasing n=440000                           (answer 0, Cartesian depth n)
  7  decreasing n=440000                           (answer 0)
  8  two V-shaped arrays                            (already cool)
  9  mountain (up then down), max off-centre       (answer = shorter side)
 10  random permutation n=440000
 11  zigzag 2 1 4 3 6 5 ... n=440000                 (many peaks, deep Cartesian tree)
 12  random skewed Cartesian tree n=440000
 13  nested mountains: recursive tree with random split ratios, n=440000
 14  t=500, n=1000 random-split trees
 15  t=2000, n in 3..12, global max near an end
 16  two big skewed trees (split ratio ~0.9 / ~0.1)
 17  t=20000, n in 3..12 skewed trees
 18  t=5000, n in 13..60 random-split trees
 19  t=10000, n in 3..50, max at position 2 or n-1
 20  t=50000, n=10 each (sum n = 5e5)
Input files are capped at ~3 MB, so single big arrays use n=440000 (statement max 5e5).

Oracle: exhaustive search over the actual operation (memoised over the current array
as a tuple: try every peak and both neighbours), for every test with n <= 12.
"""
from __future__ import annotations
import random
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

REFERENCE = Path(__file__).with_name("samplecode.py")
SAMPLE = "5\n3\n1 2 3\n5\n4 1 3 2 5\n6\n4 5 3 6 2 1\n7\n6 5 1 7 4 2 3\n15\n7 4 10 12 9 14 5 3 8 11 1 15 2 13 6\n"
SAMPLE_OUT = "0\n1\n3\n3\n9\n"
ORACLE_MAX_N = 12
BIG = 440000


def tree_perm(r, n, ratio=None, skew=None):
    """Permutation whose Cartesian tree has random (or skewed) split sizes."""
    pos_val = [0] * n
    nxt = n
    st = [(0, n)]  # half-open segments; preorder assignment of decreasing values
    while st:
        lo, hi = st.pop()
        if lo >= hi:
            continue
        size = hi - lo
        if skew is not None:
            k = int((size - 1) * skew + r.random())
            k = min(size - 1, max(0, k))
        elif ratio == "extreme":
            k = r.choice([0, size - 1, r.randrange(size)])
        else:
            k = r.randrange(size)
        m = lo + k
        pos_val[m] = nxt; nxt -= 1
        st.append((m + 1, hi)); st.append((lo, m))
    return pos_val


def fmt(tests):
    return f"{len(tests)}\n" + "".join(f"{len(a)}\n{' '.join(map(str, a))}\n" for a in tests)


def generate(seed):
    import itertools
    r = random.Random(2205_0004 * 7919 + seed)

    def rnd(n):
        a = list(range(1, n + 1)); r.shuffle(a); return a

    if seed == 1:
        return fmt([list(p) for p in itertools.permutations(range(1, 4))])
    if seed == 2:
        return fmt([list(p) for n in (4, 5, 6) for p in itertools.permutations(range(1, n + 1))])
    if seed == 3:
        return fmt([rnd(r.randint(3, 9)) for _ in range(50000)])
    if seed == 4:
        return fmt([rnd(r.randint(7, 10)) for _ in range(3000)])
    if seed == 5:
        return fmt([tree_perm(r, r.randint(10, 12), ratio="extreme") for _ in range(400)])
    if seed == 6:
        return fmt([list(range(1, BIG + 1))])
    if seed == 7:
        return fmt([list(range(BIG, 0, -1))])
    if seed == 8:
        res = []
        for n in (200000, 240000):
            vals = rnd(n); vals.remove(1)
            k = r.randrange(len(vals))
            left = sorted(vals[:k], reverse=True); right = sorted(vals[k:])
            res.append(left + [1] + right)
        return fmt(res)
    if seed == 9:
        n = BIG; vals = list(range(1, n)); r.shuffle(vals)
        k = 150000
        return fmt([sorted(vals[:k]) + [n] + sorted(vals[k:], reverse=True)])
    if seed == 10:
        return fmt([rnd(BIG)])
    if seed == 11:
        a = []
        for i in range(1, BIG, 2):
            a += [i + 1, i]
        return fmt([a])
    if seed == 12:
        return fmt([tree_perm(r, BIG, ratio="extreme")])
    if seed == 13:
        return fmt([tree_perm(r, BIG)])
    if seed == 14:
        return fmt([tree_perm(r, 1000) for _ in range(500)])
    if seed == 15:
        res = []
        for _ in range(2000):
            n = r.randint(3, 12); a = rnd(n); a.remove(n)
            a.insert(r.choice([0, 1, n - 2, n - 1]), n); res.append(a)
        return fmt(res)
    if seed == 16:
        return fmt([tree_perm(r, 220000, skew=0.9), tree_perm(r, 220000, skew=0.1)])
    if seed == 17:
        return fmt([tree_perm(r, r.randint(3, 12), skew=r.choice([0.15, 0.3, 0.7, 0.85])) for _ in range(20000)])
    if seed == 18:
        return fmt([tree_perm(r, r.randint(13, 60), ratio=r.choice([None, "extreme"])) for _ in range(5000)])
    if seed == 19:
        res = []
        for _ in range(10000):
            n = r.randint(3, 50); a = rnd(n); a.remove(n)
            a.insert(r.choice([1, n - 2]), n); res.append(a)
        return fmt(res)
    if seed == 20:
        return fmt([rnd(10) for _ in range(50000)])
    # Extended range: random combinations
    tests = []
    for _ in range(r.randint(100, 500)):
        n = r.randint(3, r.choice([12, 60, 100]))
        tests.append(tree_perm(r, n, skew=r.random()))
    return fmt(tests)


def valid(text):
    if not text.endswith("\n"):
        return False
    lines = text.split("\n")[:-1]
    try:
        t = int(lines[0])
        if lines[0] != str(t) or not 1 <= t <= 5 * 10**4 or len(lines) != 1 + 2 * t:
            return False
        total = 0
        for i in range(t):
            n = int(lines[1 + 2 * i])
            if lines[1 + 2 * i] != str(n) or not 3 <= n <= 5 * 10**5:
                return False
            parts = lines[2 + 2 * i].split(" ")
            if len(parts) != n or any(x != str(int(x)) for x in parts):
                return False
            if sorted(map(int, parts)) != list(range(1, n + 1)):
                return False
            total += n
        return total <= 5 * 10**5
    except (ValueError, IndexError):
        return False


@lru_cache(maxsize=None)
def brute(a):
    """Minimum operations from array a by trying every legal operation."""
    best = None
    for i in range(1, len(a) - 1):
        if a[i] > a[i - 1] and a[i] > a[i + 1]:
            for j in (i - 1, i + 1):
                c = 1 + brute(normalise(a[:j] + a[j + 1:]))
                if best is None or c < best:
                    best = c
    return 0 if best is None else best


def normalise(a):
    order = sorted(range(len(a)), key=a.__getitem__)
    res = [0] * len(a)
    for rank, i in enumerate(order):
        res[i] = rank
    return tuple(res)


def oracle_lines(text):
    tok = text.split(); p = 1; res = []
    for _ in range(int(tok[0])):
        n = int(tok[p]); p += 1
        a = tok[p:p + n]; p += n
        res.append(str(brute(normalise(list(map(int, a))))) if n <= ORACLE_MAX_N else None)
    return res


def build():
    out = Path(__file__).with_name("data"); out.mkdir(exist_ok=True)
    for f in out.glob("*"): f.unlink()
    cases = [SAMPLE] + [generate(seed) for seed in range(1, 40)]
    if len(set(cases)) != len(cases):
        raise SystemExit("duplicate inputs")
    full = 0
    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {index} violates the input contract")
        ans = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                             capture_output=True, check=True, timeout=120).stdout
        if index == 0 and ans.split() != SAMPLE_OUT.split():
            raise SystemExit(f"sample mismatch: {ans!r}")
        got = ans.split()
        exp = oracle_lines(case)
        if len(got) != len(exp):
            raise SystemExit(f"case {index}: wrong number of outputs")
        checked = 0
        for g, e in zip(got, exp):
            if e is not None:
                checked += 1
                if g != e:
                    raise SystemExit(f"case {index}: oracle disagreement")
        full += checked == len(exp)
        print(f"case {index}: {checked}/{len(exp)} tests oracle-checked", file=sys.stderr)
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(ans, encoding="utf-8")
    print(f"{full} files fully oracle-checked", file=sys.stderr)


if __name__ == "__main__":
    build()
