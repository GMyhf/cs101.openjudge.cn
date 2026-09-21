#!/usr/bin/env python3
"""Codeforces 2146D1 Max Sum OR (Easy Version) -- generator, input contract, oracle, build.

Written for this repository as a hand-off artifact; no external license.

Answers are not unique, so the problem is judged by checker.py (next to data/).
The checker assumes the optimum is r(r+1) for every r; the oracle below verifies that
independently: exhaustive bitmask DP over all assignments for r <= DP_MAX and a Kuhn
bipartite matching on the "a & i == 0" graph for r <= KUHN_MAX (a perfect matching
exists  <=>  the upper bound r(r+1) is reached).

Shapes target the ways solutions go wrong:
  * r = 2^k - 1 (the complement pairing is forced), r = 2^k and 2^k + 1 (the top bit
    has a single / two owners), r = 0 (n = 1) and r = 1;
  * every r in 0..511 in one file (all recursion depths / leftovers);
  * t = 10^4 tiny tests (reading only the first test, per-test resets);
  * max r = 199999 and 199998, big powers of two mixed with remainders;
  * int overflow of r(r+1) in 32-bit (r ~ 2e5 gives ~4e10).
Case 0 is the official sample; the checker must accept the official output as well.
"""
from __future__ import annotations
import random
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
CHECKER = HERE / "checker.py"
SAMPLE = "3\n0 3\n0 9\n0 15\n"
SAMPLE_OUT = "12\n3 2 1 0 \n90\n7 8 5 4 3 2 9 0 1 6\n240\n15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0\n"
MAXSUM = 200000
MAXT = 10000
DP_MAX = 13
KUHN_MAX = 511
# .out files are capped at 1 MB for this repository; an array of 2e5 six-digit numbers
# is ~1.3 MB, so the largest single tests use r = BIG (still 18 bits, like 199999).
BIG = 150000


def fmt(rs):
    return f"{len(rs)}\n" + "".join(f"0 {r}\n" for r in rs)


def fill(r, rs, lo, hi, budget=MAXSUM):
    used = sum(x + 1 for x in rs)
    while len(rs) < MAXT and used < budget:
        x = min(r.randint(lo, hi), budget - used - 1)
        rs.append(x); used += x + 1
    return rs


def generate(seed):
    r = random.Random(2146_0401 * 97 + seed)
    rs = []
    if seed == 1:          # all tiny r, oracle-exhaustive
        rs = list(range(0, 20)); r.shuffle(rs)
    elif seed == 2:        # t = 1e4 tiny random
        rs = [r.randint(0, 20) for _ in range(MAXT)]
    elif seed == 3:        # every r in 0..511
        rs = list(range(512)); r.shuffle(rs)
    elif seed == 4:        # max single
        rs = [BIG]
    elif seed == 5:        # all-ones r (forced pairing) at scale
        rs = [131071, 16383, 1023, 319]
    elif seed == 6:        # powers of two: top bit owned by a single number
        rs = [1 << k for k in range(17)]
    elif seed == 7:        # 2^k + 1 and 2^k - 2
        rs = []
        for k in range(1, 16):
            rs += [(1 << k) + 1, (1 << k) - 2]
        rs = fill(r, rs, 0, 3000)
    elif seed == 8:        # large powers of two plus small remainder
        rs = [131072]
        rs = fill(r, rs, 0, 60, BIG + 1)
    elif seed == 9:        # t = 1e4 of r in {0, 1, 2}
        rs = [r.choice([0, 1, 1, 2]) for _ in range(MAXT)]
    elif seed == 10:       # medium random
        rs = fill(r, [], 1000, 30000, BIG + 1)
    elif seed == 11:       # max even r (odd n)
        rs = [BIG - 1]
    elif seed == 12:
        rs = [100000, BIG - 100002]
    elif seed == 13:       # t = 1e4, r up to 38
        rs = fill(r, [], 0, 38)
    elif seed == 14:       # every 2^k - 1 and 2^k - 2
        rs = [(1 << k) - 1 for k in range(17)] + [(1 << k) - 2 for k in range(2, 15)]
        rs = fill(r, rs, 0, 500, 170000)
    elif seed == 15:       # 3 * 2^k - 1 and 3 * 2^k
        rs = []
        for k in range(0, 14):
            rs += [3 * (1 << k) - 1, 3 * (1 << k)]
        rs = fill(r, rs, 0, 200)
    elif seed == 16:       # many oracle-sized random r
        rs = [r.randint(100, KUHN_MAX) for _ in range(600)]
        while sum(x + 1 for x in rs) > MAXSUM:
            rs.pop()
    elif seed == 17:       # ascending small r
        rs = []; used = 0; x = 0
        while used + x + 1 <= MAXSUM and len(rs) < MAXT:
            rs.append(x); used += x + 1; x += 1
    elif seed == 18:
        rs = [140000, BIG - 140002]
    elif seed == 19:       # random large mixture
        rs = fill(r, [], 0, BIG, BIG + 1)
    elif seed == 20:       # t = 1e4, r = 19 each (sum n exactly 2e5)
        rs = [19] * MAXT
    else:                  # seeds 21+: random mixtures
        mode = (seed - 21) % 5
        if mode == 0:
            rs = [r.randint(0, BIG) for _ in range(min(MAXT, 500))]
        elif mode == 1:
            rs = [r.randint(0, 38) for _ in range(MAXT)]
        elif mode == 2:
            rs = [(1 << r.randint(1, 17)) - r.randint(0, 2) for _ in range(300)]
        elif mode == 3:
            rs = [r.randint(100, KUHN_MAX) for _ in range(400)]
        else:
            rs = fill(r, [], 0, BIG, BIG + 1)
        while sum(x + 1 for x in rs) > MAXSUM:
            rs.pop()
    assert sum(x + 1 for x in rs) <= MAXSUM and len(rs) <= MAXT
    return fmt(rs)


