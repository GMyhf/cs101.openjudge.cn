#!/usr/bin/env python3
"""Generate deterministic tests for practice/31183."""
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAMPLE_INPUT = "6\n10\n-3\n8\nEND\n"
SAMPLE_OUTPUT = "15\n"


def generate(number, seed):
    if number == 0:
        return SAMPLE_INPUT
    rng = random.Random(3118300 + seed)
    mode = (number - 1) % 8 + 1
    if mode == 1:
        values = ["oneword", "leading  and  trailing", "a  b   c"]
        return f"1\n{values[(number // 8) % len(values)]}\n"
    if mode == 2:
        x = [-1_000_000, 0, rng.randint(-999_999, 999_999)][number % 3]
        return f"2\n{x}\n"
    if mode == 3:
        words = ["alpha", "beta", "gamma"] if number < 10 else ["z", "same", "same"]
        return "3\n" + " ".join(words) + "\n"
    if mode == 4:
        a, b = ((1_000_000, -1_000_000) if number < 12 else
                (rng.randint(-1_000_000, 1_000_000), rng.randint(-1_000_000, 1_000_000)))
        return f"4\n{a} {b}\n"
    if mode == 5:
        n = 100 if number > 12 else 1
        values = [-1_000_000] if n == 1 else [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]
        return "5\n" + " ".join(map(str, values)) + "\n"
    if mode == 6:
        values = [] if number < 12 else [1_000_000, -1_000_000, 7, -8]
        return "6\n" + "\n".join(map(str, values)) + ("\n" if values else "") + "END\n"
    if mode == 7:
        n = 100 if number > 14 else 1
        pairs = [(rng.randint(-1_000_000, 1_000_000), rng.randint(-1_000_000, 1_000_000)) for _ in range(n)]
        return "7\n" + str(n) + "\n" + "\n".join(f"{a} {b}" for a, b in pairs) + "\n"
    values = ["apple", "banana", "cat"] if number < 16 else ["a", "zz", "middle"]
    return "8\n" + ",".join(values) + "\n"


def valid(text):
    lines = text.splitlines()
    return bool(lines) and lines[0] in set("12345678")


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
