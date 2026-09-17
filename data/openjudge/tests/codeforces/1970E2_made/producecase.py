#!/usr/bin/env python3
"""1970E2 Trails (Medium) -- generator, input contract, oracles and data build.

Statement: m cabins (1 <= m <= 100), n days (1 <= n <= 1e9), 0 <= s_i, l_i <= 1000,
and "Each cabin is connected, with one or more trails" (so s_i + l_i >= 1 is kept).
Answer = number of trail sequences starting at cabin 1, modulo 1e9+7.

Shapes are chosen around how solutions go wrong:
  * forgetting "at least one of the two trails has to be short" (counting t_i*t_j):
    any case with long trails; all-long-at-cabin-1 cases make the true answer 0.
  * off-by-one in the number of days / exponent: n = 1, n = 2, n = 1e9.
  * dropping one of the short/long cross terms (s_i*t_j instead of the symmetric form):
    cases where s and l differ a lot.
  * ignoring the start cabin (uniform start): random s/l with cabin 1 special.
  * rank-1 degenerate inputs (all l = 0, all s = 0), m = 1, maximal values.

Answers come from samplecode.py (2x2 reduction).  Every case is checked in build by an
independent oracle using the raw m x m transfer matrix built from the definition:
explicit trail-by-trail walk enumeration when tiny, day-by-day DP when n*m*m is small,
otherwise m x m matrix fast power.
"""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

MOD = 1_000_000_007
HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
SAMPLE = "3 2\n1 0 1\n0 1 1\n"
SAMPLE_OUT = "18\n"
MAX_M, MAX_N, MAX_V = 100, 10**9, 1000


def fmt(n, s, l):
    return f"{len(s)} {n}\n{' '.join(map(str, s))}\n{' '.join(map(str, l))}\n"


def rand_vals(r, m, lo=0, hi=MAX_V):
    s = [r.randint(lo, hi) for _ in range(m)]
    l = [r.randint(lo, hi) for _ in range(m)]
    for i in range(m):
        if s[i] + l[i] == 0:
            (s if r.random() < 0.5 else l)[i] = r.randint(1, max(1, hi))
    return s, l


