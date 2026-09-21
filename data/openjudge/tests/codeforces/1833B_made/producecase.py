#!/usr/bin/env python3
"""1833B Restore the Weather: match temperatures by rank with diverse cases."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "3\n5 2\n1 3 5 3 9\n2 5 11 2 4\n6 1\n-1 3 -2 0 -5 -1\n-4 0 -1 4 0 0\n3 3\n7 7 7\n9 4 8\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(1833_000_003 + seed * 9176 + attempt)
    mode = (seed - 1 + attempt) % 5
    if mode == 0:
        t = 1
        n = SIZES[(seed - 1) % len(SIZES)]
    elif mode == 1:
        t = r.randint(1, 100)
        n = r.randint(1, min(1000, 10**5 // t))
    else:
        t = 1
        n = SIZES[(seed - 1) % len(SIZES)]

    cases_input = f"{t}\n"
    for _ in range(t):
        k = r.randint(0, 10**9)
        # Generate a such that a valid b exists within k
        if mode == 2:
            # All same a values
            base = r.randint(-10**9, 10**9)
            a = [base] * n
            b = [base + r.randint(-k, k) for _ in range(n)]
        elif mode == 3:
            # Already sorted
            a = sorted([r.randint(-10**9, 10**9) for _ in range(n)])
            b = sorted([x + r.randint(-min(k, 100), min(k, 100)) for x in a])
            r.shuffle(b)
        else:
            a = [r.randint(-10**9, 10**9) for _ in range(n)]
            # b is a permutation of values close to a
            b = [x + r.randint(-min(k, 10**6), min(k, 10**6)) for x in a]
            r.shuffle(b)
        cases_input += f"{n} {k}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"
    return cases_input


SIZES = (1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 30, 50, 80, 100, 200, 500, 1000, 5000, 100000)


def valid(text):
    v = list(map(int, text.split()))
    idx = 0
    t = v[idx]; idx += 1
    if t < 1 or t > 10000:
        return False
    total_n = 0
    for _ in range(t):
        n = v[idx]; k = v[idx+1]; idx += 2
        if n < 1 or n > 100000 or k < 0 or k > 10**9:
            return False
        total_n += n
        idx += 2 * n
    return idx == len(v) and total_n <= 100000


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
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__":
    build()
