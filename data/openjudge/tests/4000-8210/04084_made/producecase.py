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

def sample(body, label):
    fence = r"\x60\x60\x60"
    pattern = rf"(?:{label})\s*\n+{fence}\n(.*?){fence}"
    values = re.findall(pattern, body, re.S | re.I)
    if not values: raise ValueError("missing " + label)
    return values[0].strip() + "\n"

def g4084(r):
    n = r.randint(2, 20); edges = [(i, i + 1) for i in range(1, n)]
    for _ in range(r.randint(0, n)):
        a, b = sorted(r.sample(range(1, n + 1), 2))
        if a != b and (a, b) not in edges: edges.append((a, b))
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4084(random.Random(NUMBER + i)) for i in range(1, 20)]

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
