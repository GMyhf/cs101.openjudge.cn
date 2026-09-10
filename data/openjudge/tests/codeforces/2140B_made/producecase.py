#!/usr/bin/env python3
"""2140B: validate the t-case protocol as well as each concatenation witness."""
from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "1\n6\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed: int, attempt: int = 0) -> str:
    r = random.Random(2140_000_003 + seed * 9_176 + attempt)
    # The implementation searches witnesses; keep x within the proof-backed
    # construction range while exercising t=1 and many-case parsing.
    count = (1, 2, 3, 10, 20)[(seed - 1) % 5]
    xs = [r.randint(1, 100) for _ in range(count)]
    return f"{count}\n" + "\n".join(map(str, xs)) + "\n"


def valid(text: str) -> bool:
    tokens = text.split()
    try:
        count, xs = int(tokens[0]), list(map(int, tokens[1:]))
    except (ValueError, IndexError):
        return False
    return 1 <= count <= 100 and len(xs) == count and all(1 <= x <= 100 for x in xs)


def oracle(text: str) -> str:
    xs = list(map(int, text.split()[1:])); answers = []
    for x in xs:
        # Independent linear scan: it validates the relation directly instead
        # of relying on the special checker or the reference program.
        for y in range(1, 100_000):
            if int(str(x) + str(y)) % (x + y) == 0:
                answers.append(str(y)); break
        else:
            raise RuntimeError("missing witness")
    return "\n".join(answers) + "\n"


def build():
    out = Path(__file__).with_name("data"); out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 21):
        attempt = 0; case = generate(seed)
        while case in cases:
            attempt += 1; case = generate(seed, attempt)
        cases.append(case)
    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"invalid case {index}")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, check=True, timeout=30).stdout
        if answer != oracle(case):
            raise SystemExit(f"oracle disagreement at case {index}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__":
    build()
