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


def valid(text):
    """题面契约：首行 n m；接下来恰 m 行，每行两个整数 a b，0<=a,b<=n-1；
    a != b（不含自环）；
    同一条无向边（a b 与 b a 视为同一条）至多出现一次。题面未给 n 的上限。"""
    try:
        if not text.endswith("\n"):
            return False
        lines = text[:-1].split("\n")
        head = lines[0].split(" ")
        if len(head) != 2:
            return False
        n, m = int(head[0]), int(head[1])
        if n < 1 or m < 0 or len(lines) != m + 1:
            return False
        seen = set()
        for line in lines[1:]:
            parts = line.split(" ")
            if len(parts) != 2:
                return False
            a, b = int(parts[0]), int(parts[1])
            if not (0 <= a < n and 0 <= b < n):
                return False
            if a == b:  # 拉普拉斯矩阵按简单图定义，不出自环
                return False
            key = (min(a, b), max(a, b))
            if key in seen:
                return False
            seen.add(key)
        return True
    except ValueError:
        return False


def make_graph(rng, n, m):
    """n 个点里随机取 m 条互异无向边（不含自环），顶点顺序随机。"""
    if m * 3 > n * (n - 1):
        allpairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        edges = rng.sample(allpairs, m)
    else:
        es = set()
        while len(es) < m:
            u, v = rng.sample(range(n), 2)
            es.add((min(u, v), max(u, v)))
        edges = list(es)
    rng.shuffle(edges)
    edges = [(v, u) if rng.random() < 0.5 else (u, v) for u, v in edges]
    return f"{n} {len(edges)}\n" + "".join(f"{u} {v}\n" for u, v in edges)


def extra_cases():
    rng = random.Random(199430)
    cases = [
        "1 0\n",                         # 单点无边
        "3 0\n",                         # 全是孤立点
        "2 1\n1 0\n",                   # 最小有边图，边逆序给出
        make_graph(rng, 12, 66),         # 完全图 K12
        make_graph(rng, 10, 3),          # 大量孤立点（度为 0 的行全 0）
        make_graph(rng, 60, 200),
        make_graph(rng, 150, 2000),
        make_graph(rng, 300, 300 * 299 // 2 // 3),  # 较大规模稠密图
    ]
    return cases


def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    rng = random.Random(19943)
    root = Path(__file__).parent / "data"
    cases = [SAMPLE_IN]
    while len(cases) < 20:
        case = generate_case(rng)
        if case not in cases:  # 原随机组 4 与 19 曾完全相同，去重
            cases.append(case)
    cases += extra_cases()
    for index, content in enumerate(cases):
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 19943")


if __name__ == "__main__":
    main()
