#!/usr/bin/env python3
"""1970E3 Trails (Hard) -- generator, input contract, oracles and data build.

Statement: m cabins (1 <= m <= 1e5), n days (1 <= n <= 1e9), 0 <= s_i, l_i <= 1000,
and "Each cabin is connected, with one or more trails" (so s_i + l_i >= 1 is kept).
Answer = number of trail sequences starting at cabin 1, modulo 1e9+7.

Shapes are chosen around how solutions go wrong:
  * O(m^2) / O(m^3 log n) matrix solutions: m = 1e5 with n = 1e9.
  * forgetting "at least one of the two trails has to be short" (t_i*t_j): long trails present;
    no-short-trail cases where the answer is 0.
  * off-by-one in days: n = 1, n = 2.
  * dropping one cross term (s_i*t_j): lopsided s / l.
  * ignoring start cabin 1: cabin 1 made special.
  * intermediate overflow of sums like sum(t_i^2) (up to 4e11) in 64-bit-careless code.

Answers come from samplecode.py (2x2 reduction).  Independent oracle, run in build:
cabins are grouped into classes of identical (s_i, l_i) (cabin 1 is always its own class);
the class-level transfer matrix is built straight from the definition
(count_q * (s_p s_q + s_p l_q + l_p s_q)) and then walked by explicit trail enumeration
(tiny), day-by-day DP, or K x K matrix fast power.  Every case with <= 100 classes is
checked; big cases are drawn from small value palettes so most of them are checked too.
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
MAX_M, MAX_N, MAX_V = 100_000, 10**9, 1000
ORACLE_MAX_CLASSES = 100


def fmt(n, s, l):
    return f"{len(s)} {n}\n{' '.join(map(str, s))}\n{' '.join(map(str, l))}\n"


def fix_zero(r, s, l):
    for i in range(len(s)):
        if s[i] + l[i] == 0:
            (s if r.random() < 0.5 else l)[i] = r.randint(1, 1000)
    return s, l


def rand_vals(r, m, lo=0, hi=MAX_V):
    return fix_zero(r, [r.randint(lo, hi) for _ in range(m)], [r.randint(lo, hi) for _ in range(m)])


def palette_vals(r, m, k):
    pal = []
    while len(pal) < k:
        p = (r.randint(0, 1000), r.randint(0, 1000))
        if sum(p) and p not in pal:
            pal.append(p)
    pairs = [r.choice(pal) for _ in range(m)]
    return [p[0] for p in pairs], [p[1] for p in pairs]


def generate(seed, attempt=0):
    r = random.Random(1970_300_000 + seed * 7919 + attempt * 104729)
    M = MAX_M
    if seed == 1:      # m=1, only a long trail -> 0
        return fmt(1, [0], [1])
    if seed == 2:      # m=1, max everything
        return fmt(MAX_N, [1000], [1000])
    if seed == 3:      # m = 1e5 all maximal, n = 1e9
        return fmt(MAX_N, [1000] * M, [1000] * M)
    if seed == 4:      # m = 1e5 no short trails -> 0
        return fmt(MAX_N, [0] * M, [r.choice([1, 1000]) for _ in range(M)])
    if seed == 5:      # m = 1e5 no long trails, rank 1
        return fmt(MAX_N, [r.choice([1, 999, 1000]) for _ in range(M)], [0] * M)
    if seed == 6:      # m = 1e5, n = 1, palette
        s, l = palette_vals(r, M, 60); return fmt(1, s, l)
    if seed == 7:      # m = 1e5, n = 2, palette
        s, l = palette_vals(r, M, 40); return fmt(2, s, l)
    if seed == 8:      # m = 1e5, cabin 1 long only, palette, n huge
        s, l = palette_vals(r, M, 80); s[0], l[0] = 0, 1000; return fmt(MAX_N - r.randint(0, 99), s, l)
    if seed == 9:      # m = 1e5, only cabin 1 has short trails
        s = [1000] + [0] * (M - 1); l = [0] + [r.choice([1, 500, 1000]) for _ in range(M - 1)]
        return fmt(MAX_N, s, l)
    if seed == 10:     # m = 1e5, s tiny / l large palette
        pal = [(a, b) for a in range(3) for b in (900, 950, 1000)]
        pairs = [r.choice(pal) for _ in range(M)]
        return fmt(r.randint(MAX_N // 2, MAX_N), [p[0] for p in pairs], [p[1] for p in pairs])
    if seed == 11:     # m = 1e5 full random (not oracle-checked: too many classes)
        s, l = rand_vals(r, M); return fmt(r.randint(MAX_N // 2, MAX_N), s, l)
    if seed == 12:     # m = 1e5 full random, s large l tiny (not oracle-checked)
        s = [r.randint(900, 1000) for _ in range(M)]; l = [r.randint(0, 3) for _ in range(M)]
        return fmt(MAX_N - 1, s, l)
    if seed == 13:     # random m in [50000, 1e5], random n (not oracle-checked)
        s, l = rand_vals(r, r.randint(50_000, M)); return fmt(r.randint(1, MAX_N), s, l)
    if seed == 14:     # tiny enumeration
        m = 3; s = [r.randint(0, 2) for _ in range(m)]; l = [r.randint(0, 2) for _ in range(m)]
        for i in range(m):
            if s[i] + l[i] == 0: s[i] = 1
        return fmt(3, s, l)
    if seed == 15:     # small m, moderate n, DP
        s, l = rand_vals(r, r.randint(5, 15)); return fmt(r.randint(20, 200), s, l)
    if seed == 16:     # m = 100 random, n = 1e9
        s, l = rand_vals(r, 100); return fmt(MAX_N, s, l)
    if seed == 17:     # m = 2 short-only / long-only
        return fmt(MAX_N, [r.randint(1, 1000), 0], [0, r.randint(1, 1000)])
    if seed == 18:     # m = 1e5 with cabin 1 duplicated in value elsewhere, power-of-two n
        s, l = palette_vals(r, M, 20); return fmt(2**29, s, l)
    if seed == 19:     # tiny enumeration, n = 4
        return fmt(4, [1, 0], [r.randint(0, 1), 1])
    # seed 20: m = 1e5 of 0/1 values
    s = [r.randint(0, 1) for _ in range(M)]; l = [1 - x if r.random() < 0.6 else 1 for x in s]
    return fmt(r.randint(1, MAX_N), s, l)


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
    if not all(0 <= x <= MAX_V for x in s) or not all(0 <= x <= MAX_V for x in l):
        return False
    return all(a + b >= 1 for a, b in zip(s, l))   # "connected with one or more trails"


def parse(text):
    tok = list(map(int, text.split()))
    m, n = tok[0], tok[1]
    return m, n, tok[2:2 + m], tok[2 + m:2 + 2 * m]


def classes(m, s, l):
    """Class 0 = cabin 1 alone; other classes = identical (s, l) pairs among cabins 2..m."""
    keys = [(s[0], l[0])]
    count = [1]
    index = {}
    for i in range(1, m):
        key = (s[i], l[i])
        if key not in index:
            index[key] = len(keys); keys.append(key); count.append(0)
        count[index[key]] += 1
    return keys, count


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


def class_matrix(keys, count):
    k = len(keys)
    return [[count[q] * (keys[p][0] * keys[q][0] + keys[p][0] * keys[q][1] + keys[p][1] * keys[q][0]) % MOD
             for q in range(k)] for p in range(k)]


def oracle_dp(n, A):
    k = len(A)
    v = [1] + [0] * (k - 1)
    for _ in range(n):
        v = [sum(v[i] * A[i][j] for i in range(k)) % MOD for j in range(k)]
    return sum(v) % MOD


def oracle_matpow(n, A):
    def mul(X, Y):
        cols = list(zip(*Y))
        return [[sum(a * b for a, b in zip(row, col)) % MOD for col in cols] for row in X]

    v = [[1] + [0] * (len(A) - 1)]
    e = n
    while e:
        if e & 1:
            v = mul(v, A)
        e >>= 1
        if e:
            A = mul(A, A)
    return sum(v[0]) % MOD


def oracle(text):
    """Return (method, answer) or (None, None) when no oracle is feasible."""
    m, n, s, l = parse(text)
    if n <= 4 and m <= 3 and max(s + l) <= 2:
        try:
            return "enumerate", oracle_enumerate(text)
        except OverflowError:
            pass
    keys, count = classes(m, s, l)
    if len(keys) > ORACLE_MAX_CLASSES:
        return None, None
    A = class_matrix(keys, count)
    if n * len(keys) ** 2 <= 2_000_000:
        return "dp", oracle_dp(n, A)
    return "matpow", oracle_matpow(n, A)


def run_reference(text):
    return subprocess.run([sys.executable, str(REFERENCE)], input=text, text=True,
                          capture_output=True, check=True).stdout


def build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 40):
        attempt = 0
        case = generate(seed)
        while case in cases:
            attempt += 1
            case = generate(seed, attempt)
        cases.append(case)
    checked = 0
    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {index}: violates input contract")
        answer = run_reference(case)
        if index == 0 and answer.split() != SAMPLE_OUT.split():
            raise SystemExit(f"sample mismatch: {answer!r}")
        how, expect = oracle(case)
        if how is not None:
            if answer.split() != [str(expect)]:
                raise SystemExit(f"case {index}: oracle ({how}) {expect} != reference {answer!r}")
            checked += 1
        print(f"case {index}: {'ok (' + how + ')' if how else 'no oracle'}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")
    if checked < 15:
        raise SystemExit(f"only {checked} oracle-checked cases")


if __name__ == "__main__":
    build()
