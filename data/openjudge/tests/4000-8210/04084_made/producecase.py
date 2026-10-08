"""4084 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4084
SAMPLE_IN = '6 8\n1 2\n1 3\n1 4\n3 2\n3 5\n4 5\n6 4\n6 5\n'
SAMPLE_OUT = 'v1 v3 v2 v6 v4 v5\n'
REFERENCE_SOURCE = 'import heapq\n\ndef topological_sort(vertices, edges):\n    # Initialize in-degree and connection matrix\n    in_edges = [0] * (vertices + 1)\n    connect = [[0] * (vertices + 1) for _ in range(vertices + 1)]\n\n    # Populate the in-degree and connection matrix\n    for u, v in edges:\n        in_edges[v] += 1\n        connect[u][v] += 1\n\n    # Priority queue for vertices with in-degree of 0\n    queue = []\n    for i in range(1, vertices + 1):\n        if in_edges[i] == 0:\n            heapq.heappush(queue, i)\n\n    # List to store the topological order\n    order = []\n\n    # Processing vertices\n    while queue:\n        u = heapq.heappop(queue)\n        order.append(u)\n        for v in range(1, vertices + 1):\n            if connect[u][v] > 0:\n                in_edges[v] -= connect[u][v]\n                if in_edges[v] == 0:\n                    heapq.heappush(queue, v)\n\n    if len(order) == vertices:\n        return order\n    else:\n        return None\n\n# Read input\nvertices, num_edges = map(int, input().split())\nedges = []\nfor _ in range(num_edges):\n    u, v = map(int, input().split())\n    edges.append((u, v))\n\n# Perform topological sort\norder = topological_sort(vertices, edges)\n\n# Output result\nif order:\n    for i, vertex in enumerate(order):\n        if i < len(order) - 1:\n            print(f"v{vertex}", end=" ")\n        else:\n            print(f"v{vertex}")\nelse:\n    print("No topological order exists due to a cycle in the graph.")\n'

def g4084(r):
    n = r.randint(2, 20); edges = [(i, i + 1) for i in range(1, n)]
    for _ in range(r.randint(0, n)):
        a, b = sorted(r.sample(range(1, n + 1), 2))
        if a != b and (a, b) not in edges: edges.append((a, b))
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges) + "\n"

def valid(text):
    """题面契约：首行 v a（v<=100, a<=500），随后恰好 a 行弧 “u w”，端点在 1..v；
    要求输出拓扑序，故图须无环（自环亦视为环）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    try:
        head = lines[0].split(" ")
        if len(head) != 2:
            return False
        v, a = int(head[0]), int(head[1])
        if not (1 <= v <= 100 and 0 <= a <= 500) or len(lines) != a + 1:
            return False
        indeg = [0] * (v + 1)
        adj = [[] for _ in range(v + 1)]
        for line in lines[1:]:
            t = line.split(" ")
            if len(t) != 2:
                return False
            x, y = int(t[0]), int(t[1])
            if not (1 <= x <= v and 1 <= y <= v):
                return False
            adj[x].append(y)
            indeg[y] += 1
    except ValueError:
        return False
    stack = [i for i in range(1, v + 1) if indeg[i] == 0]
    seen = 0
    while stack:
        x = stack.pop()
        seen += 1
        for y in adj[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                stack.append(y)
    return seen == v


def random_dag(r, v, a, layered=False):
    """随机 DAG：先给顶点随机打乱一个拓扑次序，再只连“前 -> 后”的弧，无重边。"""
    order = list(range(1, v + 1))
    r.shuffle(order)
    a = min(a, v * (v - 1) // 2)
    arcs = set()
    while len(arcs) < a:
        i, j = sorted(r.sample(range(v), 2))
        if layered and j - i > 12:
            continue
        arcs.add((order[i], order[j]))
    arcs = list(arcs)
    r.shuffle(arcs)
    return f"{v} {len(arcs)}\n" + "".join(f"{x} {y}\n" for x, y in arcs)


def extra_cases():
    """原 1..19 组都含主链 1->2->…->n，答案恒为 v1 v2 … vn，按编号直接输出也能过；
    这里补随机编号的 DAG、满规模（v=100, a=500）、无弧、孤立点等。"""
    r = random.Random(NUMBER * 7 + 1)
    cases = ["1 0\n", "2 1\n2 1\n", "5 0\n", "3 2\n3 1\n2 1\n"]
    # 逆链 100 -> 99 -> … -> 1：只有一种拓扑序，且与编号完全相反
    cases.append("100 99\n" + "".join(f"{i + 1} {i}\n" for i in range(1, 100)))
    # 大号指向一大批小号：FIFO 队列与最小堆结果不同
    arcs = [(100, i) for i in range(1, 100)] + [(i, i - 1) for i in range(60, 30, -1)]
    cases.append(f"100 {len(arcs)}\n" + "".join(f"{x} {y}\n" for x, y in arcs))
    for k in range(6):
        cases.append(random_dag(r, 100, 500, layered=(k % 2 == 1)))
    for k in range(4):
        cases.append(random_dag(r, r.randint(30, 100), r.randint(50, 300)))
    for k in range(4):
        cases.append(random_dag(r, r.randint(5, 15), r.randint(3, 20)))
    return cases


def build_cases():
    return [SAMPLE_IN] + [g4084(random.Random(NUMBER + i)) for i in range(1, 20)] + extra_cases()

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
