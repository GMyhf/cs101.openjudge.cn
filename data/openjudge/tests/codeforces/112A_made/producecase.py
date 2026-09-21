#!/usr/bin/env python3
"""112A: Petya and Strings test generator."""
from __future__ import annotations
import random
import string
import subprocess
import sys
from pathlib import Path

SAMPLE = "aaaa\naaaA\n"
SAMPLE_OUT = "0\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(112_000 + seed * 7901 + attempt * 53)
    mode = seed % 6
    length = r.randint(1, 100)
    if mode == 0:
        # Identical strings (different case)
        base = [r.choice(string.ascii_letters) for _ in range(length)]
        s1 = "".join(base)
        s2 = "".join(c.upper() if r.random() < 0.5 else c.lower() for c in base)
    elif mode == 1:
        # s1 < s2
        s1 = "".join(r.choice(string.ascii_letters) for _ in range(length))
        s2 = "".join(r.choice(string.ascii_letters) for _ in range(length))
        # Ensure s1 < s2 by making first char smaller
        c1 = r.choice('abcdefghijklmnop')
        c2 = r.choice('qrstuvwxyz')
        s1 = c1 + s1[1:]
        s2 = c2 + s2[1:]
    elif mode == 2:
        # s1 > s2
        s1 = "".join(r.choice(string.ascii_letters) for _ in range(length))
        s2 = "".join(r.choice(string.ascii_letters) for _ in range(length))
        c1 = r.choice('qrstuvwxyz')
        c2 = r.choice('abcdefghijklmnop')
        s1 = c1 + s1[1:]
        s2 = c2 + s2[1:]
    elif mode == 3:
        # Length 1
        s1 = r.choice(string.ascii_letters)
        s2 = r.choice(string.ascii_letters)
    elif mode == 4:
        # Length 100
        length = 100
        s1 = "".join(r.choice(string.ascii_letters) for _ in range(length))
        s2 = "".join(r.choice(string.ascii_letters) for _ in range(length))
    else:
        # All same letter different case
        ch = r.choice(string.ascii_lowercase)
        s1 = ch * length
        s2 = ch.upper() * length
    return f"{s1}\n{s2}\n"


def valid(text):
    lines = text.strip().split("\n")
    if len(lines) != 2:
        return False
    s1, s2 = lines
    if not (1 <= len(s1) <= 100 and 1 <= len(s2) <= 100):
        return False
    if len(s1) != len(s2):
        return False
    return all(c in string.ascii_letters for c in s1 + s2)


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
            raise SystemExit(f"invalid case {index}")
        if index == 0:
            answer = SAMPLE_OUT
        else:
            answer = subprocess.run(
                [sys.executable, str(REFERENCE)],
                input=case, text=True, capture_output=True, check=True
            ).stdout
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__":
    build()
