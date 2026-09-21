#!/usr/bin/env python3
"""1352A: Sum of Round Numbers test generator."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "5\n5009\n7\n9876\n10000\n10\n"
SAMPLE_OUT = "2\n5000 9\n1\n7 \n4\n800 70 6 9000 \n1\n10000 \n1\n10\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(1352_000 + seed * 10009 + attempt * 47)
    t = r.randint(1, 10**4)
    lines = [str(t)]
    for _ in range(t):
        mode = (seed + _) % 6
        if mode == 0:
            n = r.randint(1, 9)  # Single digit
        elif mode == 1:
            n = r.choice([10, 100, 1000, 10000])  # Round numbers
        elif mode == 2:
            n = r.randint(10, 99)  # Two digits
        elif mode == 3:
            n = r.randint(100, 999)  # Three digits
        elif mode == 4:
            n = r.randint(1000, 9999)  # Four digits
        else:
            n = r.randint(1, 10000)  # General
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
        if not (1 <= parts[i] <= 10000):
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
