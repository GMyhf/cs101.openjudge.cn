#!/usr/bin/env python3
"""456A Laptops: deterministic monotone and inversion cases."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "2\n1 2\n2 1\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


# 题面：1<=a_i,b_i<=n，且 a_i 两两不同、b_i 两两不同 —— 于是价格与质量各是 1..n 的排列。
# 2026-09-20 之前这里从 1..100000 里取样，n=2 的组里也会出现 a_i=57238，越出题面；
# 规模列表同时避免 n=1 出现两次（n=1 只有唯一一种合法输入，会撞成重复组）。
SIZES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 30, 50, 80, 120, 200, 500, 1000)


def generate(seed, attempt=0):
    r = random.Random(456_000_003 + seed * 9176 + attempt)
    n = SIZES[(seed - 1 + attempt) % len(SIZES)]
    prices = list(range(1, n + 1))
    qualities = list(range(1, n + 1))
    r.shuffle(prices)
    r.shuffle(qualities)
    rows = list(zip(prices, qualities))
    if seed % 3 == 0:
        rows = list(zip(sorted(prices), sorted(qualities)))
    elif n > 1:
        rows = list(zip(sorted(prices), sorted(qualities, reverse=True)))
    r.shuffle(rows)
    return str(n) + "\n" + "".join(f"{a} {b}\n" for a, b in rows)


def valid(text):
    v = list(map(int, text.split())); n = v[0]
    return (1 <= n <= 100_000 and len(v) == 1 + 2*n and len(set(v[1::2])) == n
            and len(set(v[2::2])) == n and all(1 <= x <= n for x in v[1:]))


def oracle(text):
    v = list(map(int, text.split())); rows = list(zip(v[1::2], v[2::2]))
    return ("Happy Alex" if any(a < c and b > d for a, b in rows for c, d in rows) else "Poor Alex") + "\n"


def build():
    out = Path(__file__).with_name("data"); out.mkdir(exist_ok=True); cases = [SAMPLE]
    for seed in range(1, 40):
        attempt = 0; case = generate(seed)
        while case in cases: attempt += 1; case = generate(seed, attempt)
        cases.append(case)
    for index, case in enumerate(cases):
        if not valid(case): raise SystemExit(f"invalid {index}")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True, capture_output=True, check=True).stdout
        if answer != oracle(case): raise SystemExit(f"oracle disagreement {index}")
        (out / f"{index}.in").write_text(case, encoding="utf-8"); (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__": build()
