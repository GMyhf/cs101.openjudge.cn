#!/usr/bin/env python3
"""1970E1 Trails: deterministic DP inputs and matrix oracle."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path
MOD = 1_000_000_007
SAMPLE = "3 2\n1 0 1\n0 1 1\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(1970_000_003 + seed * 9176 + attempt)
    m, days = ((1, 1), (2, 30), (10, 100), (40, 250))[(seed - 1) % 4]
    short = [r.randint(0, 1000) for _ in range(m)]; long = [r.randint(0, 1000) for _ in range(m)]
    if seed == 1: short, long = [0], [1000]
    return f"{m} {days}\n{' '.join(map(str, short))}\n{' '.join(map(str, long))}\n"


def valid(text):
    rows = text.splitlines();
    try: m, days = map(int, rows[0].split()); short = list(map(int, rows[1].split())); long = list(map(int, rows[2].split()))
    except (ValueError, IndexError): return False
    return len(rows) == 3 and 1 <= m <= 100 and 1 <= days <= 1000 and len(short) == len(long) == m and all(0 <= x <= 1000 for x in short + long)


def oracle(text):
    rows = text.splitlines(); m, days = map(int, rows[0].split()); short = list(map(int, rows[1].split())); long = list(map(int, rows[2].split()))
    matrix = [[(long[i]*short[j] + short[i]*long[j] + short[i]*short[j]) % MOD for j in range(m)] for i in range(m)]
    vector = [1] + [0] * (m-1)
    for _ in range(days): vector = [sum(vector[i] * matrix[i][j] for i in range(m)) % MOD for j in range(m)]
    return f"{sum(vector) % MOD}\n"


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
