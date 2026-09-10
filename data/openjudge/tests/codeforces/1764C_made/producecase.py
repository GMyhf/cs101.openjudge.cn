#!/usr/bin/env python3
"""1764C Doremy's City Construction: deterministic cut-boundary cases."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "4\n4\n2 2 3 1\n6\n5 2 3 1 5 2\n12\n7 2 4 9 1 4 6 3 7 4 2 3\n4\n1000000 1000000 1000000 1000000\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(1764_000_003 + seed * 9176 + attempt); count = (1, 2, 5, 20)[(seed - 1) % 4]; rows = []
    for index in range(count):
        n = (2, 3, 200, 10_000)[(seed + index) % 4] + attempt % 3
        mode = (seed + index) % 4
        if mode == 0: values = [r.randint(1, 10**6)] * n
        elif mode == 1: values = [1] * (n // 2) + [10**6] * (n - n // 2)
        elif mode == 2: values = [r.randint(1, 5) for _ in range(n)]
        else: values = r.sample(range(1, 10**6 + 1), n)
        r.shuffle(values); rows.append(values)
    return str(count) + "\n" + "".join(f"{len(row)}\n{' '.join(map(str, row))}\n" for row in rows)


def valid(text):
    v = list(map(int, text.split())); cursor = 1; total = 0
    try:
        for _ in range(v[0]):
            n = v[cursor]; row = v[cursor+1:cursor+1+n]; cursor += n+1; total += n
            if not 2 <= n <= 200_000 or len(row) != n or not all(1 <= x <= 10**6 for x in row): return False
    except IndexError: return False
    return 1 <= v[0] <= 10_000 and cursor == len(v) and total <= 200_000


def oracle(text):
    v = list(map(int, text.split())); cursor = 1; answers = []
    for _ in range(v[0]):
        n = v[cursor]; row = sorted(v[cursor+1:cursor+1+n]); cursor += n+1
        # Explicitly enumerate legal group boundaries rather than retaining a
        # running maximum like samplecode.
        choices = [n // 2] + [i * (n-i) for i in range(1, n) if row[i-1] != row[i]]
        answers.append(str(max(choices)))
    return "\n".join(answers) + "\n"


def build():
    out = Path(__file__).with_name("data"); out.mkdir(exist_ok=True); cases = [SAMPLE]
    for seed in range(1, 21):
        attempt = 0; case = generate(seed)
        while case in cases: attempt += 1; case = generate(seed, attempt)
        cases.append(case)
    for index, case in enumerate(cases):
        if not valid(case): raise SystemExit(f"invalid {index}")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True, capture_output=True, check=True, timeout=30).stdout
        if answer != oracle(case): raise SystemExit(f"oracle disagreement {index}")
        (out / f"{index}.in").write_text(case, encoding="utf-8"); (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__": build()
