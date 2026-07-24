def solve_text(text):
    out = []
    for token in text.split():
        n = int(token); dp = [0] * (n + 1); dp[0] = 1
        for part in range(1, n + 1):
            for total in range(part, n + 1):
                dp[total] += dp[total - part]
        out.append(str(dp[n]))
    return "\n".join(out) + ("\n" if out else "")


def generate_case(rng): return "\n".join(map(str, [1, 2, 3, 4, 5, 10, 20, 50] + [rng.randint(1, 50) for _ in range(12)])) + "\n"

import random
from pathlib import Path
SAMPLE_IN = '5\n'
SAMPLE_OUT = '7\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(4117)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 04117")
