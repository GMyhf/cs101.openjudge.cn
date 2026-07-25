import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nimport threading\nimport heapq\n\ndef main():\n    input = sys.stdin.readline\n    N, M = map(int, input().split())\n    graph = [[] for _ in range(N+1)]\n    for _ in range(M):\n        A, B, c = map(int, input().split())\n        graph[A].append((B, c))\n    INF = 10**30\n    dist = [INF] * (N+1)\n    dist[1] = 0\n    pq = [(0, 1)]  # (当前距离, 节点)\n    while pq:\n        d, u = heapq.heappop(pq)\n        if d > dist[u]:\n            continue\n        if u == N:\n            break    # 提前退出\n        for v, w in graph[u]:\n            nd = d + w\n            if nd < dist[v]:\n                dist[v] = nd\n                heapq.heappush(pq, (nd, v))\n    # 输出从 1 到 N 的最短路距离，即为最大可实现的 x_N - x_1\n    print(dist[N])\n\nif __name__ == "__main__":\n    threading.Thread(target=main).start()\n'
SAMPLE_IN = '2 2\n1 2 5\n2 1 4\n'
SAMPLE_OUT = '5\n'
def generate_case(r):
    n = r.randint(3, 20); edges = [(i, i + 1, r.randint(1, 30)) for i in range(1, n)]
    for _ in range(r.randint(0, n * 2)):
        a, b = sorted(r.sample(range(1, n + 1), 2)); edges.append((a, b, r.randint(1, 30)))
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b} {w}" for a, b, w in edges) + "\n"

assert SAMPLE_IN == '2 2\n1 2 5\n2 1 4\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(3424 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
