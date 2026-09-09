#!/usr/bin/env python3
"""Generate deterministic tests for practice/31184."""
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAMPLE_INPUT = "1\n-123\n"
SAMPLE_OUTPUT = "123\n"


def generate(number, seed):
    if number == 0:
        return SAMPLE_INPUT
    rng = random.Random(3118400 + seed)
    mode = (number - 1) % 9 + 1
    if mode == 1:
        return f"1\n{[-1_000_000, 0, 1_000_000][number % 3]}\n"
    if mode in (2, 3):
        values = [rng.randint(-1_000_000, 1_000_000) for _ in range(3)]
        return f"{mode}\n" + " ".join(map(str, values)) + "\n"
    if mode == 4:
        return "4\nalpha beta gamma\n" if number < 12 else "4\na a z\n"
    if mode == 5:
        if number == 14:
            return "5\n4\n10 20 30 40\n"
        n = 100
        values = [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]
        return f"5\n{n}\n" + " ".join(map(str, values)) + "\n"
    if mode in (6, 9):
        n = 100 if number > 14 else 1
        values = [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]
        return f"{mode}\n{n}\n" + " ".join(map(str, values)) + "\n"
    if mode == 7:
        a, b = ((-1_000_000, 1_000_000) if number < 14 else (0, -17))
        return f"7\n{a} {b}\n"
    a, b = [(1, 8), (7, 2), (-1, 8)][number % 3]
    return f"8\n{a} {b}\n"


def valid(text):
    lines = text.splitlines()
    return bool(lines) and lines[0] in set("123456789")


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
