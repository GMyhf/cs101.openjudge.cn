#!/usr/bin/env python3
"""1328A: Divisibility Problem test generator."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "5\n10 4\n13 9\n100 13\n123 456\n92 46\n"
SAMPLE_OUT = "2\n5\n4\n333\n0\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(1328_000 + seed * 7919 + attempt * 41)
    t = r.randint(1, 10**4)
    lines = [str(t)]
    for _ in range(t):
        mode = (seed + _) % 5
        if mode == 0:
            # Already divisible
            b = r.randint(1, 10**9)
            a = b * r.randint(1, 10**9 // b if b > 0 else 1)
            a = min(a, 10**9)
        elif mode == 1:
            # a < b
            b = r.randint(2, 10**9)
            a = r.randint(1, b - 1)
        elif mode == 2:
            # a = 1
            a = 1
            b = r.randint(1, 10**9)
        elif mode == 3:
            # Large values
            a = r.randint(1, 10**9)
            b = r.randint(1, 10**9)
        else:
            # b = 1 (always 0)
            a = r.randint(1, 10**9)
            b = 1
        lines.append(f"{a} {b}")
    return "\n".join(lines) + "\n"


def valid(text):
    parts = list(map(int, text.split()))
    t = parts[0]
    if not (1 <= t <= 10**4):
        return False
    if len(parts) != 1 + 2 * t:
        return False
    for i in range(t):
        a = parts[1 + 2 * i]
        b = parts[2 + 2 * i]
        if not (1 <= a <= 10**9 and 1 <= b <= 10**9):
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
