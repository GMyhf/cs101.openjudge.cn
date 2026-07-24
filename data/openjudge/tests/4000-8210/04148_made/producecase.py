def solve_text(text):
    out = []; case = 1
    for line in text.splitlines():
        p, e, i, d = map(int, line.split())
        if (p, e, i, d) == (-1, -1, -1, -1): break
        day = d + 1
        while (day - p) % 23 or (day - e) % 28 or (day - i) % 33:
            day += 1
        out.append(f"Case {case}: the next triple peak occurs in {day - d} days.")
        case += 1
    return "\n".join(out) + ("\n" if out else "")


def generate_case(rng):
    lines = []
    for _ in range(10):
        d = rng.randint(0, 365); base = rng.randint(0, 21252)
        lines.append(f"{(base + rng.randint(0, 22)) % 23} {(base + rng.randint(0, 27)) % 28} {(base + rng.randint(0, 32)) % 33} {d}")
    return "\n".join(lines) + "\n-1 -1 -1 -1\n"

import random
from pathlib import Path
SAMPLE_IN = '0 0 0 0\n0 0 0 100\n5 20 34 325\n4 5 6 7\n283 102 23 320\n203 301 203 40\n-1 -1 -1 -1\n'
SAMPLE_OUT = 'Case 1: the next triple peak occurs in 21252 days.\nCase 2: the next triple peak occurs in 21152 days.\nCase 3: the next triple peak occurs in 19575 days.\nCase 4: the next triple peak occurs in 16994 days.\nCase 5: the next triple peak occurs in 8910 days.\nCase 6: the next triple peak occurs in 10789 days.\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(4148)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 04148")
