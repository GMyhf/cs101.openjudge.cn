#!/usr/bin/env python3
"""545C Woodcutters: greedy tree-falling, diverse positions and heights."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "5\n1 2\n2 1\n5 10\n10 9\n19 1\n"
SAMPLE_OUT = "3\n"
REFERENCE = Path(__file__).with_name("samplecode.py")

SIZES = (1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 30, 50, 80, 100, 200, 500, 1000, 5000, 100000)


def generate(seed, attempt=0):
    r = random.Random(545_000_003 + seed * 9176 + attempt)
    n = SIZES[(seed - 1 + attempt) % len(SIZES)]
    mode = (seed - 1 + attempt) % 5

    if mode == 0:
        # Random positions and heights
        # Generate n unique sorted positions in [1, 10^9]
        positions = sorted(r.sample(range(1, 10**9 + 1), n))
        heights = [r.randint(1, 10**9) for _ in range(n)]
    elif mode == 1:
        # Trees very close together (dense)
        positions = list(range(1, n + 1))
        heights = [r.randint(1, 100) for _ in range(n)]
    elif mode == 2:
        # Trees very far apart (all can fall) - positions within [1, 10^9]
        gap = max(1, (10**9 - 1) // max(n, 1))
        positions = [1 + i * gap for i in range(n)]
        # Ensure strictly increasing and within bounds
        for i in range(1, n):
            if positions[i] <= positions[i-1]:
                positions[i] = positions[i-1] + 1
            if positions[i] > 10**9:
                positions[i] = 10**9
        heights = [r.randint(1, min(gap - 1, 100)) for _ in range(n)] if gap > 1 else [1] * n
    elif mode == 3:
        # n=1 edge case
        n = 1
        positions = [r.randint(1, 10**9)]
        heights = [r.randint(1, 10**9)]
    else:
        # Heights much larger than gaps
        positions = list(range(1, n + 1))
        heights = [r.randint(1, 10**9) for _ in range(n)]

    lines = [f"{n}"]
    for i in range(n):
        lines.append(f"{positions[i]} {heights[i]}")
    return "\n".join(lines) + "\n"


def valid(text):
    v = list(map(int, text.split()))
    n = v[0]
    if n < 1 or n > 100000:
        return False
    if len(v) != 1 + 2 * n:
        return False
    positions = v[1::2]
    heights = v[2::2]
    if any(x < 1 or x > 10**9 for x in positions):
        return False
    if any(x < 1 or x > 10**9 for x in heights):
        return False
    # Check strictly increasing positions
    for i in range(1, n):
        if positions[i] <= positions[i-1]:
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
