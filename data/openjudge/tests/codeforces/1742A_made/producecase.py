#!/usr/bin/env python3
"""1742A Sum: all equality positions and negative cases."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "7\n1 4 3\n2 5 7\n1 2 3\n4 0 4\n0 0 0\n100 1 2\n7 3 4\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(1742_000_003 + seed * 9176 + attempt); count = (1, 2, 11, 100)[(seed - 1) % 4]; rows = []
    for index in range(count):
        a, b = r.randint(0, 50), r.randint(0, 50)
        if (seed + index) % 2:
            row = [a, b, a + b]; r.shuffle(row)
        else:
            row = [a, b, r.randint(0, 100)]
            while any(row[i] + row[j] == row[3-i-j] for i in range(3) for j in range(i + 1, 3)):
                row[2] = r.randint(0, 100)
        rows.append(row)
    return str(count) + "\n" + "".join(" ".join(map(str, row)) + "\n" for row in rows)


def valid(text):
    v = list(map(int, text.split())); return 1 <= v[0] <= 1000 and len(v) == 1 + 3*v[0] and all(0 <= x <= 100 for x in v[1:])


def oracle(text):
    v = list(map(int, text.split())); return "\n".join("YES" if max(row) == sum(row) - max(row) else "NO" for row in (v[i:i+3] for i in range(1, len(v), 3))) + "\n"


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
