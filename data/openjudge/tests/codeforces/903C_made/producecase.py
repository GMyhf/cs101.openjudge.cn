#!/usr/bin/env python3
"""903C Boxes Packing: deterministic single-problem data."""
from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

PROBLEM = "903C"
SAMPLE = "3\n1 2 3\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed: int, attempt: int = 0) -> str:
    r = random.Random(903_000_003 + seed * 9_176 + attempt)
    shapes = ("one", "all_same", "uniform", "dominant", "large_values")
    shape = shapes[(seed - 1) % len(shapes)]
    if shape == "one":
        values = [r.randint(1, 1000)]
    elif shape == "all_same":
        values = [r.randint(1, 1000)] * r.randint(2, 1000)
    elif shape == "uniform":
        values = list(range(1, r.randint(2, 1001)))
        r.shuffle(values)
    elif shape == "dominant":
        n = r.randint(100, 1000); repeated = r.randint(1, 1000)
        values = [repeated] * r.randint(n // 2, n) + [r.randint(1, 1000) for _ in range(n)]
        values = values[:1000]; r.shuffle(values)
    else:
        values = [r.randint(900, 1000) for _ in range(r.randint(2, 1000))]
    return f"{len(values)}\n{' '.join(map(str, values))}\n"


def valid(text: str) -> bool:
    tokens = text.split()
    try:
        n, values = int(tokens[0]), list(map(int, tokens[1:]))
    except (ValueError, IndexError):
        return False
    return 1 <= n <= 1000 and len(values) == n and all(1 <= value <= 1000 for value in values)


def oracle(text: str) -> str:
    # Sort/run-length counting is deliberately unlike samplecode's hash map.
    values = sorted(map(int, text.split()[1:]))
    best = run = 0
    previous = None
    for value in values:
        run = run + 1 if value == previous else 1
        best = max(best, run); previous = value
    return f"{best}\n"


def build():
    out = Path(__file__).with_name("data"); out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 21):
        attempt = 0; case = generate(seed)
        while case in cases:
            attempt += 1; case = generate(seed, attempt)
        cases.append(case)
    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"invalid case {index}")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, check=True, timeout=30).stdout
        if answer != oracle(case):
            raise SystemExit(f"oracle disagreement at case {index}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__":
    build()
