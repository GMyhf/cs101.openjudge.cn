#!/usr/bin/env python3
"""466C Number of Ways: split array into 3 equal-sum parts, diverse patterns."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "5\n1 2 3 0 3\n"
SAMPLE_OUT = "2\n"
REFERENCE = Path(__file__).with_name("samplecode.py")

SIZES = (3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 50, 80, 100, 200, 500, 1000, 5000, 100000, 500000)


def generate(seed, attempt=0):
    r = random.Random(466_000_003 + seed * 9176 + attempt)
    n = SIZES[(seed - 1 + attempt) % len(SIZES)]
    mode = (seed - 1 + attempt) % 6

    if mode == 0:
        # All zeros - many ways
        a = [0] * n
    elif mode == 1:
        # Constructed to have exactly one way
        third = n // 3
        a = [0] * n
        a[0] = 1
        a[third] = -1
        a[third + 1] = 1
        if 2 * third + 1 < n:
            a[2 * third + 1] = -1
    elif mode == 2:
        # Random values, sum divisible by 3
        a = [r.randint(-10**9, 10**9) for _ in range(n)]
        s = sum(a) % 3
        if s != 0:
            a[0] += (3 - s) % 3
    elif mode == 3:
        # All same positive value
        v = r.randint(1, 100)
        a = [v] * n
        # Sum = n*v, need n*v % 3 == 0
        if (n * v) % 3 != 0:
            a[-1] += (3 - (n * v) % 3) % 3
    elif mode == 4:
        # Alternating +1, -1
        a = [1 if i % 2 == 0 else -1 for i in range(n)]
        s = sum(a) % 3
        if s != 0:
            a[0] += (3 - s) % 3
    else:
        # Large random
        a = [r.randint(-10**9, 10**9) for _ in range(n)]
        s = sum(a) % 3
        if s != 0:
            a[-1] += (3 - s) % 3

    return f"{n}\n{' '.join(map(str, a))}\n"


def valid(text):
    v = list(map(int, text.split()))
    n = v[0]
    if n < 1 or n > 500000:
        return False
    if len(v) != n + 1:
        return False
    return all(-10**9 <= x <= 10**9 for x in v[1:])


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
