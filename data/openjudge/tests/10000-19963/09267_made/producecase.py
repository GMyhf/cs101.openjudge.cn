def solve_text(text):
    n, m = map(int, text.split()); states = [0] * m; states[0] = 1
    for _ in range(n):
        next_states = [0] * m
        for run, count in enumerate(states):
            next_states[0] += count
            if run + 1 < m: next_states[run + 1] += count
        states = next_states
    return str(sum(states)) + "\n"


def generate_case(rng): return f"{rng.randint(2, 49)} {rng.randint(2, 5)}\n"

import random
from pathlib import Path
SAMPLE_IN = '4 3\n'
SAMPLE_OUT = '13\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(9267)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 09267")
