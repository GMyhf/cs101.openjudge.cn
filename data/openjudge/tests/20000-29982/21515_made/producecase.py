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

def valid(text):
    """题面：第一行 N P K（0<=K<N<=1000，1<=P<=2000）；接下来 P 行 A_i B_i L_i，A_i,B_i 为基站编号 1..N。
    题面没给 L_i 范围，这里只要求非负整数（升级花费）。"""
    try:
        lines = text.split('\n')
        while lines and lines[-1].strip() == '':
            lines.pop()
        if not lines:
            return False
        head = lines[0].split()
        if len(head) != 3:
            return False
        n, p, k = map(int, head)
        if not (0 <= k < n <= 1000 and 1 <= p <= 2000) or len(lines) != p + 1:
            return False
        for ln in lines[1:]:
            t = ln.split()
            if len(t) != 3:
                return False
            a, b, w = map(int, t)
            if not (1 <= a <= n and 1 <= b <= n and w >= 0):
                return False
        return True
    except ValueError:
        return False


def fmt(n, k, edges):
    return f"{n} {len(edges)} {k}\n" + "\n".join(f"{a} {b} {w}" for a, b, w in edges) + "\n"


def random_graph(r, n, p, wmax, connected=True, comp_split=None):
    """不含自环与重边的随机无向图；comp_split 给出时 1..split 与 split+1..n 互不连通（1 与 N 不连通）。"""
    pairs, edges = set(), []
    def add(a, b):
        if a != b and frozenset((a, b)) not in pairs:
            pairs.add(frozenset((a, b))); edges.append((a, b, r.randint(1, wmax)))
    groups = [list(range(1, n + 1))] if comp_split is None else [list(range(1, comp_split + 1)), list(range(comp_split + 1, n + 1))]
    if connected:
        for g in groups:
            for i in range(1, len(g)):
                add(g[i], g[r.randrange(i)])
    while len(edges) < p:
        g = r.choice(groups)
        if len(g) >= 2:
            a, b = r.sample(g, 2); add(a, b)
    r.shuffle(edges)
    return edges


def specials():
    r = random.Random(21515)
    out = []
    out.append(fmt(2, 0, [(1, 2, 7)]))                              # 最小规模
    out.append(fmt(2, 1, [(2, 1, 1000000)]))                        # K 覆盖全部路径 → 0
    out.append(fmt(4, 3, [(1, 2, 5), (3, 4, 6)]))                   # 不连通 → -1
    out.append(fmt(1000, 999, random_graph(r, 1000, 2000, 10**6, comp_split=500)))   # 大规模不连通 → -1
    chain = [(i, i + 1, r.randint(1, 10**6)) for i in range(1, 1000)]
    out.append(fmt(1000, 0, chain + [(1, 1000, 10**6)]))            # 长链 + 一条贵的直连边，K=0
    out.append(fmt(1000, 998, chain))                               # 单链长 999，K=998：只剩最便宜的一条要付
    out.append(fmt(1000, 0, random_graph(r, 1000, 2000, 10**6)))
    out.append(fmt(1000, 1, random_graph(r, 1000, 1050, 10**6)))   # 近似树，1 到 N 跳数多于 K
    out.append(fmt(1000, 999, random_graph(r, 1000, 2000, 10**6)))  # K=N-1 → 0
    # 稀疏长路：网格状长路，K 适中，避免只靠直连
    edges = []
    for i in range(1, 1000):
        edges.append((i, i + 1, r.randint(1, 10**6)))
        if i + 2 <= 1000 and r.random() < .5:
            edges.append((i, i + 2, r.randint(1, 10**6)))
    out.append(fmt(1000, 37, edges))
    out.append(fmt(1000, 400, edges[::-1]))
    out.append(fmt(1000, 3, random_graph(r, 1000, 999, 30)))         # 树，权值很小、大量相同
    return out


def main():
    assert SAMPLE_IN == '5 7 1\n1 2 5\n3 1 4\n2 4 8\n3 2 3\n5 2 9\n3 4 7\n4 5 6\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        contents = []
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(21515 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            seen.append(content)
            contents.append(content)
        contents += specials()
        assert all(valid(c) for c in contents) and len(set(contents)) == len(contents)
        for index, content in enumerate(contents):
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
