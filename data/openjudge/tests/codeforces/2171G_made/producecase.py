#!/usr/bin/env python3
"""Codeforces 2171G Sakura Adachi and Optimal Sequences -- generator, contract, oracles, build.

Written for this repository as a hand-off artifact; no external license.

Statement: t (1..1e4) tests; each n (2..2e5), a_1..a_n (1..1e6), b_1..b_n (a_i..1e6); sum n <=
2e5.  Operations: a_i += 1, or double all of a.  Print the minimum operation count x (exactly)
and the number of length-x sequences reaching b, modulo 1e6+3.

The reference is C++ (samplecode.cpp, compiled with g++ -O2 during build): ~20 doubling counts
times n = 2e5 is several seconds in pure Python.

Shapes (how solutions go wrong):
  * tiny_bfs     -- t=1e4 tiny tests, both numbers checked by BFS over array states.
  * near_power   -- b_i close to a_i*2^k: stage counts after doublings matter (kills solutions
                    that drop the per-stage factorials or ignore the stage structure).
                    Note: since n >= 2, one extra doubling lowers the per-index cost by >= 1 for
                    every index, so the cost is strictly decreasing in k and the max feasible k
                    is always the unique optimum -- "sum over tied k" can never be tested; these
                    shapes instead target the max-feasible-k computation (min over indices).
  * greedy_k     -- one index limits k (a_0*2^K just fits) while others would allow more.
  * all_equal    -- a == b (x = 0, count 1) and one a_i == b_i = 1e6 forcing k = 0.
  * near_p       -- k forced to 0 and sum of increments = p-1, p, p+1 ... : multinomials with
                    N >= p vanish mod p, N = p-1 does not (kills naive factorial mod p).
  * big_x        -- k forced to 0 with n = 2e5 so x ~ 2e11 (32-bit overflow, "x mod p").
  * upper bound  -- n = 2e5 random full range; a = 1, b = 1e6 (k = 19); many medium tests.
Oracles (independent of the reference's bit decomposition + Lucas):
  1. BFS over whole arrays counting shortest paths (tests with small n and b).
  2. For tests where some 2*a_i > b_i (no doubling possible): x = sum(b-a) and the count is the
     exact big-integer multinomial via math.comb, reduced mod p at the end.
  3. For medium tests: x recomputed with a per-index DP over (doublings used, value).
"""
from __future__ import annotations
import math
import random
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "samplecode.cpp"
P = 10 ** 6 + 3
MAXV = 10 ** 6
SAMPLE = """8
6
1 3 6 4 3 2
3 7 10 4 4 8
2
1 1
4 3
5
2 3 2 5 1
18 13 10 30 7
5
5 4 3 6 2
100 125 231 113 107
4
2 2 2 2
2 2 2 2
4
1 1 1 1
2 2 2 2
7
1 1 1 1 1 1 200000
200000 200000 200000 200000 200000 200000 200000
3
542264 174876 441510
641112 325241 995342
"""
SAMPLE_OUT = "17 827116\n3 1\n12 288\n35 567812\n0 1\n1 1\n1199994 0\n803045 366998\n"


def test(a, b):
    return f"{len(a)}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"


def pack(tests):
    return f"{len(tests)}\n" + "".join(tests)


def rand_test(r, n, amax, bmax):
    a = [r.randint(1, amax) for _ in range(n)]
    return test(a, [r.randint(x, max(x, bmax)) for x in a])


def near_power_test(r, n):
    # b_i = a_i*2^k + small remainder: exercises every post-doubling stage.
    k = r.randint(1, 3); a = [r.randint(1, 3) for _ in range(n)]
    b = [x * (1 << k) + r.randint(0, (1 << k)) for x in a]
    return test(a, b)


def forced_k0(r, n, total, rng=None):
    """k=0 forced by a_1 = b_1 = MAXV; remaining increments sum to `total`."""
    rest = n - 1; ds = [0] * rest; left = total
    for i in range(rest):
        cap = MAXV - 1
        lo = max(0, left - cap * (rest - i - 1)); hi = min(cap, left)
        ds[i] = hi if i == rest - 1 else (rng or r).randint(lo, hi)
        left -= ds[i]
    assert left == 0
    a = [MAXV] + [1] * rest; b = [MAXV] + [1 + d for d in ds]
    return test(a, b)


