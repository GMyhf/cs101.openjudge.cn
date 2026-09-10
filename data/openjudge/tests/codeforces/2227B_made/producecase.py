#!/usr/bin/env python3
"""2227B Party Monster: count-based, not balance-based, data."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "4\n2\n)(\n4\n()()\n4\n))((\n5\n()(()\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(2227_000_003 + seed * 9176 + attempt); count = (1, 2, 20, 200)[(seed - 1) % 4]; rows = []
    for index in range(count):
        n = 1 if seed == 1 and index == 0 else (100 if seed == 2 and index == 0 else r.randint(1, 100))
        opens = n // 2 if (seed + index) % 2 else r.randint(0, n)
        text = "(" * opens + ")" * (n - opens)
        if (seed + index) % 3: text = "".join(reversed(text))
        rows.append(text)
    return str(count) + "\n" + "".join(f"{len(text)}\n{text}\n" for text in rows)


def valid(text):
    lines = text.splitlines(); count = int(lines[0]); return 1 <= count <= 10_000 and len(lines) == 1 + 2*count and all(1 <= int(lines[i]) <= 100 and len(lines[i+1]) == int(lines[i]) and not set(lines[i+1])-set("()") for i in range(1, len(lines), 2))


def oracle(text):
    lines = text.splitlines()[1:]; return "\n".join("YES" if line.count("(") == line.count(")") else "NO" for line in lines[1::2]) + "\n"


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
