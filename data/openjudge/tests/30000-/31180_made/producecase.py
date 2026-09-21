#!/usr/bin/env python3
"""Generate deterministic tests for practice/31180."""
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAMPLE_INPUT = """5
Birth Height Name Math Gender Chinese English
2005-02-15 170.5 Alice 85 F 90 95
2005-06-20 180.0 Bob 92 M 88 90
2005-08-10 165.2 Cathy 75 F 72 80
2005-11-05 178.4 David 95 M 95 98
2005-01-30 160.5 Eva 65 F 85 70
"""

NAMES = ["Alice", "Bob", "Cathy", "David", "Eva", "Grace", "Helen", "Ivy", "Jack", "Kira", "Liam", "Mona"]
HEADERS = ["Name", "Gender", "Chinese", "Math", "English", "Birth", "Height"]


def generate(number):
    if number == 0:
        return SAMPLE_INPUT
    rng = random.Random(3118000 + number)
    n = 1 if number == 1 else (2 if number == 2 else (100 if number == 20 else 3 + (number * 7) % 18))
    names = [f"Student{chr(65 + (i // 26) % 26)}{chr(65 + i % 26)}" for i in range(n)] if n > len(NAMES) else NAMES[:n]
    rows = []
    for i, name in enumerate(names):
        month = ((i + number * 2) % 12) + 1
        day = (i * 3 + 1) % 27 + 1
        gender = "F" if (i + number) % 2 == 0 else "M"
        if number == 2:
            scores = (80, 80, 80)
        elif number == 3 and i == 0:
            scores = (100, 100, 100)
        else:
            scores = tuple(rng.randint(0, 100) for _ in range(3))
        height = 145.0 + rng.randint(0, 450) / 10
        rows.append([name, gender, scores[0], scores[1], scores[2], f"2005-{month:02d}-{day:02d}", height])
    headers = HEADERS[:]
    rng.shuffle(headers)
    lines = [str(n), " ".join(headers)]
    for row in rows:
        values = dict(zip(HEADERS, row))
        lines.append(" ".join(str(values[h]) if h != "Height" else f"{values[h]:.1f}" for h in headers))
    return "\n".join(lines) + "\n"


def valid(text):
    lines = text.splitlines()
    if len(lines) < 2:
        return False
    n = int(lines[0]); headers = lines[1].split()
    return 1 <= n <= 1000 and sorted(headers) == sorted(HEADERS) and len(lines) == n + 2


def solve(text):
    result = subprocess.run([sys.executable, str(ROOT / "samplecode.py")], input=text, text=True, capture_output=True, check=True)
    return result.stdout


def main():
    data = ROOT / "data"
    data.mkdir(exist_ok=True)
    for number in range(40):
        case = generate(number)
        assert valid(case)
        output = solve(case)
        if number == 0:
            assert output == """David 288
Q1 2 165.5
Q2 1 180.0
Q3 1 165.2
Q4 1 178.4
1
Alice 90 85 95 270
"""
        (data / f"{number}.in").write_text(case, encoding="utf-8")
        (data / f"{number}.out").write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
