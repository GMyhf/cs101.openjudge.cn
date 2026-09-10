#!/usr/bin/env python3
"""270A Fancy Fence: deterministic cases with an independent polygon oracle."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "3\n30\n60\n90\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(270_000_003 + seed * 9176 + attempt)
    count = (1, 2, 17, 179)[(seed - 1) % 4]
    angles = [r.randint(1, 179) for _ in range(count)]
    if seed == 1: angles = [1]
    if seed == 2: angles = [179, 60]
    return f"{count}\n" + "\n".join(map(str, angles)) + "\n"


def valid(text):
    values = list(map(int, text.split()))
    return 1 <= values[0] < 180 and len(values) == values[0] + 1 and all(0 < x < 180 for x in values[1:])


def oracle(text):
    # A regular k-gon has interior angle 180 - 360/k; enumerate k instead
    # of repeating the reference divisibility expression.
    values = list(map(int, text.split()))[1:]
    return "\n".join("YES" if any(180 - 360 / sides == angle for sides in range(3, 361)) else "NO" for angle in values) + "\n"


def build():
    out = Path(__file__).with_name("data"); out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 21):
        attempt = 0; case = generate(seed)
        while case in cases:
            attempt += 1; case = generate(seed, attempt)
        cases.append(case)
    for index, case in enumerate(cases):
        if not valid(case): raise SystemExit(f"invalid case {index}")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True, capture_output=True, check=True).stdout
        if answer != oracle(case): raise SystemExit(f"oracle disagreement {index}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__":
    build()
