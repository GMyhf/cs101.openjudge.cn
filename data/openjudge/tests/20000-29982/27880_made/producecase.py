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


def valid(text):
    """题面：首行 n m（1<=n<=300，1<=m<=8000），随后 m 行 u v c（1<=c<=10^4）；
    道路双向，两路口间至多一条道路，所有路口连通。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def nums(line, k):
        parts = line.split(" ")
        if len(parts) != k or not all(x.isdigit() and x == str(int(x)) for x in parts):
            return None
        return list(map(int, parts))
    first = nums(lines[0], 2)
    if first is None:
        return False
    n, m = first
    if not (1 <= n <= 300 and 1 <= m <= 8000 and len(lines) == m + 1):
        return False
    parent = list(range(n + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    seen = set(); comps = n
    for line in lines[1:]:
        e = nums(line, 3)
        if e is None:
            return False
        u, v, c = e
        if not (1 <= u <= n and 1 <= v <= n and u != v and 1 <= c <= 10000):
            return False
        key = (min(u, v), max(u, v))
        if key in seen:
            return False
        seen.add(key)
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv; comps -= 1
    return comps == 1


def build(rng, n, m, cost):
    """随机连通图：随机标号的生成树 + 不重复的额外边，边序与方向打乱。"""
    labels = list(range(1, n + 1)); rng.shuffle(labels)
    edges = []; seen = set()
    for i in range(1, n):
        u, v = labels[i], labels[rng.randrange(i)]
        seen.add((min(u, v), max(u, v))); edges.append((u, v))
    m = min(m, n * (n - 1) // 2)
    if m > n * (n - 1) // 4:
        rest = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1) if (u, v) not in seen]
        rng.shuffle(rest); edges += rest[:m - len(edges)]
    else:
        while len(edges) < m:
            u, v = rng.sample(range(1, n + 1), 2)
            key = (min(u, v), max(u, v))
            if key in seen: continue
            seen.add(key); edges.append((u, v))
    rng.shuffle(edges)
    rows = []
    for u, v in edges:
        if rng.random() < .5: u, v = v, u
        rows.append(f"{u} {v} {cost(rng)}")
    return f"{n} {len(edges)}\n" + "\n".join(rows) + "\n"


def bridge_case(rng):
    """两个大团只靠一条分值 10^4 的桥相连，其余边分值都很小：答案的最大值必为 10^4。"""
    half = 150; rows = []; seen = set()
    for base in (0, half):
        for i in range(2, half + 1):
            u, v = base + i, base + rng.randint(1, i - 1)
            rows.append((u, v, rng.randint(1, 50))); seen.add((min(u, v), max(u, v)))
    while len(rows) < 7999:
        base = rng.choice((0, half))
        u, v = rng.sample(range(base + 1, base + half + 1), 2)
        key = (min(u, v), max(u, v))
        if key in seen: continue
        seen.add(key); rows.append((u, v, rng.randint(1, 9999)))
    rows.append((rng.randint(1, half), rng.randint(half + 1, 2 * half), 10000))
    rng.shuffle(rows)
    return f"300 {len(rows)}\n" + "\n".join(f"{u} {v} {c}" for u, v, c in rows) + "\n"


def generate_cases(rng):
    full = lambda r: r.randint(1, 10000)
    cases = [
        "2 1\n1 2 1\n",                                    # 最小规模
        "2 1\n2 1 10000\n",                                # 最小规模、分值上限
        build(rng, 300, 299, full),                          # 恰好是树
        build(rng, 300, 8000, full),                         # 满规模
        build(rng, 300, 8000, lambda r: 10000),              # 满规模、分值全相同
        build(rng, 300, 8000, lambda r: r.randint(1, 3)),    # 大量重复分值
        bridge_case(rng),                                    # 桥必选
        build(rng, 126, 7875, full),                         # 完全图
        build(rng, 300, 8000, lambda r: r.randint(9990, 10000)),
    ]
    while len(cases) < 19:
        n = rng.choice([rng.randint(2, 10), rng.randint(10, 60), rng.randint(60, 300)])
        m = rng.randint(n - 1, min(8000, n * (n - 1) // 2))
        cases.append(build(rng, n, m, full))
    return cases


def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    rng = random.Random(27880)
    root = Path(__file__).parent / "data"
    for index, content in enumerate([SAMPLE_IN] + generate_cases(rng)):
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print("generated 20 cases for 27880")


import random
from pathlib import Path
SAMPLE_IN = '4 5\n1 2 3\n1 4 5\n2 4 7\n2 3 6\n3 4 8\n'
SAMPLE_OUT = '3 6\n'

if __name__ == "__main__":
    main()
