#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CASES = [
    6, 1, 2, 3, 4, 5, 7, 8, 9, 10,
    15, 16, 17, 24, 25, 26, 35, 36, 37, 48,
    49, 50, 63, 64, 65, 80, 81, 82, 99, 100,
    101, 256, 257, 999, 1024, 1025, 4095, 4096, 4097, 10000,
]


def oracle(n):
    alive = [True] * n
    count = n
    last_released = None
    while count:
        position = 0
        next_alive = alive.copy()
        for original_index, present in enumerate(alive):
            if not present:
                continue
            position += 1
            root = int(position ** 0.5)
            if root * root == position:
                next_alive[original_index] = False
                last_released = original_index + 1
                count -= 1
        alive = next_alive
    return last_released


def main():
    assert len(CASES) == 40 and len(set(CASES)) == 40
    assert all(1 <= n <= 10000 for n in CASES)
    assert oracle(6) == 5
    DATA.mkdir(exist_ok=True)
    for index, n in enumerate(CASES):
        (DATA / f"{index}.in").write_text(f"{n}\n", encoding="ascii")
        (DATA / f"{index}.out").write_text(f"{oracle(n)}\n", encoding="ascii")
    print(f"generated {len(CASES)} cases in {DATA}")


if __name__ == "__main__":
    main()
