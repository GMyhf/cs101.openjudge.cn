import random, subprocess, tempfile
from pathlib import Path
SAMPLE_IN = '2\n7 6\n1 2\n1 3\n2 4\n2 5\n3 6\n3 7\n12 13\n1 2\n2 3\n2 4\n3 5\n5 6\n4 6\n6 7\n7 8\n8 4\n7 9\n9 10\n10 11\n10 12\n'
SAMPLE_OUT = 'No\nYes\n'
CASES = ['2\n7 6\n1 2\n1 3\n2 4\n2 5\n3 6\n3 7\n12 13\n1 2\n2 3\n2 4\n3 5\n5 6\n4 6\n6 7\n7 8\n8 4\n7 9\n9 10\n10 11\n10 12\n', '1\n8 7\n4 4\n6 5\n1 1\n3 3\n2 2\n7 5\n5 2\n', '1\n5 4\n4 3\n1 1\n3 2\n2 2\n', '1\n16 17\n11 1\n8 8\n13 8\n14 14\n6 5\n12 10\n1 1\n5 4\n15 1\n1 16\n7 3\n16 1\n10 6\n2 2\n3 2\n4 1\n9 4\n', '1\n21 20\n20 14\n14 7\n5 4\n8 3\n2 2\n15 2\n18 10\n12 9\n9 4\n17 17\n16 9\n7 6\n3 2\n4 4\n19 1\n10 4\n1 1\n11 3\n13 9\n6 3\n', '1\n15 14\n2 1\n1 1\n5 1\n4 2\n12 3\n9 5\n10 10\n3 3\n7 6\n8 6\n11 5\n6 6\n14 2\n13 5\n', '1\n17 18\n6 2\n9 7\n17 1\n8 1\n1 1\n5 1\n12 9\n14 6\n16 12\n1 17\n3 3\n10 6\n13 6\n7 2\n2 2\n11 5\n15 12\n4 1\n', '1\n7 6\n2 1\n6 5\n5 4\n1 1\n3 3\n4 1\n', '1\n13 14\n7 4\n2 1\n13 1\n3 1\n6 1\n1 1\n10 1\n11 9\n12 6\n1 13\n9 8\n5 3\n8 2\n4 1\n', '1\n24 25\n4 3\n10 9\n11 8\n16 4\n7 7\n1 24\n20 13\n14 6\n12 6\n3 3\n5 3\n19 5\n8 8\n2 1\n24 1\n15 7\n6 4\n13 13\n21 2\n22 12\n23 20\n17 16\n1 1\n9 6\n18 8\n', '1\n13 14\n7 4\n8 8\n2 1\n13 1\n1 1\n6 4\n4 2\n11 6\n12 12\n1 13\n3 2\n9 7\n10 2\n5 2\n', '1\n5 6\n2 1\n1 5\n4 3\n1 1\n5 1\n3 3\n', '1\n19 20\n9 2\n2 2\n11 11\n16 16\n18 10\n4 2\n12 3\n14 3\n8 5\n10 8\n6 4\n7 3\n3 2\n5 2\n17 10\n19 1\n1 1\n13 3\n15 6\n1 19\n', '1\n21 20\n20 5\n12 7\n3 1\n11 2\n10 6\n17 15\n16 13\n2 1\n19 17\n15 1\n6 4\n18 9\n7 6\n5 2\n4 4\n14 8\n8 1\n9 9\n1 1\n13 12\n', '1\n7 6\n5 5\n2 1\n1 1\n3 3\n6 6\n4 1\n', '1\n9 8\n5 5\n2 1\n6 5\n4 3\n7 5\n1 1\n8 3\n3 2\n', '1\n11 12\n11 1\n8 8\n2 1\n7 5\n1 11\n10 4\n1 1\n5 1\n4 2\n3 2\n6 3\n9 4\n', '1\n8 7\n1 1\n5 1\n7 2\n2 2\n3 2\n6 3\n4 1\n', '1\n21 20\n4 3\n3 1\n5 4\n11 8\n15 11\n18 7\n14 6\n12 12\n20 19\n17 14\n8 8\n2 1\n19 17\n6 1\n13 13\n9 3\n1 1\n10 7\n7 2\n16 8\n', '1\n16 15\n6 2\n7 1\n13 7\n1 1\n10 1\n4 2\n11 6\n15 10\n8 3\n3 3\n14 3\n2 2\n9 7\n12 8\n5 2\n']
REFERENCE_SOURCE = "# 蒋子轩 工院\nfrom collections import deque,defaultdict\ndef topo_sort(graph):\n    in_degree={u:0 for u in range(1,n+1)}\n    for u in graph:\n        for v in graph[u]:\n            in_degree[v]+=1\n    q=deque([u for u in in_degree if in_degree[u]==0])\n    topo_order=[]\n    while q:\n        u=q.popleft()\n        topo_order.append(u)\n        for v in graph[u]:\n            in_degree[v]-=1\n            if in_degree[v]==0:\n                q.append(v)\n    if len(topo_order)!=len(graph):\n        return 'Yes'\n    return 'No'\nfor _ in range(int(input())):\n    n,m=map(int,input().split())\n    graph=defaultdict(list)\n    for _ in range(m):\n        u,v=map(int,input().split())\n        graph[u].append(v)\n    print(topo_sort(graph))\n"
assert CASES[0] == SAMPLE_IN
random.seed(9202)
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index, content in enumerate(CASES):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
