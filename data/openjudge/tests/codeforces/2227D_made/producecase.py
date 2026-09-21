#!/usr/bin/env python3
"""Codeforces 2227D Palindromex -- generator, input contract, oracle and build.

Written for this repo as a hand-off artifact.

Statement: t (1<=t<=1e4) tests; each has n (1<=n<=1e5) and 2n integers in [0, n-1],
every value in [0, n-1] appears exactly twice; sum of 2n <= 2e5.  Output the maximum
mex over palindromic subarrays.

Shapes (seed -> how solutions go wrong):
  1        n=1 only ([0 0], answer 1).
  2        t=1e4 tests with n in 1..4 -- many small, near-exhaustive coverage.
  3        many tests n in 5..12 uniform random.
  4        many full-array palindromes (answer n) -- the midpoint-of-zeros centre.
  5        full palindromes with one random swap (breaks symmetry near the ends/middle).
  6        odd palindrome centred on ONE zero, the other zero far away -- kills solutions
           that only use the midpoint of the two zeros.
  7        same as 6 but centred on the SECOND zero -- kills "first zero only".
  8        zeros adjacent / even centre with mirrored values, plus decoys.
  9        long palindrome that misses value 1 (mex trap: length != mex).
  10       mixed small shapes 4..9 in one file, n up to 60.
  11       medium random n ~ 200..2000 (oracle-checked, O(m^2) oracle).
  12       medium structured (zero-centred / midpoint) n ~ 500..1500.
  13       n=1e5 full palindrome (answer 100000).
  14       n=1e5 palindrome centred on the second zero, length ~ 2n-ish.
  15       n=1e5 uniform random.
  16       n=1e5 full palindrome with one swap near the ends (answer large but < n).
  17       n=1e5 radius-5e4 palindrome on first zero, value 1 missing inside (mex trap).
  18       2 tests n=5e4 each: one midpoint-centre winner, one zero-centre winner.
  19       t=1e4 tests with n in 1..19 (sum 2n <= 2e5) random structured mix.
  20       1000 tests of n=100 structured mix.
The oracle expands every one of the 4n-1 centres (not only zero-related ones) and keeps
an incremental mex; it runs on every file whose sum of (2n)^2 is at most ORACLE_BUDGET.
"""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
SAMPLE = """6
4
1 2 0 3 3 0 2 1
2
0 1 0 1
2
1 1 0 0
3
2 0 2 1 1 0
4
0 1 3 0 3 1 2 2
3
0 1 2 1 0 2
"""
SAMPLE_OUT = "4\n2\n1\n1\n2\n3\n"
ORACLE_BUDGET = 30_000_000
MAXN = 100_000


def rand_arr(r, n):
    a = list(range(n)) * 2
    r.shuffle(a)
    return a


def full_pal(r, n):
    half = list(range(n)); r.shuffle(half)
    return half[::-1] + half


def zero_centred(r, n, k, second=False, missing_one=False):
    """Odd palindrome of radius k centred on a zero, holding values 1..k (or 2..k+1
    when missing_one, so mex stays 1); the other zero is outside on the chosen side."""
    k = min(k, n - 1)
    if missing_one:
        k = min(k, n - 2)
        inside = list(range(2, k + 2))
    else:
        inside = list(range(1, k + 1))
    r.shuffle(inside)
    core = inside[::-1] + [0] + inside
    used = set(inside)
    rest = [v for v in range(1, n) if v not in used for _ in (0, 1)]
    r.shuffle(rest)
    cut = r.randint(0, len(rest)); c2 = r.randint(cut, len(rest))
    if second:
        return rest[:cut] + [0] + rest[cut:c2] + core + rest[c2:]
    return rest[:cut] + core + rest[cut:c2] + [0] + rest[c2:]


def even_centre(r, n, k):
    """Two adjacent zeros with values 1..k mirrored around them, rest random outside."""
    k = min(k, n - 1)
    inside = list(range(1, k + 1)); r.shuffle(inside)
    core = inside[::-1] + [0, 0] + inside
    rest = [v for v in range(k + 1, n) for _ in (0, 1)]
    r.shuffle(rest)
    cut = r.randint(0, len(rest))
    return rest[:cut] + core + rest[cut:]


def swapped(r, a):
    a = a[:]
    i, j = r.randrange(len(a)), r.randrange(len(a))
    a[i], a[j] = a[j], a[i]
    return a