def generate(seed):
    r = random.Random(2171_0007 * 1000 + seed)
    if seed == 1:   # t = 1e4 tiny, BFS
        return pack([rand_test(r, 2, 4, 9) for _ in range(10000)])
    if seed == 2:   # n = 2 minimum, single test
        return pack([test([1, 1], [2, 2])])
    if seed == 3:   # near-power, tiny, BFS
        return pack([near_power_test(r, r.randint(2, 3)) for _ in range(1500)])
    if seed == 4:   # n=3..4, small values, BFS
        return pack([rand_test(r, r.randint(3, 4), 3, 10) for _ in range(600)])
    if seed == 5:   # K limited by index 0: a_0*2^K just <= b_0
        tests = []
        for _ in range(1500):
            n = r.randint(2, 3); a = [r.randint(1, 3) for _ in range(n)]; K = r.randint(1, 3)
            b = [x * (1 << K) + r.randint(0, 2) for x in a]
            b[0] = a[0] * (1 << K) + (1 << K) - 1
            tests.append(test(a, [min(y, 14) if min(y, 14) >= x else y for x, y in zip(a, b)]))
        return pack(tests)
    if seed == 6:   # all-equal and k forced to 0
        tests = [test([5, 5], [5, 5]), test([MAXV, 1], [MAXV, MAXV]), test([1, 1], [1, 3]),
                 test([MAXV] * 3, [MAXV] * 3)]
        tests += [test(a, a) for a in ([r.randint(1, MAXV) for _ in range(r.randint(2, 6))] for _ in range(200))]
        tests += [rand_test(r, 2, 6, 11) for _ in range(300)]
        return pack(tests)
    if seed == 7:   # near p multinomials (exact bigint oracle)
        tests = [forced_k0(r, 3, tot) for tot in (P - 2, P - 1, P, P + 1)]
        tests += [forced_k0(r, 4, 1999998), forced_k0(r, 2, 999999), forced_k0(r, 2, 1)]
        tests += [forced_k0(r, r.randint(2, 8), r.randint(0, 3000)) for _ in range(40)]
        return pack(tests)
    if seed == 8:   # medium tests, x checked by DP
        return pack([rand_test(r, r.randint(2, 6), 50, 400) for _ in range(300)])
    if seed == 9:   # big x: forced k=0, n=2e5, full increments
        return pack([forced_k0(r, 200000, 199999 * (MAXV - 1))])
    if seed == 10:  # a=1, b=1e6 everywhere (k up to 19)
        return pack([test([1] * 200000, [MAXV] * 200000)])
    if seed == 11:  # random full range, one test
        return pack([rand_test(r, 200000, MAXV, MAXV)])
    if seed == 12:  # small a, large b (many doublings, stage multinomials)
        return pack([rand_test(r, 200000, 3, MAXV)])
    if seed == 13:  # t = 1e4, n = 20, random full range
        return pack([rand_test(r, 20, MAXV, MAXV) for _ in range(10000)])
    if seed == 14:  # b close to a*2^k with small noise, large n
        n = 200000; k = 5; a = [r.randint(1, 30000) for _ in range(n)]
        return pack([test(a, [x * (1 << k) + r.randint(0, 40) for x in a])])
    if seed == 15:  # forced k0 with sum just below p at scale
        return pack([forced_k0(r, 1000, P - 1), forced_k0(r, 1000, P), forced_k0(r, 50000, 60000)])
    if seed == 16:  # a = b except few indices
        n = 199997; a = [r.randint(1, MAXV) for _ in range(n)]; b = a[:]
        for i in r.sample(range(n), 50): b[i] = min(MAXV, b[i] + r.randint(1, 1000))
        return pack([test(a, b), test([1] * 3, [1, 2, 3])])
    if seed == 17:  # near-power at medium size, BFS on the tiny ones
        return pack([near_power_test(r, r.randint(2, 3)) if i % 2 else near_power_test(r, r.randint(10, 200)) for i in range(2000)])
    if seed == 18:  # many small tests near value bound (a in upper half -> k=0)
        return pack([rand_test(r, 10, MAXV, MAXV) if i % 2 else test([MAXV // 2 + 1] * 2, [MAXV, MAXV]) for i in range(10000)])
    if seed == 19:  # powers of two, a=1, b=2^j
        tests = []
        for i in range(2000):
            n = r.randint(2, 100); tests.append(test([1] * n, [1 << r.randint(0, 19) for _ in range(n)]))
        return pack(tests)
    # seed 20: t = 1e4 mixed tiny adversarial (BFS)
    tests = []
    for i in range(10000):
        k = i % 3
        tests.append([rand_test(r, 2, 3, 12), near_power_test(r, 2), rand_test(r, 3, 2, 6)][k])
    return pack(tests)


def parse(text):
    tok = text.split(); p = 1; res = []
    for _ in range(int(tok[0])):
        n = int(tok[p]); p += 1
        a = list(map(int, tok[p:p + n])); p += n
        b = list(map(int, tok[p:p + n])); p += n
        res.append((a, b))
    return res


def valid(text):
    try:
        if not text.endswith("\n"):
            return False
        lines = text.split("\n")[:-1]; li = 0
        t = int(lines[0]); li = 1
        if lines[0] != str(t) or not 1 <= t <= 10000:
            return False
        total = 0
        for _ in range(t):
            n = int(lines[li]); li += 1
            if lines[li - 1] != str(n) or not 2 <= n <= 200000:
                return False
            total += n
            a = list(map(int, lines[li].split())); b = list(map(int, lines[li + 1].split())); li += 2
            if len(a) != n or len(b) != n:
                return False
            if not all(1 <= x <= MAXV and x <= y <= MAXV for x, y in zip(a, b)):
                return False
        return li == len(lines) and total <= 200000
    except (ValueError, IndexError):
        return False


BFS_STATES = 3000
K0_BIG = 6          # exact multinomials with ~1e6 factorial digits cost seconds each


def bfs_oracle(a, b):
    """Shortest-path counting over whole-array states."""
    target = tuple(b); cur = {tuple(a): 1}; seen = {tuple(a)}; steps = 0
    while target not in cur:
        nxt = {}
        for s, c in cur.items():
            moves = []
            for i in range(len(s)):
                if s[i] < b[i]:
                    moves.append(s[:i] + (s[i] + 1,) + s[i + 1:])
            if all(2 * x <= y for x, y in zip(s, b)):
                moves.append(tuple(2 * x for x in s))
            for m in moves:
                if m not in seen:
                    nxt[m] = nxt.get(m, 0) + c
        seen.update(nxt); cur = nxt; steps += 1
    return steps, cur[target] % P


def bfs_feasible(a, b):
    return math.prod(y - x + 1 for x, y in zip(a, b)) <= BFS_STATES


def k0_oracle(a, b):
    ds = [y - x for x, y in zip(a, b)]; ways = 1; pref = 0
    for d in ds:
        pref += d; ways *= math.comb(pref, d)
    return sum(ds), ways % P


def dp_x_oracle(a, b):
    K = 0
    while all(x << (K + 1) <= y for x, y in zip(a, b)):
        K += 1
    best = None
    for k in range(K + 1):
        tot = k
        for x, y in zip(a, b):
            # h[v] = min increments to reach v from x using exactly j doublings
            h = {v: v - x for v in range(x, y + 1)}
            for j in range(1, k + 1):
                lo = x << j; g = {}
                for v in range(lo, y + 1):
                    c = h.get(v // 2) if v % 2 == 0 else None
                    prev = g.get(v - 1)
                    opts = [o for o in (c, None if prev is None else prev + 1) if o is not None]
                    g[v] = min(opts)
                h = g
            tot += h[y]
        best = tot if best is None else min(best, tot)
    return best


def build():
    out = HERE / "data"; out.mkdir(exist_ok=True)
    for f in out.glob("*"):
        f.unlink()
    tmp = Path(tempfile.mkdtemp()); exe = tmp / "ref"
    subprocess.run(["g++", "-O2", "-o", str(exe), str(SOURCE)], check=True, stderr=subprocess.DEVNULL)
    cases = [SAMPLE] + [generate(s) for s in range(1, 21)]
    if len(set(cases)) != len(cases):
        raise SystemExit("duplicate inputs")
    checked_cases = 0
    for idx, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {idx} violates the input contract")
        res = subprocess.run([str(exe)], input=case, text=True, capture_output=True, check=True, timeout=60)
        if idx == 0 and res.stdout.split() != SAMPLE_OUT.split():
            raise SystemExit(f"sample mismatch: {res.stdout!r}")
        tests = parse(case); got = list(map(int, res.stdout.split()))
        if len(got) != 2 * len(tests):
            raise SystemExit(f"case {idx}: wrong answer count")
        nb = nk = nd = big_k0 = 0
        for i, (a, b) in enumerate(tests):
            mine = (got[2 * i], got[2 * i + 1])
            if bfs_feasible(a, b):
                if bfs_oracle(a, b) != mine:
                    raise SystemExit(f"case {idx} test {i}: BFS oracle disagreement {bfs_oracle(a, b)} {mine}")
                nb += 1
            dsum = sum(y - x for x, y in zip(a, b))
            if any(2 * x > y for x, y in zip(a, b)) and len(a) <= 1000 and (
                    dsum <= 20000 or (len(a) <= 4 and dsum <= 2_100_000 and big_k0 < K0_BIG)):
                big_k0 += dsum > 20000
                if k0_oracle(a, b) != mine:
                    raise SystemExit(f"case {idx} test {i}: k=0 bigint oracle disagreement")
                nk += 1
            if len(a) <= 6 and max(b) <= 400:
                if dp_x_oracle(a, b) != mine[0]:
                    raise SystemExit(f"case {idx} test {i}: DP x oracle disagreement")
                nd += 1
        checked_cases += (nb + nk + nd) > 0
        print(f"case {idx}: {len(tests)} tests, bfs {nb}, k0-bigint {nk}, dp-x {nd}", file=sys.stderr)
        (out / f"{idx}.in").write_text(case); (out / f"{idx}.out").write_text(res.stdout)
    exe.unlink(); tmp.rmdir()
    print(f"oracle-checked cases: {checked_cases}", file=sys.stderr)


if __name__ == "__main__":
    build()
