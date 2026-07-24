def solve_text(text):
    values = list(map(int, text.split())); n = values[0]
    edges = [tuple(values[i:i + 3]) for i in range(2, len(values), 3)]
    parent = list(range(n + 1))
    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]; node = parent[node]
        return node
    count = largest = 0
    for u, v, cost in sorted(edges, key=lambda edge: edge[2]):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv; count += 1; largest = max(largest, cost)
    return f"{count} {largest}\n"


def generate_case(rng):
    # 题面约束:两个交叉路口之间最多一条道路,生成时必须去重
    n = rng.randint(2, 30); edges = [(i, i + 1, rng.randint(1, 10000)) for i in range(1, n)]
    seen = {(u, v) for u, v, _ in edges}
    for _ in range(rng.randint(n, n * 3)):
        u, v = rng.sample(range(1, n + 1), 2)
        key = (min(u, v), max(u, v))
        if key in seen: continue
        seen.add(key); edges.append((u, v, rng.randint(1, 10000)))
    return f"{n} {len(edges)}\n" + "\n".join(f"{u} {v} {c}" for u, v, c in edges) + "\n"

import random
from pathlib import Path
SAMPLE_IN = '4 5\n1 2 3\n1 4 5\n2 4 7\n2 3 6\n3 4 8\n'
SAMPLE_OUT = '3 6\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(27880)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 27880")
