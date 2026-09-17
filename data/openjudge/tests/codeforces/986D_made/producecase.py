#!/usr/bin/env python3
"""Codeforces 986D Perfect Encoding -- generator, input contract and data build.

Statement: one positive integer n, no leading zeros, at most 1.5e6 decimal digits.
Output: min sum b_i over m >= 1 with prod b_i >= n.  Unique integer -> token-exact is fine.

Case 0 is official sample 1 (36 -> 10); seeds 1 and 2 are samples 2 and 3 (37 -> 11,
12345678901234567890123456789 -> 177); all three are asserted against the statement.

Shapes, chosen by how solutions go wrong:
  * n = 1 (answer 1, not 0) and tiny n (2, 4) where the "4 = 2+2" choice matters;
  * exact powers 3^k, 2*3^k, 4*3^k and their +-1 neighbours -- kill `<=` vs `<`
    off-by-ones and float-logarithm estimates (log3(3^k + 1) is k + 1e-20);
  * n = 4*3^k - 1 style values where using only 3s and one 2 is not optimal;
  * medium random numbers (hundreds / thousands of digits);
  * upper-bound numbers with ~1.5e6 digits (all nines, 10^1499999, max 3^k, random)
    that kill O(L^2) schoolbook big-number solutions.

Oracle (independent): dynamic programming over the partition of the cost.
best[c] = largest product of positive integers summing to c, computed with Python ints
by trying every last part (all parts 1..c for c <= FULL_DP, parts 1..8 above -- the
full-range run on the small cases shows parts > 4 never help).  The answer is the least
c >= 1 with best[c] >= n.  It is run on every case with at most ORACLE_DIGITS digits.
"""
from __future__ import annotations

import decimal
import random
import subprocess
import sys
from pathlib import Path

REFERENCE = Path(__file__).with_name("samplecode.py")
SAMPLE = "36\n"
SAMPLE_OUT = "10\n"
EXTRA_SAMPLES = {1: ("37\n", "11\n"), 2: ("12345678901234567890123456789\n", "177\n")}
MAX_DIGITS = 1_500_000
ORACLE_DIGITS = 2600
FULL_DP = 300


def _ctx(digits):
    return decimal.Context(prec=digits + 50, Emax=decimal.MAX_EMAX, Emin=decimal.MIN_EMIN,
                           traps=[decimal.Inexact, decimal.Rounded, decimal.InvalidOperation])


def big(mult, k, delta, digits_hint):
    """Decimal string of mult * 3^k + delta (exact, via libmpdec)."""
    ctx = _ctx(digits_hint)
    v = ctx.add(ctx.multiply(decimal.Decimal(mult), ctx.power(decimal.Decimal(3), k)),
                decimal.Decimal(delta))
    return format(v, "f")


def max_k(mult, digits=MAX_DIGITS):
    # largest k with mult*3^k (+1) having at most `digits` digits (checked below)
    import math
    k = int((digits - 1 - math.log10(mult)) / math.log10(3))
    while len(big(mult, k + 1, 1, digits + 10)) <= digits:
        k += 1
    while len(big(mult, k, 1, digits + 10)) > digits:
        k -= 1
    return k


def generate(seed):
    r = random.Random(986_004 + seed * 7919)
    if seed in EXTRA_SAMPLES:
        return EXTRA_SAMPLES[seed][0]
    if seed == 3:
        return "1\n"
    if seed == 4:
        return "4\n"
    if seed == 5:
        return f"{r.randint(5, 1000)}\n"
    if seed == 6:
        return big(1, 40, 0, 40) + "\n"                 # exact power of 3
    if seed == 7:
        return big(1, 40, 1, 40) + "\n"                 # just above a power of 3
    if seed == 8:
        return big(2, 55, 0, 40) + "\n"
    if seed == 9:
        return big(4, 70, 1, 60) + "\n"
    if seed == 10:
        return big(4, 100, -1, 60) + "\n"               # 3s-and-one-2 is not optimal
    if seed == 11:
        return str(r.randint(1, 9)) + "".join(r.choice("0123456789") for _ in range(299)) + "\n"
    if seed == 12:
        return big(1, 2000, -1, 1000) + "\n"            # 999...-like just below 3^2000
    if seed == 13:
        return big(2, 2500, 1, 1300) + "\n"
    if seed == 14:
        return str(r.randint(1, 9)) + "".join(r.choice("0123456789") for _ in range(2499)) + "\n"
    if seed == 15:
        return "9" * MAX_DIGITS + "\n"
    if seed == 16:
        return big(1, max_k(1), 0, MAX_DIGITS) + "\n"
    if seed == 17:
        return big(4, max_k(4), -1, MAX_DIGITS) + "\n"
    if seed == 18:
        return big(2, max_k(2), 1, MAX_DIGITS) + "\n"
    if seed == 19:
        return "1" + "0" * (MAX_DIGITS - 1) + "\n"
    # seed 20: random full-length number
    return str(r.randint(1, 9)) + "".join(r.choices("0123456789", k=MAX_DIGITS - 1)) + "\n"


def valid(text):
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    s = text[:-1]
    return (1 <= len(s) <= MAX_DIGITS and s.isascii() and s.isdigit()
            and s[0] != "0")


def oracle(text):
    s = text.strip()
    sys.set_int_max_str_digits(0)
    n = int(s)
    best = [0, 1]            # best[c]: max product of positive parts summing to c
    c = 1
    while best[c] < n:
        c += 1
        top = c if c <= FULL_DP else 8
        v = c                # single part
        for last in range(1, min(top, c - 1) + 1):
            v = max(v, best[c - last] * last)
        best.append(v)
    return f"{c}\n"


def build():
    out = Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    for path in out.glob("*"):
        path.unlink()
    cases = [SAMPLE] + [generate(seed) for seed in range(1, 21)]
    if len(set(cases)) != len(cases):
        raise SystemExit("duplicate inputs")
    checked = 0
    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {index} violates the input contract")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, check=True, timeout=60).stdout
        if index == 0 and answer.split() != SAMPLE_OUT.split():
            raise SystemExit(f"sample mismatch: {answer!r}")
        if index in EXTRA_SAMPLES and answer.split() != EXTRA_SAMPLES[index][1].split():
            raise SystemExit(f"sample {index} mismatch: {answer!r}")
        if len(case) - 1 <= ORACLE_DIGITS:
            if oracle(case).split() != answer.split():
                raise SystemExit(f"oracle disagreement on case {index}")
            checked += 1
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")
    print(f"built {len(cases)} cases, {checked} oracle-checked")


if __name__ == "__main__":
    build()
