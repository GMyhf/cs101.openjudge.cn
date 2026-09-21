#!/usr/bin/env python3
"""158A: Next Round test generator."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "8 5\n10 9 8 7 7 7 5 5\n"
SAMPLE_OUT = "6\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(158_000 + seed * 7901 + attempt * 61)
    mode = seed % 6
    if mode == 0:
        # All zeros
        n = r.randint(1, 50)
        k = r.randint(1, n)
        scores = [0] * n
    elif mode == 1:
        # All same positive score
        n = r.randint(1, 50)
        k = r.randint(1, n)
        val = r.randint(1, 100)
        scores = [val] * n
    elif mode == 2:
        # k = n
        n = r.randint(1, 50)
        k = n
        scores = sorted([r.randint(0, 100) for _ in range(n)], reverse=True)
    elif mode == 3:
        # k = 1
        n = r.randint(1, 50)
        k = 1
        scores = sorted([r.randint(0, 100) for _ in range(n)], reverse=True)
    elif mode == 4:
        # n = 50, max
        n = 50
        k = r.randint(1, n)
        scores = sorted([r.randint(0, 100) for _ in range(n)], reverse=True)
    else:
        # General
        n = r.randint(1, 50)
        k = r.randint(1, n)
        scores = sorted([r.randint(0, 100) for _ in range(n)], reverse=True)
    return f"{n} {k}\n{' '.join(map(str, scores))}\n"


def valid(text):
    parts = list(map(int, text.split()))
    n = parts[0]
    k = parts[1]
    if not (1 <= k <= n <= 50):
        return False
    if len(parts) != 2 + n:
        return False
    scores = parts[2:]
    if not all(0 <= s <= 100 for s in scores):
        return False
    # Check non-increasing
    for i in range(n - 1):
        if scores[i] < scores[i + 1]:
            return False
    return True


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
