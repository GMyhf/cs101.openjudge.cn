import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent


def generate(i):
    fixed = [
        (100, 500), (100, 999), (100, 152), (153, 153),
        (154, 369), (370, 370), (371, 407), (408, 999),
        (999, 999), (400, 406), (200, 800),
    ]
    if i < len(fixed):
        a, b = fixed[i]
    else:
        rng = random.Random(3120100 + i)
        a = rng.randint(100, 999)
        b = rng.randint(a, 999)
    return f"{a} {b}\n"


def valid(text):
    """题面契约：一行两个正整数 a b，100 <= a <= b <= 999。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    parts = text[:-1].split(" ")
    if len(parts) != 2 or not all(p.isdigit() and p[0] != "0" for p in parts):
        return False
    a, b = map(int, parts)
    return 100 <= a <= b <= 999


def main():
    for i in range(40):
        case = generate(i)
        result = subprocess.run(
            ["python3", str(ROOT / "samplecode.py")],
            input=case, text=True, capture_output=True, check=True,
        ).stdout
        (ROOT / "data" / f"{i}.in").write_text(case, encoding="utf-8")
        (ROOT / "data" / f"{i}.out").write_text(result, encoding="utf-8")


if __name__ == "__main__":
    main()
