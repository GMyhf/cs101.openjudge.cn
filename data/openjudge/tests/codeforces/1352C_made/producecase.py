#!/usr/bin/env python3
"""1352C K-th Not Divisible by n: diverse n,k pairs including edge cases."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "6\n3 7\n4 12\n2 1000000000\n7 97\n1000000000 1000000000\n2 1\n"
SAMPLE_OUT = "10\n15\n1999999999\n113\n1000000001\n1\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(1352_000_003 + seed * 9176 + attempt)
    t = r.randint(1, 20)
    lines = []
    for _ in range(t):
        mode = (seed + _) % 6
        if mode == 0:
            n, k = 2, r.randint(1, 10**9)
        elif mode == 1:
            n = r.randint(2, 10**9)
            k = 1
        elif mode == 2:
            n = r.randint(2, 1000)
            k = r.randint(1, 1000)
        elif mode == 3:
            n = r.randint(2, 10**9)
            k = r.randint(1, 10**9)
        elif mode == 4:
            n = r.randint(2, 10)
            k = r.randint(1, 10**9)
        else:
            n, k = 10**9, 10**9
        lines.append(f"{n} {k}")
    return f"{t}\n" + "\n".join(lines) + "\n"


def valid(text):
    v = list(map(int, text.split()))
    t = v[0]
    if t < 1 or t > 1000:
        return False
    if len(v) != 1 + 2 * t:
        return False
    idx = 1
    for _ in range(t):
        n, k = v[idx], v[idx + 1]
        if n < 2 or n > 10**9 or k < 1 or k > 10**9:
            return False
        idx += 2
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
