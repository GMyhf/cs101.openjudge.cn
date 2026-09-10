#!/usr/bin/env python3
"""1829D Gold Rush: deterministic split-tree reachability cases."""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "11\n6 4\n9 4\n4 2\n18 27\n27 4\n27 2\n27 10\n1 1\n3 1\n5 1\n746001 2984004\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def descendants(n):
    seen, todo = {n}, [n]
    while todo:
        value = todo.pop()
        if value % 3 == 0:
            for nxt in (value // 3, value * 2 // 3):
                if nxt not in seen: seen.add(nxt); todo.append(nxt)
    return seen


def generate(seed, attempt=0):
    r = random.Random(1829_000_003 + seed * 9176 + attempt); count = (1, 2, 17, 100)[(seed - 1) % 4]; rows = []
    for index in range(count):
        base = 3 ** r.randint(0, 12) * r.choice((1, 2, 4, 5, 7))
        possible = descendants(base)
        if (seed + index) % 2: target = r.choice(tuple(possible))
        else:
            target = r.randint(1, 10**7)
            while target in possible: target = r.randint(1, 10**7)
        rows.append((base, target))
    return str(count) + "\n" + "".join(f"{n} {m}\n" for n, m in rows)


def valid(text):
    v = list(map(int, text.split())); return 1 <= v[0] <= 1000 and len(v) == 1 + 2*v[0] and all(1 <= x <= 10**7 for x in v[1:])


def oracle(text):
    v = list(map(int, text.split())); return "\n".join("YES" if target in descendants(n) else "NO" for n, target in zip(v[1::2], v[2::2])) + "\n"


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
