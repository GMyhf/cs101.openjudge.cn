#!/usr/bin/env python3
"""1154A: Restoring Three Numbers test generator."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "3 6 5 4\n"
SAMPLE_OUT = "2 1 3\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(1154_000 + seed * 9973 + attempt * 37)
    mode = seed % 5
    # Constraint: a+b+c <= 10^9 (since max of the 4 output values is a+b+c)
    # and each xi >= 2 (so each pairwise sum >= 2, meaning a,b,c >= 1)
    if mode == 0:
        # a = b = c
        a = r.randint(1, 10**9 // 3)
        b, c = a, a
    elif mode == 1:
        # Two equal
        a = r.randint(1, 10**9 // 4)
        b = a
        c = r.randint(1, 10**9 - 2 * a)
    elif mode == 2:
        # Large values
        a = r.randint(1, 10**9 // 3)
        b = r.randint(1, (10**9 - a) // 2)
        c = r.randint(1, 10**9 - a - b)
    elif mode == 3:
        # One very small
        a = 1
        b = r.randint(1, (10**9 - 1) // 2)
        c = r.randint(1, 10**9 - a - b)
    else:
        # General
        a = r.randint(1, 10**9 // 3)
        b = r.randint(1, (10**9 - a) // 2)
        c = r.randint(1, 10**9 - a - b)

    # Generate the four numbers: a+b, a+c, b+c, a+b+c in random order
    sums = [a + b, a + c, b + c, a + b + c]
    r.shuffle(sums)
    return " ".join(map(str, sums)) + "\n"


def valid(text):
    parts = list(map(int, text.split()))
    if len(parts) != 4:
        return False
    return all(2 <= x <= 10**9 for x in parts)


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
            raise SystemExit(f"invalid case {index}")
        if index == 0:
            answer = SAMPLE_OUT
        else:
            answer = subprocess.run(
                [sys.executable, str(REFERENCE)],
                input=case, text=True, capture_output=True, check=True
            ).stdout
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__":
    build()
