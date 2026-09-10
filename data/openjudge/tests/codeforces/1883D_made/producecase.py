#!/usr/bin/env python3
"""1883D In Love: valid add/remove streams with duplicate segments."""
from __future__ import annotations
from collections import Counter
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "12\n+ 1 2\n+ 3 4\n+ 2 3\n+ 2 2\n+ 3 4\n- 3 4\n- 3 4\n- 1 2\n+ 3 4\n- 2 2\n- 2 3\n- 3 4\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(1883_000_003 + seed * 9176 + attempt); q = (1, 2, 50, 500)[(seed - 1) % 4]; active = Counter(); rows = []
    for index in range(q):
        if active and r.randrange(3) == 0:
            pair = r.choice(list(active.elements())); active[pair] -= 1
            if not active[pair]: del active[pair]
            rows.append(("-", *pair))
        else:
            if seed == 1 and index == 0: pair = (1, 10**9)
            elif index % 7 == 0: pair = (r.randint(1, 100), 10**9)
            elif index % 7 == 1: pair = (10**9 - 1, 10**9)
            else:
                left = r.randint(1, 10**9); pair = (left, r.randint(left, 10**9))
            active[pair] += 1; rows.append(("+", *pair))
    return str(q) + "\n" + "".join(f"{op} {left} {right}\n" for op, left, right in rows)


def valid(text):
    lines = text.splitlines();
    try: q = int(lines[0])
    except (ValueError, IndexError): return False
    active = Counter()
    if not 1 <= q <= 100_000 or len(lines) != q + 1: return False
    for line in lines[1:]:
        op, left, right = line.split(); left = int(left); right = int(right); pair = (left, right)
        if op == "+": active[pair] += 1
        elif op == "-" and active[pair]:
            active[pair] -= 1
            if not active[pair]: del active[pair]
        else: return False
        if not (1 <= left <= right <= 10**9): return False
    return True


def oracle(text):
    lines = text.splitlines()[1:]; active = Counter(); answer = []
    for line in lines:
        op, left, right = line.split(); pair = (int(left), int(right))
        if op == "+": active[pair] += 1
        else:
            active[pair] -= 1
            if not active[pair]: del active[pair]
        answer.append("YES" if active and min(x[1] for x in active) < max(x[0] for x in active) else "NO")
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
