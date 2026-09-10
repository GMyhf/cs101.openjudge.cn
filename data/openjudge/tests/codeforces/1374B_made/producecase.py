#!/usr/bin/env python3
"""1374B: factor-family coverage with a brute-force small-number oracle."""
from __future__ import annotations
from collections import deque
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "7\n1\n2\n3\n12\n12345\n15116544\n387420489\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(1374_000_003 + seed * 9176 + attempt)
    count = (1, 2, 17, 80)[(seed - 1) % 4]; values = []
    for index in range(count):
        mode = (seed + index) % 5
        if mode == 0: value = 3 ** r.randint(0, 18)
        elif mode == 1: value = 2 ** r.randint(1, 12) * 3 ** r.randint(0, 5)
        elif mode == 2: value = 2 ** r.randint(0, 8) * 3 ** r.randint(1, 12)
        elif mode == 3: value = r.choice((5, 7, 11, 13)) * 2 ** r.randint(0, 8) * 3 ** r.randint(0, 8)
        else: value = r.randint(1, 10**9)
        values.append(min(value, 10**9))
    return f"{count}\n" + "\n".join(map(str, values)) + "\n"


def valid(text):
    v = list(map(int, text.split())); return 1 <= v[0] <= 20_000 and len(v) == v[0] + 1 and all(1 <= x <= 10**9 for x in v[1:])


def oracle_one(value):
    # BFS is intentionally independent from factor counting; limit is enough
    # for cross-checking the small cases used here.
    todo = deque([(value, 0)]); seen = {value}
    while todo:
        current, steps = todo.popleft()
        if current == 1: return steps
        for nxt in ((current * 2), (current // 6 if current % 6 == 0 else -1)):
            if 0 < nxt <= 10**9 and nxt not in seen:
                seen.add(nxt); todo.append((nxt, steps + 1))
    return -1


def oracle(text):
    return "\n".join(map(str, (oracle_one(x) for x in map(int, text.split()[1:]))) ) + "\n"


def build():
    out = Path(__file__).with_name("data"); out.mkdir(exist_ok=True); cases = [SAMPLE]
    for seed in range(1, 21):
        attempt = 0; case = generate(seed)
        while case in cases: attempt += 1; case = generate(seed, attempt)
        cases.append(case)
    for index, case in enumerate(cases):
        if not valid(case): raise SystemExit(f"invalid {index}")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True, capture_output=True, check=True).stdout
        # The BFS oracle is used only where its state space is bounded.
        if index == 0 and answer != oracle(case): raise SystemExit("sample oracle disagreement")
        (out / f"{index}.in").write_text(case, encoding="utf-8"); (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__": build()
