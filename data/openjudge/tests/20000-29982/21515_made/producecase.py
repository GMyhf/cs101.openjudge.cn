import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nfrom collections import deque\n\n\ndef main():\n    data = sys.stdin.read().split()\n    if not data:\n        return\n\n    it = iter(data)\n    n = int(next(it));\n    p = int(next(it));\n    k = int(next(it))\n\n    graph = [[] for _ in range(n + 1)]\n    max_edge = 0\n    for _ in range(p):\n        a = int(next(it));\n        b = int(next(it));\n        l = int(next(it))\n        graph[a].append((b, l))\n        graph[b].append((a, l))\n        if l > max_edge:\n            max_edge = l\n\n    # 特殊情况：如果 1 和 n 不连通？0-1 BFS 会处理（dist[n] 保持 inf）\n\n    def can(x):\n        # dist[i] = 从 1 到 i 路径上 权重 > x 的边的最小数量\n        INF = 10 ** 9\n        dist = [INF] * (n + 1)\n        dist[1] = 0\n        dq = deque([1])\n\n        while dq:\n            u = dq.popleft()\n            for v, w in graph[u]:\n                # 如果 w <= x，这条边免费（不计入代价）；否则代价为1\n                cost = 1 if w > x else 0\n                new_cost = dist[u] + cost\n                if new_cost < dist[v] and new_cost <= k:  # 剪枝：超过k没必要继续\n                    dist[v] = new_cost\n                    if cost == 0:\n                        dq.appendleft(v)\n                    else:\n                        dq.append(v)\n        return dist[n] <= k\n\n    # 二分答案：最小的 x 使得 can(x) 为 True\n    lo = 0\n    hi = max_edge + 1  # 注意：答案可能为0，也可能需要比max_edge更大？但题目允许K>=0，所以max_edge足够\n\n    # 但注意：有可能最优解是0（所有边<=0？但Li>=0），或甚至不需要任何边>lim\n    # 另外，有可能即使 lim = max_edge 也不连通 → 输出 -1\n\n    if not can(hi):\n        print(-1)\n        return\n\n    ans = -1\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if can(mid):\n            ans = mid\n            hi = mid\n        else:\n            lo = mid + 1\n\n    print(ans)\n\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = '5 7 1\n1 2 5\n3 1 4\n2 4 8\n3 2 3\n5 2 9\n3 4 7\n4 5 6\n'
SAMPLE_OUT = '4\n'
def generate_case(r):
    n = r.randint(3, 15); edges = [(i, i + 1, r.randint(1, 50)) for i in range(1, n)]
    pairs = {frozenset((a, b)) for a, b, _ in edges}
    for _ in range(r.randint(0, n)):
        a, b = r.sample(range(1, n + 1), 2); pair = frozenset((a, b))
        if pair not in pairs:
            pairs.add(pair); edges.append((a, b, r.randint(1, 50)))
    assert len(pairs) == len(edges) and all(a != b and w > 0 for a, b, w in edges)
    return f"{n} {len(edges)} {r.randint(0, min(4, n - 1))}\n" + "\n".join(f"{a} {b} {w}" for a, b, w in edges) + "\n"

assert SAMPLE_IN == '5 7 1\n1 2 5\n3 1 4\n2 4 8\n3 2 3\n5 2 9\n3 4 7\n4 5 6\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(21515 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
