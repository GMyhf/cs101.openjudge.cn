#!/usr/bin/env python3
"""433B: Kuriyama Mirai's Stones test generator."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "6\n6 4 2 7 2 7\n3\n2 3 6\n1 3 4\n1 1 6\n"
SAMPLE_OUT = "24\n9\n28\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(433_000 + seed * 7919 + attempt * 71)
    mode = seed % 6
    if mode == 0:
        # Small n, small m
        n = r.randint(1, 100)
        m = r.randint(1, 100)
    elif mode == 1:
        # Large n, large m
        n = 10**5
        m = 10**5
    elif mode == 2:
        # n = 1
        n = 1
        m = r.randint(1, 100)
    elif mode == 3:
        # All same values
        n = r.randint(1, 10**5)
        m = r.randint(1, 10**5)
    elif mode == 4:
        # Large values
        n = r.randint(1, 10**5)
        m = r.randint(1, 10**5)
    else:
        # General
        n = r.randint(1, 10**5)
        m = r.randint(1, 10**5)

    if mode == 3:
        val = r.randint(1, 10**9)
        v = [val] * n
    elif mode == 4:
        v = [r.randint(10**8, 10**9) for _ in range(n)]
    else:
        v = [r.randint(1, 10**9) for _ in range(n)]

    lines = [str(n), " ".join(map(str, v)), str(m)]
    for _ in range(m):
        typ = r.randint(1, 2)
        l = r.randint(1, n)
        rr = r.randint(l, n)
        lines.append(f"{typ} {l} {rr}")
    return "\n".join(lines) + "\n"


def valid(text):
    parts = list(map(int, text.split()))
    idx = 0
    n = parts[idx]; idx += 1
    if not (1 <= n <= 10**5):
        return False
    if len(parts) < 1 + n:
        return False
    v = parts[idx:idx + n]; idx += n
    if not all(1 <= x <= 10**9 for x in v):
        return False
    m = parts[idx]; idx += 1
    if not (1 <= m <= 10**5):
        return False
    if len(parts) != idx + 3 * m:
        return False
    for i in range(m):
        typ = parts[idx]; l = parts[idx + 1]; rr = parts[idx + 2]; idx += 3
        if not (1 <= typ <= 2 and 1 <= l <= rr <= n):
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
