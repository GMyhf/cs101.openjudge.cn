def solve_text(text):
    it = iter(text.split()); out = []
    for _ in range(int(next(it))):
        n, k = int(next(it)), int(next(it))
        pos = [int(next(it)) for _ in range(n)]
        profit = [int(next(it)) for _ in range(n)]
        dp = [0] * n
        for i in range(n):
            dp[i] = profit[i] + max(
                [dp[j] for j in range(i) if pos[i] - pos[j] > k] or [0]
            )
        out.append(str(max(dp)))
    return "\n".join(out) + "\n"


def generate_case(rng):
    cases = [(3, 11, [1, 2, 10], [15, 2, 30]), (4, 2, [1, 4, 7, 10], [5, 8, 4, 10])]
    for _ in range(8):
        n = rng.randint(1, 12); cases.append((n, rng.randint(1, 8), sorted(rng.sample(range(1, 80), n)), [rng.randint(1, 100) for _ in range(n)]))
    lines = [str(len(cases))]
    for n, k, positions, profits in cases:
        lines += [f"{n} {k}", " ".join(map(str, positions)), " ".join(map(str, profits))]
    return "\n".join(lines) + "\n"

import random
from pathlib import Path
SAMPLE_IN = '2\n3 11\n1 2 15\n10 2 30\n3 16\n1 2 15\n10 2 30\n'
SAMPLE_OUT = '40\n30\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(4118)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 04118")
