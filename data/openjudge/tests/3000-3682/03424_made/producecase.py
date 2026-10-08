import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nimport threading\nimport heapq\n\ndef main():\n    input = sys.stdin.readline\n    N, M = map(int, input().split())\n    graph = [[] for _ in range(N+1)]\n    for _ in range(M):\n        A, B, c = map(int, input().split())\n        graph[A].append((B, c))\n    INF = 10**30\n    dist = [INF] * (N+1)\n    dist[1] = 0\n    pq = [(0, 1)]  # (当前距离, 节点)\n    while pq:\n        d, u = heapq.heappop(pq)\n        if d > dist[u]:\n            continue\n        if u == N:\n            break    # 提前退出\n        for v, w in graph[u]:\n            nd = d + w\n            if nd < dist[v]:\n                dist[v] = nd\n                heapq.heappush(pq, (nd, v))\n    # 输出从 1 到 N 的最短路距离，即为最大可实现的 x_N - x_1\n    print(dist[N])\n\nif __name__ == "__main__":\n    threading.Thread(target=main).start()\n'
SAMPLE_IN = '2 2\n1 2 5\n2 1 4\n'
SAMPLE_OUT = '5\n'

def valid(text):
    """题面：首行 N M（N<=30000，M<=150000），孩子编号 1..N；随后 M 行 "A B c"（1<=A,B<=N）。
    提示 32 位有符号整数足够 → c 限定在 int32 内；"difference is guaranteed to be finite" → N 从 1 可达。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def ints(ln, k):
        t = ln.split(" ")
        if len(t) != k:
            return None
        try:
            v = [int(x) for x in t]
        except ValueError:
            return None
        if [str(x) for x in v] != t:
            return None
        return v
    h = ints(lines[0], 2)
    if h is None:
        return False
    n, m = h
    if not (1 <= n <= 30000 and 0 <= m <= 150000) or len(lines) != m + 1:
        return False
    adj = [[] for _ in range(n + 1)]
    for ln in lines[1:]:
        e = ints(ln, 3)
        if e is None:
            return False
        a, b, c = e
        if not (1 <= a <= n and 1 <= b <= n and -2**31 <= c < 2**31):
            return False
        adj[a].append((b, c))
    seen = [False] * (n + 1); seen[1] = True; st = [1]
    while st:
        u = st.pop()
        for v, _ in adj[u]:
            if not seen[v]:
                seen[v] = True; st.append(v)
    if not seen[n]:
        return False
    # "guaranteed to be finite" 且 "32 位有符号整数足够"：1→N 最短路存在（无可影响它的负环）且落在 int32 内
    INF = float("inf")
    if all(c >= 0 for row in adj for _, c in row):
        import heapq
        dist = [INF] * (n + 1); dist[1] = 0; pq = [(0, 1)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, c in adj[u]:
                if d + c < dist[v]:
                    dist[v] = d + c; heapq.heappush(pq, (d + c, v))
    else:
        radj = [[] for _ in range(n + 1)]
        for u in range(1, n + 1):
            for v, _ in adj[u]:
                radj[v].append(u)
        back = [False] * (n + 1); back[n] = True; st = [n]
        while st:
            u = st.pop()
            for v in radj[u]:
                if not back[v]:
                    back[v] = True; st.append(v)
        keep = [seen[i] and back[i] for i in range(n + 1)]
        es = [(u, v, c) for u in range(1, n + 1) if keep[u] for v, c in adj[u] if keep[v]]
        dist = [INF] * (n + 1); dist[1] = 0
        for it in range(n + 1):
            changed = False
            for u, v, c in es:
                if dist[u] + c < dist[v]:
                    dist[v] = dist[u] + c; changed = True
            if not changed:
                break
        else:
            return False   # 1→N 路径上有负环，答案无界
    return -2**31 <= dist[n] < 2**31

def generate_case(r, index):
    """c 取非负（原题 POJ 3159 数据即如此，参考解 Dijkstra 依赖于此）。"""
    N, M = 30000, 150000
    edges = []
    nreq = None
    def path(n, wlo, whi):
        perm = [1] + r.sample(range(2, n), n - 2) + [n] if n > 2 else list(range(1, n + 1))
        k = r.randint(1, n - 1) if n > 2 else 1
        rank = {x: i for i, x in enumerate(perm)}
        mid = sorted(r.sample(perm[1:-1], k - 1), key=rank.__getitem__) if k > 1 else []
        p = [1] + mid + [n]
        return [(p[i], p[i + 1], r.randint(wlo, whi)) for i in range(len(p) - 1)]
    if index == 1:
        n = 2; edges = [(1, 2, r.randint(0, 50))]
    elif index == 2:
        n = 2; edges = [(1, 2, 7), (1, 2, 3), (2, 1, 0), (1, 1, 5), (2, 2, 0), (1, 2, 9)]
    elif index in (3, 4):
        n = N; edges = path(n, 0, 10000)
        hi = 10000 if index == 3 else 100
        nreq = len(edges)
        while len(edges) < M:
            edges.append((r.randint(1, n), r.randint(1, n), r.randint(0, hi)))
    elif index == 5:
        # 一条长链（每段权 10000），答案约 3e8，检验累加不溢出 32 位
        n = N; edges = [(i, i + 1, 10000) for i in range(1, n)]
        nreq = len(edges)
        while len(edges) < M:
            a = r.randint(1, n); b = r.randint(1, n)
            edges.append((a, b, 10000 * abs(b - a) + r.randint(1, 50) if b > a else r.randint(0, 10000)))
    elif index == 6:
        n = N; edges = [(1, n, 0)] + [(r.randint(1, n), r.randint(1, n), r.randint(0, 10)) for _ in range(M - 1)]  # 答案 0
        nreq = 1
    elif index == 7:
        # 大量 0 权边
        n = N; edges = path(n, 0, 3)
        nreq = len(edges)
        while len(edges) < M:
            edges.append((r.randint(1, n), r.randint(1, n), r.choice((0, 0, 0, 1, 2))))
    elif index == 8:
        # 网格状 DAG：大量等价路径，SPFA/朴素 Bellman-Ford 吃亏
        W = 150; H = N // W; n = W * H
        idx = lambda x, y: x * W + y + 1
        for x in range(H):
            for y in range(W):
                if y + 1 < W: edges.append((idx(x, y), idx(x, y + 1), r.randint(0, 1000)))
                if x + 1 < H: edges.append((idx(x, y), idx(x + 1, y), r.randint(0, 1000)))
        nreq = len(edges)
        while len(edges) < M:
            u = r.randint(1, n); v = r.randint(1, n)
            edges.append((u, v, r.randint(500, 1000)))
    elif index == 9:
        # 许多点从 1 不可达，且大量反向边
        n = N; reach = n // 3
        edges = [(1, i, r.randint(0, 1000)) for i in range(2, reach + 1)] + [(reach, n, r.randint(0, 1000))]
        nreq = len(edges)
        while len(edges) < M:
            u = r.randint(reach + 1, n); v = r.randint(1, n)
            edges.append((u, v, r.randint(0, 1000)))
    elif index <= 15:
        n = r.randint(1000, N); m = r.randint(n, M); edges = path(n, 0, 10000)
        nreq = len(edges)
        while len(edges) < m:
            edges.append((r.randint(1, n), r.randint(1, n), r.randint(0, 10000)))
    else:
        n = r.randint(3, 20); m = r.randint(n, 60); edges = path(n, 0, 30)
        nreq = len(edges)
        while len(edges) < m:
            edges.append((r.randint(1, n), r.randint(1, n), r.randint(0, 30)))
    # 评测数据单组 .in 限 1MB：N=30000 时一行约 15 字节，M 只能做到 6 万多条；
    # data/ 合计限 10MB：只有第 3（随机满规模）、5（长链）、8（网格，卡 SPFA）组用满 1MB，
    # 其余大组压到约 350KB。先生成的是保证可达的必需边，超出预算时只从尾部截掉随机边。
    if nreq is None: nreq = len(edges)
    budget = 1000000 - 16 if index in (3, 5, 8) else 350000
    size = len(f"{n} {len(edges)}\n") + sum(len(f"{a} {b} {w}\n") for a, b, w in edges)
    while size > budget and len(edges) > nreq:
        a, b, w = edges.pop(); size -= len(f"{a} {b} {w}\n")
    r.shuffle(edges)
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b} {w}" for a, b, w in edges) + "\n"

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        root.mkdir(exist_ok=True)
        seen = [SAMPLE_IN]
        for index in range(25):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(3424 + index + attempt * 1000), index)
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            assert valid(content), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
