#!/usr/bin/env python3
"""Generate deterministic tests for practice/31185."""
import random
import string
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAMPLE_INPUT = "1 1\n6\n4 1 7 -2 4 10\n"
SAMPLE_OUTPUT = "-2 1 4 4 7 10\n10 -2\n"


def generate(number, seed):
    if number == 0:
        return SAMPLE_INPUT
    rng = random.Random(3118500 + seed)
    mode = (number - 1) % 6 + 1
    rule = 1 if (number // 6) % 2 == 0 else 2
    n = 100 if number >= 18 else 7
    if mode in (1, 5):
        values = [-1_000_000, 1_000_000, 0, 7, 7, -3, 2]
        values += [rng.randint(-1_000_000, 1_000_000) for _ in range(n - len(values))]
        return f"{mode} {rule}\n{n}\n" + " ".join(map(str, values)) + "\n"
    if mode == 2:
        values = ["a", "aa", "z", "same", "same", "abc", "b"]
        values += ["".join(rng.choice(string.ascii_lowercase) for _ in range(rng.randint(1, 20)))
                   for _ in range(n - len(values))]
        return f"2 {rule}\n{n}\n" + " ".join(values) + "\n"
    if mode == 3:
        values = [(2, 3), (1, 4), (0, 9), (-1, 1), (7, -2), (3, 2), (1, -1)]
        values += [(rng.randint(-1_000_000, 1_000_000), rng.randint(-1_000_000, 1_000_000))
                   for _ in range(n - len(values))]
    elif mode == 4:
        values = [(8, 2, 9), (1, 7, 3), (4, 2, 0), (5, -1, 6),
                  (9, 7, -4), (0, 2, 8), (3, -1, 5)]
        values += [tuple(rng.randint(-1_000_000, 1_000_000) for _ in range(3))
                   for _ in range(n - len(values))]
    else:
        values = [(2, 5), (1, 7), (2, 9), (1, 3), (3, 6), (2, 5), (1, 7)]
        values += [(rng.randint(-1_000_000, 1_000_000), rng.randint(-1_000_000, 1_000_000))
                   for _ in range(n - len(values))]
    return f"{mode} {rule}\n{n}\n" + "\n".join(" ".join(map(str, row)) for row in values) + "\n"


def valid(text):
    lines = text.splitlines()
    if len(lines) < 3:
        return False
    mode, rule = map(int, lines[0].split())
    return 1 <= mode <= 6 and rule in (1, 2) and 1 <= int(lines[1]) <= 100


def solve(text):
    run = subprocess.run([sys.executable, str(ROOT / "samplecode.py")], input=text,
                         text=True, capture_output=True, check=True)
    return run.stdout


def main():
    data = ROOT / "data"
    data.mkdir(exist_ok=True)
    for number in range(21):
        case = generate(number, number)
        assert valid(case)
        output = solve(case)
        if number == 0:
            assert output == SAMPLE_OUTPUT
        (data / f"{number}.in").write_text(case, encoding="utf-8")
        (data / f"{number}.out").write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
