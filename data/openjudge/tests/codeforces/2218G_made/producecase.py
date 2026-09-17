#!/usr/bin/env python3
"""Codeforces 2218G The 67th Iteration of "Counting is Fun" -- generator, contract, oracle, build.

Written for this repository.  Run `python3 producecase.py` from this directory.

Input: t (1..1e4); each test: `n m` (1 <= m <= n <= 2e5), then b_1..b_n with
0 <= b_i < m and every value 0..m-1 present; sum n <= 2e5.
Output: one integer per test, the number of arrays a (0 <= a_i < n) producing b,
mod 676767677.

Shapes (seed -> what it attacks):
  1  n=1 (b=[0])                                     answer 1
  2  every valid b for n=1..5 (633 tests)            exhaustive small space
  3  every valid b for n=6 (4683 tests)
  4  t=1e4, n<=7, b produced by growth (mostly non-zero answers)
  5  t=1e4, n<=7, arbitrary contiguous b (zero and non-zero answers)
  6  all zeros n=2e5, m=1                           answer 1
  7  staircase 0,1,...,n-1 (m=n)                     (n-1)! style product: needs modulus
  8  staircase from the right end
  9  single zero in the middle, both fronts advance together
 10  random growth, few zeros, frontier people often delayed (s < t branch)
 11  random growth, many zeros (small m, large equal-time groups)
 12  t=1e4, n=8 growth tests, 3/4 with one planted violation (strict local minimum > 0)
 13  t=1e4, n<=7, violations/delays placed at array ends (neighbour of index 1 / n)
 14  t=1e4, n<=7, growth b with one random perturbation (kept contiguous)
 15  heavy delays: frontier sits with probability 0.05 per step, n=2e5
 16  two big growth tests with different parameters
 17  m=n with the zero at a random position, fronts alternate randomly
 18  t=1e4, n=20 growth tests (sum n = 2e5)
 19  arbitrary contiguous b (n=5e4, m large / m=3), plus 100 n=1000 growth tests with
     a planted violation (all answers 0)
 20  m=2: blocks of one or two 1s between zeros, n=2e5 (huge power of #zeros)

Oracle: brute-force enumeration of every array a in [0,n)^n for n<=8, simulating the
seating process literally and tallying the produced b; any test with n<=8 is checked
against that tally (b absent from the tally => 0).
"""
from __future__ import annotations
import collections
import itertools
import random
import subprocess
import sys
from pathlib import Path

MOD = 676767677
REFERENCE = Path(__file__).with_name("samplecode.py")
SAMPLE = ("7\n4 3\n0 1 2 0\n8 4\n0 1 2 3 1 2 0 1\n9 5\n1 0 1 3 4 3 2 1 0\n"
          "15 14\n3 0 1 2 3 4 5 6 7 8 9 10 11 12 13\n5 5\n4 3 0 1 2\n5 2\n0 1 1 1 0\n3 2\n0 1 1\n")
SAMPLE_OUT = "2\n0\n1920\n138007136\n8\n0\n0\n"
ORACLE_MAX_N = 8
BIGN = 200000


def growth(r, n, pzero, psit, zeros=None):
    """b from an actual spread: at each step a random subset of the frontier sits."""
    b = [-1] * n
    if zeros is None:
        zeros = [i for i in range(n) if r.random() < pzero]
        if not zeros:
            zeros = [r.randrange(n)]
    for i in zeros:
        b[i] = 0
    frontier = set()
    for i in zeros:
        for j in (i - 1, i + 1):
            if 0 <= j < n and b[j] < 0:
                frontier.add(j)
    t = 0
    left = n - len(zeros)
    while left:
        t += 1
        cand = sorted(frontier)
        chosen = [i for i in cand if r.random() < psit]
        if not chosen:
            chosen = [r.choice(cand)]
        for i in chosen:
            b[i] = t
        left -= len(chosen)
        for i in chosen:
            frontier.discard(i)
        for i in chosen:
            for j in (i - 1, i + 1):
                if 0 <= j < n and b[j] < 0:
                    frontier.add(j)
    return b


def contiguous(b):
    m = max(b) + 1
    return len(set(b)) == m and min(b) == 0


def arbitrary(r, n, m=None):
    while True:
        mm = m if m is not None else r.randint(1, n)
        b = list(range(mm)) + [r.randrange(mm) for _ in range(n - mm)]
        r.shuffle(b)
        if contiguous(b):
            return b


def perturb(r, b, where=None):
    n = len(b)
    for _ in range(100):
        c = b[:]
        i = r.randrange(n) if where is None else where
        c[i] = r.randrange(max(c) + 2)
        if c != b and contiguous(c):
            return c
    return b


def plant_violation(r, b):
    """Make some position a strict local minimum with positive value, keeping contiguity."""
    n = len(b)
    for _ in range(1000):
        i = r.randrange(n)
        nb = [b[j] for j in (i - 1, i + 1) if 0 <= j < n]
        lo = min(nb)
        if lo >= 1:
            c = b[:]; c[i] = r.randint(1, lo)
            if contiguous(c):
                return c
    return b


def fmt(tests):
    return f"{len(tests)}\n" + "".join(f"{len(b)} {max(b) + 1}\n{' '.join(map(str, b))}\n" for b in tests)


def all_b(n):
    for b in itertools.product(range(n), repeat=n):
        if contiguous(b):
            yield list(b)


