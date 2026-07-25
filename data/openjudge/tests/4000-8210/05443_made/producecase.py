"""5443 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5443
SAMPLE_IN = '6\nGinza\nSensouji\nShinjukugyoen\nUenokouen\nYoyogikouen\nMeijishinguu\n6\nGinza Sensouji 80\nShinjukugyoen Sensouji 40\nGinza Uenokouen 35\nUenokouen Shinjukugyoen 85\nSensouji Meijishinguu 60\nMeijishinguu Yoyogikouen 35\n2\nUenokouen Yoyogikouen\nMeijishinguu Meijishinguu\n'
SAMPLE_OUT = 'Uenokouen->(35)->Ginza->(80)->Sensouji->(60)->Meijishinguu->(35)->Yoyogikouen\nMeijishinguu\n'
REFERENCE_SOURCE = 'import heapq\nimport sys\n\ndef solve():\n    # 读取所有输入数据\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    ptr = 0\n    \n    # 1. 处理地点部分\n    P = int(input_data[ptr])\n    ptr += 1\n    place_names = []\n    name_to_idx = {}\n    for i in range(P):\n        name = input_data[ptr]\n        place_names.append(name)\n        name_to_idx[name] = i\n        ptr += 1\n        \n    # 2. 处理道路部分 (无向图)\n    Q = int(input_data[ptr])\n    ptr += 1\n    adj = [[] for _ in range(P)]\n    for _ in range(Q):\n        u_name = input_data[ptr]\n        v_name = input_data[ptr+1]\n        dist = int(input_data[ptr+2])\n        ptr += 3\n        \n        u, v = name_to_idx[u_name], name_to_idx[v_name]\n        adj[u].append((v, dist))\n        adj[v].append((u, dist))\n        \n    # 3. 处理查询部分\n    R = int(input_data[ptr])\n    ptr += 1\n    for _ in range(R):\n        start_name = input_data[ptr]\n        end_name = input_data[ptr+1]\n        ptr += 2\n        \n        if start_name == end_name:\n            print(start_name)\n            continue\n            \n        start_idx = name_to_idx[start_name]\n        end_idx = name_to_idx[end_name]\n        \n        # Dijkstra 算法\n        distances = [float(\'inf\')] * P\n        parent = [-1] * P\n        edge_to_dist = [0] * P # 记录到达该节点时的那段路程\n        \n        distances[start_idx] = 0\n        pq = [(0, start_idx)]\n        \n        while pq:\n            d, u = heapq.heappop(pq)\n            \n            if d > distances[u]:\n                continue\n            if u == end_idx:\n                break\n                \n            for v, weight in adj[u]:\n                if distances[u] + weight < distances[v]:\n                    distances[v] = distances[u] + weight\n                    parent[v] = u\n                    edge_to_dist[v] = weight\n                    heapq.heappush(pq, (distances[v], v))\n        \n        # 路径回溯\n        path_nodes = []\n        path_edges = []\n        curr = end_idx\n        while curr != -1:\n            path_nodes.append(place_names[curr])\n            if parent[curr] != -1:\n                path_edges.append(edge_to_dist[curr])\n            curr = parent[curr]\n            \n        path_nodes.reverse()\n        path_edges.reverse()\n        \n        # 格式化输出\n        output = []\n        for i in range(len(path_nodes)):\n            output.append(path_nodes[i])\n            if i < len(path_edges):\n                output.append(f"->({path_edges[i]})->")\n        \n        print("".join(output))\n\nif __name__ == "__main__":\n    solve()\n'

def g5443(r):
    import heapq

    def shortest_path_count(p, edges, s, t):
        graph = {i: [] for i in range(p)}
        for (i, j), w in edges.items():
            graph[i].append((j, w)); graph[j].append((i, w))
        dist = [float("inf")] * p; count = [0] * p
        dist[s] = 0; count[s] = 1; heap = [(0, s)]
        while heap:
            du, u = heapq.heappop(heap)
            if du > dist[u]: continue
            for v, w in graph[u]:
                if du + w < dist[v]:
                    dist[v] = du + w; count[v] = count[u]; heapq.heappush(heap, (dist[v], v))
                elif du + w == dist[v]:
                    count[v] += count[u]
        return count[t]

    # 题面要求输出最短路走法本身,输出比对是精确的:必须保证每个查询的最短路唯一
    while True:
        p = r.randint(4, 14); names = [f"Place{i}" for i in range(p)]
        edges = {(i, i + 1): r.randint(1, 999) for i in range(p - 1)}
        for i in range(p):
            for j in range(i + 2, p):
                if len(edges) < 49 and r.random() < .15: edges[(i, j)] = r.randint(1, 999)
        queries = [(r.randrange(p), r.randrange(p)) for _ in range(r.randint(2, 10))]
        if all(shortest_path_count(p, edges, a, b) == 1 for a, b in queries):
            break
    roads = [f"{names[i]} {names[j]} {w}" for (i, j), w in edges.items()]
    return (f"{p}\n" + "\n".join(names) + f"\n{len(roads)}\n" + "\n".join(roads) +
            f"\n{len(queries)}\n" + "\n".join(f"{names[a]} {names[b]}" for a, b in queries) + "\n")

def build_cases():
    return [SAMPLE_IN] + [g5443(random.Random(NUMBER + i)) for i in range(1, 20)]

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