def structured(r, n):
    s = r.randrange(7)
    if n == 1:
        return [0, 0]
    if s == 0: return full_pal(r, n)
    if s == 1: return swapped(r, full_pal(r, n))
    if s == 2: return zero_centred(r, n, r.randint(1, n), second=False)
    if s == 3: return zero_centred(r, n, r.randint(1, n), second=True)
    if s == 4: return even_centre(r, n, r.randint(0, n))
    if s == 5: return zero_centred(r, n, r.randint(1, n), second=r.random() < .5, missing_one=True)
    return rand_arr(r, n)


def fill(r, total, lo, hi, maker, tmax=10_000):
    tests = []; used = 0
    while len(tests) < tmax:
        n = r.randint(lo, hi)
        if used + 2 * n > total:
            break
        tests.append(maker(r, n)); used += 2 * n
    return tests


def generate(seed, attempt=0):
    r = random.Random(2227_0004_000 + seed * 7919 + attempt)
    if seed == 1: tests = [[0, 0]]
    elif seed == 2: tests = fill(r, 50_000, 1, 4, lambda r, n: rand_arr(r, n) if r.random() < .5 else structured(r, n))
    elif seed == 3: tests = fill(r, 40_000, 5, 12, rand_arr, 3000)
    elif seed == 4: tests = fill(r, 20_000, 2, 30, full_pal, 1000)
    elif seed == 5: tests = fill(r, 20_000, 2, 30, lambda r, n: swapped(r, full_pal(r, n)), 1000)
    elif seed == 6: tests = fill(r, 20_000, 3, 40, lambda r, n: zero_centred(r, n, r.randint(n // 2, n), False), 1000)
    elif seed == 7: tests = fill(r, 20_000, 3, 40, lambda r, n: zero_centred(r, n, r.randint(n // 2, n), True), 1000)
    elif seed == 8: tests = fill(r, 20_000, 2, 40, lambda r, n: even_centre(r, n, r.randint(0, n)), 1000)
    elif seed == 9: tests = fill(r, 20_000, 3, 40, lambda r, n: zero_centred(r, n, n, r.random() < .5, True), 1000)
    elif seed == 10: tests = fill(r, 40_000, 1, 60, structured, 1000)
    elif seed == 11: tests = fill(r, 12_000, 200, 2000, rand_arr)
    elif seed == 12: tests = fill(r, 12_000, 500, 1500, structured)
    elif seed == 13: tests = [full_pal(r, MAXN)]
    elif seed == 14: tests = [zero_centred(r, MAXN, MAXN - 3, True)]
    elif seed == 15: tests = [rand_arr(r, MAXN)]
    elif seed == 16:
        half = list(range(MAXN)); tail = half[60_000:]; r.shuffle(tail); half[60_000:] = tail
        a = half[::-1] + half; i = 1234; j = 2 * MAXN - 1 - 5678; a[i], a[j] = a[j], a[i]; tests = [a]
    elif seed == 17: tests = [zero_centred(r, MAXN, MAXN // 2, False, True)]
    elif seed == 18:
        a = full_pal(r, 50_000); a[0], a[1] = a[1], a[0]
        tests = [a, zero_centred(r, 50_000, 40_000, True)]
    elif seed == 19: tests = fill(r, 200_000, 1, 19, structured)
    else: tests = [structured(r, 100) for _ in range(1000)]
    return f"{len(tests)}\n" + "".join(f"{len(a) // 2}\n{' '.join(map(str, a))}\n" for a in tests)


def parse(text):
    tok = text.split(); t = int(tok[0]); p = 1; tests = []
    for _ in range(t):
        n = int(tok[p]); p += 1
        tests.append(list(map(int, tok[p:p + 2 * n]))); p += 2 * n
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
            if not 1 <= n <= 100_000: return False
            a = arow.split(" ")
            if len(a) != 2 * n or any(x != str(int(x)) for x in a): return False
            a = list(map(int, a))
            cnt = [0] * n
            for x in a:
                if not 0 <= x <= n - 1: return False
                cnt[x] += 1
            if any(c != 2 for c in cnt): return False
            total += 2 * n
        return total <= 200_000
    except (ValueError, IndexError):
        return False


def oracle_one(a):
    m = len(a); best = 0
    for c in range(2 * m - 1):               # centre c: l=c//2, r=(c+1)//2
        l, r = c // 2, (c + 1) // 2
        cnt = {}; mex = 0
        while l >= 0 and r < m and a[l] == a[r]:
            for v in ((a[l],) if l == r else (a[l], a[r])):
                cnt[v] = cnt.get(v, 0) + 1
            while mex in cnt:
                mex += 1
            best = max(best, mex)
            l -= 1; r += 1
    return best


def oracle(text):
    return [oracle_one(a) for a in parse(text)]


def oracle_feasible(text):
    return sum(len(a) ** 2 for a in parse(text)) <= ORACLE_BUDGET


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