def generate(seed):
    r = random.Random(2218_0007 * 104729 + seed)
    if seed == 1:
        return fmt([[0]])
    if seed == 2:
        return fmt([b for n in range(1, 6) for b in all_b(n)])
    if seed == 3:
        return fmt(list(all_b(6)))
    if seed == 4:
        return fmt([growth(r, r.randint(1, 7), r.choice([0.1, 0.3, 0.5]), r.choice([0.3, 0.6, 1.0])) for _ in range(10000)])
    if seed == 5:
        return fmt([arbitrary(r, r.randint(1, 7)) for _ in range(10000)])
    if seed == 6:
        return fmt([[0] * BIGN])
    if seed == 7:
        return fmt([list(range(BIGN))])
    if seed == 8:
        return fmt([list(range(BIGN - 1, -1, -1))])
    if seed == 9:
        c = BIGN // 2 + 12345
        return fmt([[abs(i - c) for i in range(BIGN)]])
    if seed == 10:
        return fmt([growth(r, BIGN, 0.0005, 0.7)])
    if seed == 11:
        return fmt([growth(r, BIGN, 0.3, 0.5)])
    if seed == 12:
        res = []
        for k in range(10000):
            b = growth(r, 8, r.choice([0.1, 0.25]), r.choice([0.4, 0.8]))
            res.append(plant_violation(r, b) if k % 4 != 3 else b)
        return fmt(res)
    if seed == 13:
        res = []
        for _ in range(10000):
            n = r.randint(2, 7)
            b = growth(r, n, 0.3, 0.6)
            if r.random() < 0.7:
                b = perturb(r, b, where=r.choice([0, n - 1]))
            res.append(b)
        return fmt(res)
    if seed == 14:
        res = []
        for _ in range(10000):
            n = r.randint(1, 7)
            res.append(perturb(r, growth(r, n, 0.25, 0.5)))
        return fmt(res)
    if seed == 15:
        return fmt([growth(r, BIGN, 0.002, 0.05)])
    if seed == 16:
        return fmt([growth(r, 120000, 0.01, 0.9), growth(r, 80000, 0.0001, 0.3)])
    if seed == 17:
        n = BIGN; z = r.randrange(n); b = [0] * n
        lo, hi, t = z - 1, z + 1, 0
        while lo >= 0 or hi < n:
            t += 1
            if hi >= n or (lo >= 0 and r.random() < 0.5):
                b[lo] = t; lo -= 1
            else:
                b[hi] = t; hi += 1
        return fmt([b])
    if seed == 18:
        return fmt([growth(r, 20, r.choice([0.05, 0.2, 0.4]), r.choice([0.2, 0.5, 1.0])) for _ in range(10000)])
    if seed == 19:
        planted = [plant_violation(r, growth(r, 1000, 0.02, 0.6)) for _ in range(100)]
        return fmt([arbitrary(r, 50000, 35000), arbitrary(r, 49990, 3), [1, 0] + [1] * 8] + planted)
    if seed == 20:
        b = []
        while len(b) < BIGN - 10:
            b += [0] * r.randint(1, 3) + [1] * r.randint(1, 2)
        b = b[:BIGN - 10] + [0] * 10
        return fmt([b])
    raise ValueError(seed)


def valid(text):
    if not text.endswith("\n"):
        return False
    lines = text.split("\n")[:-1]
    try:
        t = int(lines[0])
        if lines[0] != str(t) or not 1 <= t <= 10**4 or len(lines) != 1 + 2 * t:
            return False
        total = 0
        for k in range(t):
            head = lines[1 + 2 * k].split(" ")
            if len(head) != 2 or any(x != str(int(x)) for x in head):
                return False
            n, m = map(int, head)
            if not 1 <= m <= n <= 2 * 10**5:
                return False
            parts = lines[2 + 2 * k].split(" ")
            if len(parts) != n or any(x != str(int(x)) for x in parts):
                return False
            b = list(map(int, parts))
            if any(not 0 <= x < m for x in b) or len(set(b)) != m:
                return False
            total += n
        return total <= 2 * 10**5
    except (ValueError, IndexError):
        return False


_TABLES = {}


def tally(n):
    """Enumerate every a in [0,n)^n, simulate literally, count produced b."""
    if n in _TABLES:
        return _TABLES[n]
    cnt = collections.Counter()
    for a in itertools.product(range(n), repeat=n):
        b = [0 if x == 0 else -1 for x in a]
        sat = n - b.count(-1)
        if sat == 0:
            continue
        t = 0; left = n - sat
        while left:
            t += 1
            new = [i for i in range(n) if b[i] < 0 and a[i] <= sat and
                   ((i > 0 and b[i - 1] >= 0) or (i + 1 < n and b[i + 1] >= 0))]
            if not new:
                break
            for i in new:
                b[i] = t
            sat += len(new); left -= len(new)
        if left == 0:
            cnt[tuple(b)] += 1
    _TABLES[n] = cnt
    return cnt


def oracle_lines(text):
    tok = text.split(); p = 1; res = []
    for _ in range(int(tok[0])):
        n = int(tok[p]); p += 2
        b = tuple(map(int, tok[p:p + n])); p += n
        res.append(str(tally(n).get(b, 0) % MOD) if n <= ORACLE_MAX_N else None)
    return res


def build():
    out = Path(__file__).with_name("data"); out.mkdir(exist_ok=True)
    for f in out.glob("*"): f.unlink()
    cases = [SAMPLE] + [generate(seed) for seed in range(1, 21)]
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
        checked = 0; nonzero = 0
        for g, e in zip(got, exp):
            nonzero += g != "0"
            if e is not None:
                checked += 1
                if g != e:
                    raise SystemExit(f"case {index}: oracle disagreement")
        full += checked == len(exp)
        print(f"case {index}: {checked}/{len(exp)} tests oracle-checked, {nonzero} non-zero answers", file=sys.stderr)
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(ans, encoding="utf-8")
    print(f"{full} files fully oracle-checked", file=sys.stderr)


if __name__ == "__main__":
    build()
