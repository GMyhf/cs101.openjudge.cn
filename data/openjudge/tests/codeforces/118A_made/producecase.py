#!/usr/bin/env python3
"""118A: String Task test generator."""
from __future__ import annotations
import random
import string
import subprocess
import sys
from pathlib import Path

SAMPLE = "tour\n"
SAMPLE_OUT = ".t.r\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(118_000 + seed * 7907 + attempt * 59)
    mode = seed % 6
    if mode == 0:
        # All vowels
        length = r.randint(1, 100)
        s = "".join(r.choice("AOYEUIaoyeui") for _ in range(length))
    elif mode == 1:
        # All consonants
        consonants = "".join(c for c in string.ascii_letters if c not in "AOYEUIaoyeui")
        length = r.randint(1, 100)
        s = "".join(r.choice(consonants) for _ in range(length))
    elif mode == 2:
        # Length 1
        s = r.choice(string.ascii_letters)
    elif mode == 3:
        # Length 100
        length = 100
        s = "".join(r.choice(string.ascii_letters) for _ in range(length))
    elif mode == 4:
        # Alternating vowels and consonants
        vowels = "aoeui"
        consonants = "bcdfghjklmnpqrstvwxyz"
        length = r.randint(1, 100)
        s = ""
        for i in range(length):
            if i % 2 == 0:
                s += r.choice(vowels + vowels.upper())
            else:
                s += r.choice(consonants + consonants.upper())
    else:
        # General random
        length = r.randint(1, 100)
        s = "".join(r.choice(string.ascii_letters) for _ in range(length))
    return s + "\n"


def valid(text):
    s = text.strip()
    if not (1 <= len(s) <= 100):
        return False
    return all(c in string.ascii_letters for c in s)


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
