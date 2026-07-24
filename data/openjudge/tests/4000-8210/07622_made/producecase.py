def solve_text(text):
    values = list(map(int, text.split())); n, permutation = values[0], values[1:]
    bit = [0] * (n + 2); answer = 0
    for value in reversed(permutation):
        x = value - 1
        while x:
            answer += bit[x]; x -= x & -x
        x = value
        while x <= n:
            bit[x] += 1; x += x & -x
    return str(answer) + "\n"


def generate_case(rng):
    n = rng.randint(1, 100); values = list(range(1, n + 1)); rng.shuffle(values)
    return f"{n}\n" + " ".join(map(str, values)) + "\n"

import random
from pathlib import Path
SAMPLE_IN = '6\n2 6 3 4 5 1\n'
SAMPLE_OUT = '8\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(7622)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 07622")
