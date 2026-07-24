def solve_text(text):
    n = int(text.split()[0]); catalan = [0] * (n + 1); catalan[0] = 1
    for size in range(1, n + 1):
        catalan[size] = sum(catalan[left] * catalan[size - 1 - left] for left in range(size))
    return str(catalan[n]) + "\n"


def generate_case(rng): return f"{rng.randint(1, 1000)}\n"

import random
from pathlib import Path
SAMPLE_IN = '3\n'
SAMPLE_OUT = '5\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(27217)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 27217")