def generate(seed, attempt=0):
    r = random.Random(1970_200_000 + seed * 7919 + attempt * 104729)
    M = MAX_M
    if seed == 1:      # m=1, only a long trail -> 0 every day
        return fmt(1, [0], [1])
    if seed == 2:      # m=1, maximal values, maximal n
        return fmt(MAX_N, [1000], [1000])
    if seed == 3:      # m=1, only short trail
        return fmt(1, [1], [0])
    if seed == 4:      # no short trails anywhere -> 0
        return fmt(MAX_N, [0] * M, [r.randint(1, 1000) for _ in range(M)])
    if seed == 5:      # no long trails (rank 1), max values
        return fmt(MAX_N, [1000] * M, [0] * M)
    if seed == 6:      # everything maximal
        return fmt(MAX_N, [1000] * M, [1000] * M)
    if seed == 7:      # n = 1, m = 100
        s, l = rand_vals(r, M); return fmt(1, s, l)
    if seed == 8:      # n = 2, small m, lopsided s vs l
        m = r.randint(4, 8); s = [r.randint(0, 3) for _ in range(m)]; l = [r.randint(50, 1000) for _ in range(m)]
        return fmt(2, s, l)
    if seed == 9:      # cabin 1 has only long trails; others mixed; n huge
        s, l = rand_vals(r, M); s[0] = 0; l[0] = 1000; return fmt(MAX_N - r.randint(0, 50), s, l)
    if seed == 10:     # full random upper bound
        s, l = rand_vals(r, M); return fmt(r.randint(MAX_N // 2, MAX_N), s, l)
    if seed == 11:     # m = 2, n = 1e9, cabin 1 short-only, cabin 2 long-only
        return fmt(MAX_N, [r.randint(1, 1000), 0], [0, r.randint(1, 1000)])
    if seed == 12:     # tiny values, tiny n: explicit enumeration
        m = r.randint(2, 3); s = [r.randint(0, 2) for _ in range(m)]; l = [r.randint(0, 2) for _ in range(m)]
        for i in range(m):
            if s[i] + l[i] == 0: s[i] = 1
        return fmt(3, s, l)
    if seed == 13:     # small m, moderate n for DP
        s, l = rand_vals(r, r.randint(5, 15)); return fmt(r.randint(20, 200), s, l)
    if seed == 14:     # 0/1 values, m = 100, power-of-two n
        s = [r.randint(0, 1) for _ in range(M)]; l = [1 - x if r.random() < 0.7 else 1 for x in s]
        return fmt(2**29, s, l)
    if seed == 15:     # s tiny, l large (cross terms dominate)
        s = [r.randint(0, 2) for _ in range(M)]; l = [r.randint(900, 1000) for _ in range(M)]
        return fmt(r.randint(1, MAX_N), s, l)
    if seed == 16:     # s large, l tiny
        s = [r.randint(900, 1000) for _ in range(M)]; l = [r.randint(0, 2) for _ in range(M)]
        return fmt(r.randint(1, MAX_N), s, l)
    if seed == 17:     # tiny enumeration case, n = 4
        s = [1, 0]; l = [r.randint(0, 1), 1]
        return fmt(4, s, l)
    if seed == 18:     # medium m, n = 1e9 - 1
        s, l = rand_vals(r, r.randint(20, 60)); return fmt(MAX_N - 1, s, l)
    if seed == 19:     # only cabin 1 has short trails
        s = [r.randint(1, 1000)] + [0] * (M - 1); l = [r.randint(0, 1000)] + [r.randint(1, 1000) for _ in range(M - 1)]
        return fmt(r.randint(MAX_N - 1000, MAX_N), s, l)
    # seed 20: random m, random n
    s, l = rand_vals(r, r.randint(1, M)); return fmt(r.randint(1, MAX_N), s, l)


def valid(text):
    if not text.endswith("\n"):
        return False
    rows = text[:-1].split("\n")
    if len(rows) != 3:
        return False
    try:
        head = [int(x) for x in rows[0].split(" ")]
        s = [int(x) for x in rows[1].split(" ")]
        l = [int(x) for x in rows[2].split(" ")]
    except ValueError:
        return False
    if len(head) != 2:
        return False
    m, n = head
    if not (1 <= m <= MAX_M and 1 <= n <= MAX_N and len(s) == m and len(l) == m):
        return False
    if not all(0 <= x <= MAX_V for x in s + l):
        return False
    return all(a + b >= 1 for a, b in zip(s, l))   # "connected with one or more trails"


def parse(text):
    tok = list(map(int, text.split()))
    m, n = tok[0], tok[1]
    return m, n, tok[2:2 + m], tok[2 + m:2 + 2 * m]


def oracle_enumerate(text, limit=300000):
    """Walk every concrete trail pair explicitly (trails are labelled objects)."""
    m, n, s, l = parse(text)
    trails = [[("S", c, k) for k in range(s[c])] + [("L", c, k) for k in range(l[c])] for c in range(m)]
    alltrails = [tr for c in range(m) for tr in trails[c]]
    count = 0

    def walk(cabin, day):
        nonlocal count
        if count > limit:
            raise OverflowError
        if day == n:
            count += 1
            return
        for out in trails[cabin]:
            for back in alltrails:
                if out[0] == "S" or back[0] == "S":
                    walk(back[1], day + 1)

    walk(0, 0)
    return count % MOD


def matrix(m, s, l):
    return [[(s[i] * s[j] + s[i] * l[j] + l[i] * s[j]) % MOD for j in range(m)] for i in range(m)]


def oracle_dp(text):
    m, n, s, l = parse(text)
    A = matrix(m, s, l)
    v = [1] + [0] * (m - 1)
    for _ in range(n):
        v = [sum(v[i] * A[i][j] for i in range(m)) % MOD for j in range(m)]
    return sum(v) % MOD


def oracle_matpow(text):
    m, n, s, l = parse(text)
    A = matrix(m, s, l)

    def mul(X, Y):
        cols = list(zip(*Y))
        return [[sum(a * b for a, b in zip(row, col)) % MOD for col in cols] for row in X]

    v = [[1] + [0] * (m - 1)]
    e = n
    while e:
        if e & 1:
            v = mul(v, A)
        e >>= 1
        if e:
            A = mul(A, A)
    return sum(v[0]) % MOD


def oracle(text):
    m, n, s, l = parse(text)
    if n <= 4 and m <= 3 and max(s + l) <= 2:
        try:
            return "enumerate", oracle_enumerate(text)
        except OverflowError:
            pass
    if n * m * m <= 2_000_000:
        return "dp", oracle_dp(text)
    return "matpow", oracle_matpow(text)


def run_reference(text):
    return subprocess.run([sys.executable, str(REFERENCE)], input=text, text=True,
                          capture_output=True, check=True).stdout


def build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 21):
        attempt = 0
        case = generate(seed)
        while case in cases:
            attempt += 1
            case = generate(seed, attempt)
        cases.append(case)
    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {index}: violates input contract")
        answer = run_reference(case)
        if index == 0 and answer.split() != SAMPLE_OUT.split():
            raise SystemExit(f"sample mismatch: {answer!r}")
        how, expect = oracle(case)
        if answer.split() != [str(expect)]:
            raise SystemExit(f"case {index}: oracle ({how}) {expect} != reference {answer!r}")
        print(f"case {index}: ok ({how})")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__":
    build()
