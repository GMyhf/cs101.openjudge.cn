"""5443 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 31 组数据（第 20 组起为边界组与 P=29/Q=49/R=19 的满规模组）。

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

def valid(text):
    """题面：P（P<30）后跟 P 行地点名（长度不超过 20）；Q（Q<50）后跟 Q 行「地点 地点 距离」；
    R（R<20）后跟 R 行「地点 地点」。地点名互异、道路与查询只用已列出的地点、距离为整数（取正整数）。"""
    lines = text.split("\n")
    if lines[-1] != "":
        return False
    lines = lines[:-1]; pos = 0

    def count(limit):
        nonlocal pos
        if pos >= len(lines) or not lines[pos].isdigit() or not int(lines[pos]) < limit:
            return None
        pos += 1
        return int(lines[pos - 1])

    p = count(30)
    if not p or pos + p > len(lines):
        return False
    names = lines[pos:pos + p]; pos += p
    if len(set(names)) != p or not all(1 <= len(x) <= 20 and x.isprintable() and " " not in x for x in names):
        return False
    known = set(names)
    q = count(50)
    if q is None or pos + q > len(lines):
        return False
    seen = set()
    for line in lines[pos:pos + q]:
        parts = line.split(" ")
        if len(parts) != 3 or parts[0] not in known or parts[1] not in known or parts[0] == parts[1]:
            return False
        if not parts[2].isdigit() or int(parts[2]) < 1 or frozenset(parts[:2]) in seen:
            return False
        seen.add(frozenset(parts[:2]))
    pos += q
    r = count(20)
    if r is None or pos + r != len(lines):
        return False
    return all(len(line.split(" ")) == 2 and all(x in known for x in line.split(" ")) for line in lines[pos:])


def _unique_paths(text):
    """出题方自加的要求：每个查询可达且最短路唯一（输出是走法本身，必须确定）。"""
    import heapq
    tok = text.split(); p = int(tok[0]); names = tok[1:1 + p]; idx = {x: i for i, x in enumerate(names)}
    q = int(tok[1 + p]); at = 2 + p; adj = [[] for _ in range(p)]
    for _ in range(q):
        u, v, w = idx[tok[at]], idx[tok[at + 1]], int(tok[at + 2]); at += 3
        adj[u].append((v, w)); adj[v].append((u, w))
    r = int(tok[at]); at += 1
    for _ in range(r):
        s, t = idx[tok[at]], idx[tok[at + 1]]; at += 2
        dist = [None] * p; ways = [0] * p; dist[s] = 0; ways[s] = 1; heap = [(0, s)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]: continue
            for v, w in adj[u]:
                if dist[v] is None or d + w < dist[v]:
                    dist[v] = d + w; ways[v] = ways[u]; heapq.heappush(heap, (dist[v], v))
                elif d + w == dist[v]:
                    ways[v] += ways[u]
        if ways[t] != 1:
            return False
    return True


def g5443_big(r, p, q, rq, name_len, wmax=999):
    """随机生成树打底（不再总是链），补边到 q 条；地点名长度可到 20；查询含起终点相同的情形。"""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    while True:
        names = set()
        while len(names) < p:
            names.add("".join(r.choice(alphabet) for _ in range(r.randint(1, name_len))))
        names = sorted(names); r.shuffle(names)
        edges = {}
        for i in range(1, p):
            j = r.randrange(i)
            edges[(j, i)] = r.randint(1, wmax)
        pairs = [(i, j) for i in range(p) for j in range(i + 1, p) if (i, j) not in edges]
        r.shuffle(pairs)
        for e in pairs[:max(0, q - len(edges))]:
            edges[e] = r.randint(1, wmax)
        roads = [(a, b, w) if r.random() < .5 else (b, a, w) for (a, b), w in edges.items()]
        r.shuffle(roads)
        queries = [(r.randrange(p), r.randrange(p)) for _ in range(rq)]
        queries[0] = (queries[0][0], queries[0][0])
        text = (f"{p}\n" + "".join(x + "\n" for x in names) + f"{len(roads)}\n" +
                "".join(f"{names[a]} {names[b]} {w}\n" for a, b, w in roads) +
                f"{len(queries)}\n" + "".join(f"{names[a]} {names[b]}\n" for a, b in queries))
        if _unique_paths(text):
            return text


def build_cases():
    cases = [SAMPLE_IN] + [g5443(random.Random(NUMBER + i)) for i in range(1, 20)]
    r = random.Random(544300)
    cases.append("1\nOnlyOne\n0\n1\nOnlyOne OnlyOne\n")                      # 最小规模
    cases.append("2\nA\nB\n1\nB A 7\n2\nA B\nB A\n")                         # 道路两个方向都要走
    for p, q, rq, nl in ((29, 49, 19, 20), (29, 28, 19, 20), (29, 49, 19, 3), (29, 40, 19, 20),
                         (20, 49, 19, 20), (10, 45, 19, 8), (29, 35, 19, 12), (29, 49, 19, 20)):
        cases.append(g5443_big(r, p, q, rq, nl))
    cases.append(g5443_big(r, 29, 49, 19, 20, wmax=9))   # 小权值，靠唯一性筛选
    return cases

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
    assert all(valid(c) for c in cases), "有数据越出题面约束"
    assert all(_unique_paths(c) for c in cases), "有查询的最短路不唯一或不可达"
    assert len(set(cases)) == len(cases), "有重复组"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
