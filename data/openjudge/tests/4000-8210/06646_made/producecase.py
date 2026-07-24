def solve_text(text):
    it = iter(text.split()); n = int(next(it))
    children = [(int(next(it)), int(next(it))) for _ in range(n)]
    def depth(node):
        if node == -1: return 0
        left, right = children[node - 1]
        return 1 + max(depth(left), depth(right))
    return str(depth(1)) + "\n"


def generate_case(rng):
    n = rng.randint(1, 10); children = []
    for i in range(1, n + 1):
        options = list(range(i + 1, n + 1)) + [-1]
        children.append((rng.choice(options), rng.choice(options)))
    return str(n) + "\n" + "\n".join(f"{l} {r}" for l, r in children) + "\n"

import random
from pathlib import Path
SAMPLE_IN = '3\n2 3\n-1 -1\n-1 -1\n'
SAMPLE_OUT = '2\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(6646)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 06646")
