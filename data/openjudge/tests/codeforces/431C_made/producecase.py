#!/usr/bin/env python3
"""431C k-Tree: count paths with DP, diverse n,k,d values."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "3 3 2\n"
SAMPLE_OUT = "3\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(431_000_003 + seed * 9176 + attempt)
    mode = (seed - 1 + attempt) % 6
    if mode == 0:
        n = r.randint(1, 100)
        k = r.randint(1, n)
        d = r.randint(1, k)
    elif mode == 1:
        n = r.randint(1, 10)
        k = r.randint(1, 10)
        d = r.randint(1, k)
    elif mode == 2:
        # d = k (all edges count as "big")
        n = r.randint(1, 50)
        k = r.randint(1, min(n, 20))
        d = k
    elif mode == 3:
        # d = 1 (every path has an edge >= 1, so answer = total paths)
        n = r.randint(1, 50)
        k = r.randint(1, min(n, 20))
        d = 1
    elif mode == 4:
        # k = 1 (only edge weight 1, so only one path of weight n)
        n = r.randint(1, 100)
        k = 1
        d = 1
    else:
        # Large n, k
        n = r.randint(50, 100)
        k = r.randint(1, 100)
        d = r.randint(1, k)
    return f"{n} {k} {d}\n"


def valid(text):
    v = list(map(int, text.split()))
    if len(v) != 3:
        return False
    n, k, d = v
    return 1 <= n <= 100 and 1 <= k <= 100 and 1 <= d <= k


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
