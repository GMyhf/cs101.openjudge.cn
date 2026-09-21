#!/usr/bin/env python3
"""158B: Taxi test generator."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "5\n1 2 4 3 3\n"
SAMPLE_OUT = "4\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(158_000 + seed * 7907 + attempt * 67)
    mode = seed % 7
    if mode == 0:
        # All 1s
        n = r.randint(1, 10**5)
        groups = [1] * n
    elif mode == 1:
        # All 4s
        n = r.randint(1, 10**5)
        groups = [4] * n
    elif mode == 2:
        # All 2s
        n = r.randint(1, 10**5)
        groups = [2] * n
    elif mode == 3:
        # All 3s
        n = r.randint(1, 10**5)
        groups = [3] * n
    elif mode == 4:
        # Mixed, small n
        n = r.randint(1, 100)
        groups = [r.randint(1, 4) for _ in range(n)]
    elif mode == 5:
        # Large n, mixed
        n = 10**5
        groups = [r.randint(1, 4) for _ in range(n)]
    else:
        # General
        n = r.randint(1, 10**5)
        groups = [r.randint(1, 4) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, groups))}\n"


def valid(text):
    parts = list(map(int, text.split()))
    n = parts[0]
    if not (1 <= n <= 10**5):
        return False
    if len(parts) != 1 + n:
        return False
    groups = parts[1:]
    return all(1 <= g <= 4 for g in groups)


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