# ---------------------------------------------------------------- contract
def valid(text):
    try:
        lines = text.split("\n")
        if lines[-1] != "":
            return False
        lines = lines[:-1]
        t = int(lines[0])
        if lines[0] != str(t) or not 1 <= t <= MAXT or len(lines) != t + 1:
            return False
        total = 0
        for line in lines[1:]:
            parts = line.split(" ")
            if len(parts) != 2:
                return False
            l, rr = int(parts[0]), int(parts[1])
            if line != f"{l} {rr}" or l != 0 or not l <= rr < MAXSUM:
                return False
            total += rr - l + 1
        return total <= MAXSUM
    except (ValueError, IndexError):
        return False


# ---------------------------------------------------------------- oracle
_DP = {}
_KUHN = {}


def dp_best(r):
    """max over all permutations of sum(a_i | i), exhaustive DP over assigned values."""
    if r not in _DP:
        n = r + 1
        f = [-1] * (1 << n)
        f[0] = 0
        for mask in range(1 << n):
            if f[mask] < 0:
                continue
            i = bin(mask).count("1")
            if i == n:
                continue
            for v in range(n):
                if not mask >> v & 1:
                    nm = mask | 1 << v
                    c = f[mask] + (v | i)
                    if c > f[nm]:
                        f[nm] = c
        _DP[r] = f[(1 << n) - 1]
    return _DP[r]


def kuhn_perfect(r):
    """does a permutation with a_i & i == 0 for all i exist?  (Kuhn's matching)"""
    if r not in _KUHN:
        n = r + 1
        adj = [[v for v in range(n) if v & i == 0] for i in range(n)]
        match = [-1] * n
        sys.setrecursionlimit(10000)

        def aug(i, seen):
            for v in adj[i]:
                if not seen[v]:
                    seen[v] = True
                    if match[v] < 0 or aug(match[v], seen):
                        match[v] = i
                        return True
            return False
        _KUHN[r] = all(aug(i, [False] * n) for i in range(n))
    return _KUHN[r]


def oracle(text):
    toks = text.split()
    rs = [int(toks[2 + 2 * i]) for i in range(int(toks[0]))]
    if max(rs) > KUHN_MAX:
        return None
    for r in rs:
        best = r * (r + 1)
        if r <= DP_MAX and dp_best(r) != best:
            raise SystemExit(f"oracle: DP optimum for r={r} is {dp_best(r)}, checker assumes {best}")
        if not kuhn_perfect(r):
            raise SystemExit(f"oracle: no AND-free permutation for r={r}")
    return True


def run_checker(inp, out):
    with tempfile.TemporaryDirectory() as d:
        paths = []
        for name, data in (("in", inp), ("out", out), ("ans", out)):
            p = Path(d) / name; p.write_text(data); paths.append(str(p))
        res = subprocess.run([sys.executable, "-I", str(CHECKER), *paths], capture_output=True, text=True)
    return res.returncode, res.stdout.strip()


# ---------------------------------------------------------------- build
def build():
    out = HERE / "data"; out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 40):
        case = generate(seed)
        assert case not in cases, seed
        cases.append(case)
    code, msg = run_checker(SAMPLE, SAMPLE_OUT)
    if code != 0:
        raise SystemExit(f"checker rejects the official sample output: {msg}")
    checked = 0
    for idx, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {idx}: input contract violated")
        ans = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                             capture_output=True, check=True).stdout
        code, msg = run_checker(case, ans)
        if code != 0:
            raise SystemExit(f"case {idx}: checker rejects the reference ({code}): {msg}")
        if idx == 0:   # values (not arrays) must match the official sample
            vals = [ln for k, ln in enumerate(ans.split("\n")) if k % 2 == 0 and ln]
            if vals != ["12", "90", "240"]:
                raise SystemExit(f"sample values mismatch: {vals}")
        o = oracle(case)
        checked += o is not None
        if len(case) > 3 << 20 or len(ans) > 1 << 20:
            raise SystemExit(f"case {idx}: too large")
        (out / f"{idx}.in").write_text(case, encoding="utf-8")
        (out / f"{idx}.out").write_text(ans, encoding="utf-8")
        print(f"case {idx}: in={len(case)}B out={len(ans)}B oracle={'yes' if o else 'no'}")
    print(f"oracle-checked {checked}/21")


if __name__ == "__main__":
    build()
