import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '6 8\n1 2\n1 3\n1 4\n3 2\n3 5\n4 5\n6 4\n6 5\n'
SAMPLE_OUT = 'v1 v3 v2 v6 v4 v5\n'
CASES = ['6 8\n1 2\n1 3\n1 4\n3 2\n3 5\n4 5\n6 4\n6 5\n', '15 18\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n8 15\n1 10\n8 10\n1 9\n', '5 6\n1 2\n2 3\n3 4\n4 5\n2 4\n3 5\n', '10 9\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n', '2 1\n1 2\n', '8 10\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n1 4\n3 8\n4 7\n', '18 28\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n15 16\n16 17\n17 18\n2 18\n11 13\n15 17\n13 18\n3 18\n8 18\n6 14\n4 12\n4 8\n6 8\n10 18\n', '17 21\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n15 16\n16 17\n4 15\n9 16\n6 14\n2 4\n2 8\n', '20 25\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n15 16\n16 17\n17 18\n18 19\n19 20\n4 8\n5 17\n9 14\n5 19\n9 18\n9 20\n', '14 14\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n1 4\n', '11 15\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n5 10\n3 9\n2 5\n3 7\n4 7\n', '16 17\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n15 16\n7 9\n9 15\n', '4 4\n1 2\n2 3\n3 4\n1 3\n', '8 11\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n4 8\n2 8\n1 3\n3 6\n', '16 19\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n15 16\n2 10\n12 14\n4 9\n7 13\n', '14 17\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n1 6\n7 11\n4 12\n8 14\n', '10 15\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n3 9\n5 10\n1 7\n2 6\n6 10\n7 9\n', '18 33\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n15 16\n16 17\n17 18\n5 7\n2 11\n8 11\n4 13\n1 16\n2 16\n5 18\n3 17\n7 13\n4 7\n7 15\n1 13\n12 15\n3 13\n7 12\n11 18\n', '18 31\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n15 16\n16 17\n17 18\n5 18\n4 9\n3 11\n3 17\n5 15\n8 14\n2 6\n8 17\n5 14\n6 18\n7 9\n2 15\n8 12\n3 8\n', '16 20\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n15 16\n5 8\n2 7\n6 10\n9 14\n7 11\n']
REFERENCE_SOURCE = 'import heapq\n\ndef topological_sort(vertices, edges):\n    # Initialize in-degree and connection matrix\n    in_edges = [0] * (vertices + 1)\n    connect = [[0] * (vertices + 1) for _ in range(vertices + 1)]\n\n    # Populate the in-degree and connection matrix\n    for u, v in edges:\n        in_edges[v] += 1\n        connect[u][v] += 1\n\n    # Priority queue for vertices with in-degree of 0\n    queue = []\n    for i in range(1, vertices + 1):\n        if in_edges[i] == 0:\n            heapq.heappush(queue, i)\n\n    # List to store the topological order\n    order = []\n\n    # Processing vertices\n    while queue:\n        u = heapq.heappop(queue)\n        order.append(u)\n        for v in range(1, vertices + 1):\n            if connect[u][v] > 0:\n                in_edges[v] -= connect[u][v]\n                if in_edges[v] == 0:\n                    heapq.heappush(queue, v)\n\n    if len(order) == vertices:\n        return order\n    else:\n        return None\n\n# Read input\nvertices, num_edges = map(int, input().split())\nedges = []\nfor _ in range(num_edges):\n    u, v = map(int, input().split())\n    edges.append((u, v))\n\n# Perform topological sort\norder = topological_sort(vertices, edges)\n\n# Output result\nif order:\n    for i, vertex in enumerate(order):\n        if i < len(order) - 1:\n            print(f"v{vertex}", end=" ")\n        else:\n            print(f"v{vertex}")\nelse:\n    print("No topological order exists due to a cycle in the graph.")\n'
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(4084)
assert CASES[0] == SAMPLE_IN
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
def generate_case(index):
    return CASES[index]
root = Path(__file__).parent / "data"
for index in range(20):
    content = generate_case(index)
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
