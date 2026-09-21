#!/usr/bin/env python3
"""313B Ilya and Queries: prefix sums on adjacent equal chars, diverse strings."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "#..###\n5\n1 3\n5 6\n1 5\n3 6\n3 4\n"
SAMPLE_OUT = "1\n1\n2\n2\n0\n"
REFERENCE = Path(__file__).with_name("samplecode.py")

SIZES = (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 30, 50, 80, 100, 200, 500, 1000, 5000, 10000, 100000)


def generate(seed, attempt=0):
    r = random.Random(313_000_003 + seed * 9176 + attempt)
    n = SIZES[(seed - 1 + attempt) % len(SIZES)]
    mode = (seed - 1 + attempt) % 6
    m = min(r.randint(1, 20), n * (n - 1) // 2)
    m = max(m, 1)

    if mode == 0:
        # Random binary string
        s = ''.join(r.choice('.#') for _ in range(n))
    elif mode == 1:
        # All same char
        c = r.choice('.#')
        s = c * n
    elif mode == 2:
        # Alternating
        c1, c2 = r.choice(['.#', '#.'])
        s = ''.join(c1 if i % 2 == 0 else c2 for i in range(n))
    elif mode == 3:
        # Blocks of same char
        s = ''
        while len(s) < n:
            length = r.randint(1, min(10, n - len(s)))
            s += r.choice('.#') * length
        s = s[:n]
    elif mode == 4:
        # Two characters only
        chars = r.sample(['.', '#', 'a', 'b', 'x', 'y'], 2)
        s = ''.join(r.choice(chars) for _ in range(n))
    else:
        # Random from larger alphabet
        chars = '.#abcxy'
        s = ''.join(r.choice(chars) for _ in range(n))

    # Generate queries
    queries = []
    for _ in range(m):
        l = r.randint(1, n - 1)
        r_val = r.randint(l + 1, n)
        queries.append(f"{l} {r_val}")

    return f"{s}\n{m}\n" + "\n".join(queries) + "\n"


def valid(text):
    lines = text.strip().split('\n')
    s = lines[0]
    n = len(s)
    if n < 2 or n > 100000:
        return False
    m = int(lines[1])
    if m < 1 or m > 100000:
        return False
    if len(lines) != 2 + m:
        return False
    for i in range(m):
        parts = lines[2 + i].split()
        l, r = int(parts[0]), int(parts[1])
        if l < 1 or r > n or l >= r:
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
