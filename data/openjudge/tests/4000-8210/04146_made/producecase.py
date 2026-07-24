def solve_text(text):
    n = int(text.split()[0]); ans = 0
    for a in range(n + 1):
        for b in range(n + 1):
            for c in range(n + 1):
                if (a + b) % 2 == 0 and (b + c) % 3 == 0 and (a + b + c) % 5 == 0:
                    ans = max(ans, a + b + c)
    return str(ans) + "\n"


def generate_case(rng): return f"{rng.choice([0, 1, 2, 3, 5, 10, 25, 50, 100])}\n"

import random
from pathlib import Path
SAMPLE_IN = '3\n'
SAMPLE_OUT = '5\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(4146)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 04146")
