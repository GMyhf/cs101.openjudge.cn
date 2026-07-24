def solve_text(text):
    s = int(text.split()[0]); prime = [True] * (s + 1)
    if s >= 0: prime[0] = False
    if s >= 1: prime[1] = False
    for i in range(2, int(s ** 0.5) + 1):
        if prime[i]:
            for j in range(i * i, s + 1, i): prime[j] = False
    ans = max((p * (s - p) for p in range(2, s)
               if prime[p] and prime[s - p]), default=0)
    return str(ans) + "\n"


def generate_case(rng):
    primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    p, q = rng.choice(primes), rng.choice(primes)
    return f"{p + q}\n"

import random
from pathlib import Path
SAMPLE_IN = '50\n'
SAMPLE_OUT = '589\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(4138)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 04138")
