#!/usr/bin/env python3
"""1195C Basketball Exercise: DP on two rows, diverse sizes and patterns."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "5\n9 3 5 7 3\n5 8 1 4 5\n"
SAMPLE_OUT = "29\n"
REFERENCE = Path(__file__).with_name("samplecode.py")

SIZES = (1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 30, 50, 80, 100, 200, 500, 1000, 5000, 100000)


def generate(seed, attempt=0):
    r = random.Random(1195_000_003 + seed * 9176 + attempt)
    n = SIZES[(seed - 1 + attempt) % len(SIZES)]
    mode = (seed + attempt) % 5
    h1, h2 = [], []
    if mode == 0:
        # Random heights
        h1 = [r.randint(1, 10**9) for _ in range(n)]
        h2 = [r.randint(1, 10**9) for _ in range(n)]
    elif mode == 1:
        # Row 0 dominates
        h1 = [r.randint(5*10**8, 10**9) for _ in range(n)]
        h2 = [r.randint(1, 5*10**8) for _ in range(n)]
    elif mode == 2:
        # Alternating dominance
        for i in range(n):
            if i % 2 == 0:
                h1.append(r.randint(5*10**8, 10**9))
                h2.append(r.randint(1, 10**8))
            else:
                h1.append(r.randint(1, 10**8))
                h2.append(r.randint(5*10**8, 10**9))
    elif mode == 3:
        # All same height
        v = r.randint(1, 10**9)
        h1 = [v] * n
        h2 = [v] * n
    else:
        # Small heights for variety
        h1 = [r.randint(1, 100) for _ in range(n)]
        h2 = [r.randint(1, 100) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, h1))}\n{' '.join(map(str, h2))}\n"


def valid(text):
    v = list(map(int, text.split()))
    n = v[0]
    if n < 1 or n > 100000:
        return False
    if len(v) != 1 + 2 * n:
        return False
    return all(1 <= x <= 10**9 for x in v[1:])


def build():
    out = Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 40):
        attempt = 0
        case = generate(seed)
        while case in cases:
            attempt += 1
            case = generate(seed, attempt)
        cases.append(case)
    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"invalid {index}")
        answer = subprocess.run(
            [sys.executable, str(REFERENCE)], input=case, text=True, capture_output=True, check=True
        ).stdout
        if index == 0 and answer != SAMPLE_OUT:
            raise SystemExit(f"sample mismatch: got {answer!r} expected {SAMPLE_OUT!r}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__":
    build()
