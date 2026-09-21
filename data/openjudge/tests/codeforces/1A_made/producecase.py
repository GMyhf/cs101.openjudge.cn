#!/usr/bin/env python3
"""1A: Theatre Square test generator."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "6 6 4\n"
SAMPLE_OUT = "4\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(1_000_000 + seed * 7919 + attempt * 31)
    mode = seed % 6
    if mode == 0:
        # Edge: a = 1
        n = r.randint(1, 10**9)
        m = r.randint(1, 10**9)
        a = 1
    elif mode == 1:
        # Edge: n = m = a
        v = r.randint(1, 10**9)
        n, m, a = v, v, v
    elif mode == 2:
        # Large values
        n = r.randint(10**8, 10**9)
        m = r.randint(10**8, 10**9)
        a = r.randint(1, 10**9)
    elif mode == 3:
        # n,m small, a large
        n = r.randint(1, 100)
        m = r.randint(1, 100)
        a = r.randint(10**7, 10**9)
    elif mode == 4:
        # Perfect division
        a = r.randint(1, 10**5)
        n = a * r.randint(1, 10**4)
        m = a * r.randint(1, 10**4)
    else:
        # General random
        n = r.randint(1, 10**9)
        m = r.randint(1, 10**9)
        a = r.randint(1, 10**9)
    return f"{n} {m} {a}\n"


def valid(text):
    parts = list(map(int, text.split()))
    if len(parts) != 3:
        return False
    n, m, a = parts
    return 1 <= n <= 10**9 and 1 <= m <= 10**9 and 1 <= a <= 10**9


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
