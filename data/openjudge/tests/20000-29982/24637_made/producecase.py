def solve_text(text):
    values = list(map(int, text.split())); n, treasure = values[0], values[1:]
    dp = [[0, 0] for _ in range(n)]
    for node in range(n - 1, -1, -1):
        left, right = 2 * node + 1, 2 * node + 2
        skip = (max(dp[left]) if left < n else 0) + (max(dp[right]) if right < n else 0)
        take = treasure[node] + (dp[left][0] if left < n else 0) + (dp[right][0] if right < n else 0)
        dp[node] = [skip, take]
    return str(max(dp[0])) + "\n"


def generate_case(rng):
    n = rng.randint(1, 100); values = [rng.randint(0, 1000) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, values)) + "\n"

import random
from pathlib import Path
SAMPLE_IN = '6\n3 4 5 1 3 1\n'
SAMPLE_OUT = '9\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(24637)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 24637")
