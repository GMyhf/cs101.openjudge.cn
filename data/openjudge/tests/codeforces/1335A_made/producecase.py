#!/usr/bin/env python3
"""1335A: Candies and Two Sisters test generator."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "6\n7\n1\n2\n3\n2000000000\n763243547\n"
SAMPLE_OUT = "3\n0\n0\n1\n999999999\n381621773\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(1335_000 + seed * 10007 + attempt * 43)
    t = r.randint(1, 10**4)
    lines = [str(t)]
    for _ in range(t):
        mode = (seed + _) % 6
        if mode == 0:
            n = 1  # Edge: answer is 0
        elif mode == 1:
            n = 2  # Edge: answer is 0
        elif mode == 2:
            n = r.randint(3, 10)  # Small
        elif mode == 3:
            n = r.randint(10**8, 2 * 10**9)  # Large
        elif mode == 4:
            n = 2 * 10**9  # Maximum
        else:
            n = r.randint(1, 2 * 10**9)  # General
        lines.append(str(n))
    return "\n".join(lines) + "\n"


def valid(text):
    parts = list(map(int, text.split()))
    t = parts[0]
    if not (1 <= t <= 10**4):
        return False
    if len(parts) != 1 + t:
        return False
    for i in range(1, t + 1):
        if not (1 <= parts[i] <= 2 * 10**9):
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
