#!/usr/bin/env python3
"""1475A Odd Divisor: powers of two and 64-bit boundary cases."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "6\n2\n3\n4\n5\n998244353\n1099511627776\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(1475_000_003 + seed * 9176 + attempt); count = (1, 2, 10, 100)[(seed - 1) % 4]; values = []
    for index in range(count):
        mode = (seed + index) % 4
        if mode == 0: value = 1 << r.randint(1, 46)
        elif mode == 1: value = (1 << r.randint(1, 40)) * r.choice((3, 5, 7, 9, 15))
        elif mode == 2: value = r.randrange(3, 10**14, 2)
        else: value = r.randint(2, 10**14)
        values.append(value)
    return f"{count}\n" + "\n".join(map(str, values)) + "\n"


def valid(text):
    v = list(map(int, text.split())); return 1 <= v[0] <= 10_000 and len(v) == v[0] + 1 and all(2 <= x <= 10**14 for x in v[1:])


def oracle(text):
    # Repeated division expresses the statement directly, independent of bit trick.
    answer = []
    for value in map(int, text.split()[1:]):
        while value % 2 == 0: value //= 2
        answer.append("YES" if value > 1 else "NO")
    return "\n".join(answer) + "\n"


def build():
    out = Path(__file__).with_name("data"); out.mkdir(exist_ok=True); cases = [SAMPLE]
    for seed in range(1, 21):
        attempt = 0; case = generate(seed)
        while case in cases: attempt += 1; case = generate(seed, attempt)
        cases.append(case)
    for index, case in enumerate(cases):
        if not valid(case): raise SystemExit(f"invalid {index}")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True, capture_output=True, check=True).stdout
        if answer != oracle(case): raise SystemExit(f"oracle disagreement {index}")
        (out / f"{index}.in").write_text(case, encoding="utf-8"); (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__": build()
