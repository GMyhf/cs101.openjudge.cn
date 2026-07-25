import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "import heapq\n\ndef dijkstra(n, graph, allowed_edges):\n    dist = [float('inf')] * (n + 1)\n    dist[1] = 0\n    pq = [(0, 1)]\n    while pq:\n        time, u = heapq.heappop(pq)\n        if time > dist[u]:\n            continue\n        for v, t in allowed_edges[u]:\n            if dist[v] > time + t:\n                dist[v] = time + t\n                heapq.heappush(pq, (dist[v], v))\n    return dist[n]\n\ndef check(x, n, T, edges):\n    graph = [[] for _ in range(n + 1)]\n    special_edges = []\n\n    for u, v, t, a in edges:\n        if a <= x:\n            graph[u].append((v, t))\n            graph[v].append((u, t))\n        else:\n            special_edges.append((u, v, t))\n\n    # 尝试不使用光学迷彩\n    if dijkstra(n, edges, graph) <= T:\n        return True\n\n    # 尝试每一条特权边作为迷彩边\n    for u, v, t in special_edges:\n        # 暂时加上这条边\n        graph[u].append((v, t))\n        graph[v].append((u, t))\n        if dijkstra(n, edges, graph) <= T:\n            return True\n        # 撤销\n        graph[u].pop()\n        graph[v].pop()\n\n    return False\n\ndef min_armor(n, m, T, edge_list):\n    left, right = 0, 100\n    answer = 100\n    while left <= right:\n        mid = (left + right) // 2\n        if check(mid, n, T, edge_list):\n            answer = mid\n            right = mid - 1\n        else:\n            left = mid + 1\n    return answer\n\n# 读入样例输入\nn, m, T = map(int, input().split())\nedges = [tuple(map(int, input().split())) for _ in range(m)]\n\nprint(min_armor(n, m, T, edges))\n"
SAMPLE_IN = '4 4 6\n1 2 4 0\n2 4 4 10\n1 3 3 50\n3 4 3 60\n'
def generate_case(r):
    n = r.randint(2, 8); edges = [(1, n, r.randint(1, 20), r.randint(0, 100))]
    for v in range(2, n): edges.append((v, v + 1, r.randint(1, 20), r.randint(0, 100)))
    if n >= 3: edges.append((1, 2, r.randint(1, 20), r.randint(0, 100)))
    total = sum(e[2] for e in edges[:n - 1]); limit = total + r.randint(0, 10)
    assert any(u == 1 and v == n for u, v, _, _ in edges)
    return f"{n} {len(edges)} {limit}\n" + "\n".join("%d %d %d %d" % e for e in edges) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(29803 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
