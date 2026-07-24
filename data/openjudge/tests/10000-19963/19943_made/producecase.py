def solve_text(text):
    values = list(map(int, text.split())); n = values[0]; matrix = [[0] * n for _ in range(n)]
    for i in range(2, len(values), 2):
        u, v = values[i], values[i + 1]
        matrix[u][u] += 1; matrix[v][v] += 1
        matrix[u][v] -= 1; matrix[v][u] -= 1
    return "\n".join(" ".join(map(str, row)) for row in matrix) + "\n"


def generate_case(rng):
    n = rng.randint(2, 15); edges = [(i, i + 1) for i in range(n - 1)]
    for _ in range(rng.randint(0, n * 2)):
        u, v = rng.sample(range(n), 2)
        if (u, v) not in edges and (v, u) not in edges: edges.append((u, v))
    return f"{n} {len(edges)}\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"

import random
from pathlib import Path
SAMPLE_IN = '4 5\n2 1\n1 3\n2 3\n0 1\n0 2\n'
SAMPLE_OUT = '2 -1 -1 0\n-1 3 -1 -1\n-1 -1 3 -1\n0 -1 -1 2\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(19943)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 19943")
