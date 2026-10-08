import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\ninput = sys.stdin.read\ndata = input().split()\n\ndef main():\n    ptr = 0\n    n, t = int(data[ptr]), int(data[ptr+1])\n    ptr += 2\n\n    # 建图\n    adj = [[] for _ in range(n + 1)]\n    for _ in range(n - 1):\n        u = int(data[ptr])\n        v = int(data[ptr+1])\n        adj[u].append(v)\n        adj[v].append(u)\n        ptr += 2\n\n    # 倍增预处理\n    LOG = 18\n    depth = [0] * (n + 1)\n    up = [[0] * LOG for _ in range(n + 1)]\n\n    # DFS 初始化\n    stack = [(t, 0, 0)]\n    while stack:\n        u, fa, d = stack.pop()\n        depth[u] = d\n        up[u][0] = fa\n        for v in adj[u]:\n            if v != fa:\n                stack.append((v, u, d + 1))\n\n    # 构建倍增表\n    for j in range(1, LOG):\n        for i in range(1, n + 1):\n            up[i][j] = up[up[i][j-1]][j-1]\n\n    # LCA\n    def lca(u, v):\n        if depth[u] < depth[v]:\n            u, v = v, u\n        # 对齐深度\n        for j in range(LOG-1, -1, -1):\n            if depth[u] - (1 << j) >= depth[v]:\n                u = up[u][j]\n        if u == v:\n            return u\n        for j in range(LOG-1, -1, -1):\n            if up[u][j] != up[v][j]:\n                u = up[u][j]\n                v = up[v][j]\n        return up[u][0]\n\n    # 第 k 个祖先\n    def kth_ancestor(u, k):\n        for j in range(LOG-1, -1, -1):\n            if k >= (1 << j):\n                u = up[u][j]\n                k -= (1 << j)\n        return u\n\n    # 读取查询数量 m\n    m = int(data[ptr])\n    ptr += 1\n\n    # 处理 m 组查询\n    res = []\n    for _ in range(m):\n        p = int(data[ptr])\n        q = int(data[ptr+1])\n        v1 = int(data[ptr+2])\n        v2 = int(data[ptr+3])\n        ptr += 4\n\n        r = lca(p, q)\n        L = (depth[p] - depth[r]) + (depth[q] - depth[r])\n        days = L // (v1 + v2)\n        s = v1 * days\n\n        # 找相遇点\n        if s <= depth[p] - depth[r]:\n            meet = kth_ancestor(p, s)\n        else:\n            s2 = L - s\n            meet = kth_ancestor(q, s2)\n\n        res.append(f"{days} {depth[meet]}")\n    \n    print(\'\\n\'.join(res))\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = '7 1\n1 2\n1 3\n2 4\n2 5\n3 6\n3 7\n1\n4 7 1 3\n'
def generate_case(r):
    n = r.randint(5, 14); root = 1; edges = [(i, i + 1) for i in range(1, n)]
    qrows = []
    for _ in range(r.randint(2, 8)):
        p = r.randint(1, n - 2); q = p + 2 * r.randint(1, (n - p) // 2)
        qrows.append((p, q, 1, 1))
    return f"{n} {root}\n" + "\n".join(f"{u} {v}" for u, v in edges) + f"\n{len(qrows)}\n" + "\n".join("%d %d %d %d" % row for row in qrows) + "\n"


def valid(text):
    """题面契约：n,t；n-1 条边构成以 t 为根的树（1<=u,v<=n，u!=v）；m 行 p q v1 v2，
    1<=n,m<=2e5，1<=t,p,q<=n，1<=v1,v2<=1e9，且 p 到 q 的距离 L 满足 L mod (v1+v2)=0。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def ints(line, k):
        toks = line.split(" ")
        if len(toks) != k or any(not x.isdigit() or str(int(x)) != x for x in toks):
            return None
        return list(map(int, toks))
    first = ints(lines[0], 2)
    if first is None:
        return False
    n, t = first
    if not (1 <= n <= 200000 and 1 <= t <= n) or len(lines) < n + 1:
        return False
    adj = [[] for _ in range(n + 1)]
    for line in lines[1:n]:
        e = ints(line, 2)
        if e is None:
            return False
        u, v = e
        if not (1 <= u <= n and 1 <= v <= n and u != v):
            return False
        adj[u].append(v); adj[v].append(u)
    # 连通且 n-1 条边 => 树
    par = [0] * (n + 1); dep = [-1] * (n + 1); dep[t] = 0; order = [t]
    for u in order:
        for v in adj[u]:
            if dep[v] < 0:
                dep[v] = dep[u] + 1; par[v] = u; order.append(v)
    if len(order) != n:
        return False
    mline = ints(lines[n], 1)
    if mline is None:
        return False
    m = mline[0]
    if not 1 <= m <= 200000 or len(lines) != n + 1 + m:
        return False
    LOG = max(1, n.bit_length())
    up = [par[:]]
    for j in range(1, LOG):
        prv = up[-1]; up.append([prv[prv[i]] for i in range(n + 1)])
    def lca(a, b):
        if dep[a] < dep[b]:
            a, b = b, a
        d = dep[a] - dep[b]; j = 0
        while d:
            if d & 1:
                a = up[j][a]
            d >>= 1; j += 1
        if a == b:
            return a
        for j in range(LOG - 1, -1, -1):
            if up[j][a] != up[j][b]:
                a = up[j][a]; b = up[j][b]
        return par[a]
    for line in lines[n + 1:]:
        qv = ints(line, 4)
        if qv is None:
            return False
        p, q, v1, v2 = qv
        if not (1 <= p <= n and 1 <= q <= n and 1 <= v1 <= 10**9 and 1 <= v2 <= 10**9):
            return False
        L = dep[p] + dep[q] - 2 * dep[lca(p, q)]
        if L % (v1 + v2):
            return False
    return True


def build_tree(r, n, shape):
    """返回 (根, 打乱标号后的边表)。shape: random / chain / star / caterpillar / binary / broom"""
    par = [0] * (n + 1)
    for i in range(2, n + 1):
        if shape == "chain": par[i] = i - 1
        elif shape == "star": par[i] = 1
        elif shape == "binary": par[i] = i // 2
        elif shape == "caterpillar": par[i] = i - 1 if i <= n // 2 else r.randint(1, n // 2)
        elif shape == "broom": par[i] = i - 1 if i <= n * 3 // 4 else n * 3 // 4
        elif shape == "deep": par[i] = r.randint(max(1, i - 3), i - 1)
        else: par[i] = r.randint(1, i - 1)
    perm = list(range(1, n + 1)); r.shuffle(perm); lab = [0] + perm
    edges = []
    for i in range(2, n + 1):
        u, v = lab[par[i]], lab[i]
        if r.random() < 0.5: u, v = v, u
        edges.append((u, v))
    r.shuffle(edges)
    # 根随机取（不一定是构造时的 1 号点），深度在 build 后另算
    return r.randint(1, n), edges


def make_case(r, n, m, shape, vmode="mixed"):
    root, edges = build_tree(r, n, shape)
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    par = [0] * (n + 1); dep = [-1] * (n + 1); dep[root] = 0; order = [root]
    for u in order:
        for v in adj[u]:
            if dep[v] < 0:
                dep[v] = dep[u] + 1; par[v] = u; order.append(v)
    LOG = max(1, n.bit_length()); up = [par[:]]
    for j in range(1, LOG):
        prv = up[-1]; up.append([prv[prv[i]] for i in range(n + 1)])
    def lca(a, b):
        if dep[a] < dep[b]: a, b = b, a
        d = dep[a] - dep[b]; j = 0
        while d:
            if d & 1: a = up[j][a]
            d >>= 1; j += 1
        if a == b: return a
        for j in range(LOG - 1, -1, -1):
            if up[j][a] != up[j][b]: a = up[j][a]; b = up[j][b]
        return par[a]
    deepest = max(range(1, n + 1), key=lambda x: dep[x])
    rows = []
    while len(rows) < m:
        p = r.randint(1, n)
        roll = r.random()
        if roll < 0.15: q = deepest                          # 拉长路径
        elif roll < 0.25: q = root                           # 端点为根
        else: q = r.randint(1, n)
        if r.random() < 0.5: p, q = q, p
        if p == q: continue
        L = dep[p] + dep[q] - 2 * dep[lca(p, q)]
        divs = [d for d in range(2, min(L, 400) + 1) if L % d == 0]
        if L >= 2: divs.append(L)                            # v1+v2 = L：一天就相遇
        if not divs: continue
        mode = vmode if vmode != "mixed" else r.choice(["small", "small", "big", "edge"])
        if mode == "small": s = r.choice([d for d in divs if d <= 6] or divs)
        elif mode == "big": s = max(divs) if r.random() < 0.5 else r.choice(divs)
        else: s = r.choice(divs)
        k = r.random()
        if mode == "edge" and k < 0.5: v1 = 1 if k < 0.25 else s - 1    # 相遇点紧贴一端
        else: v1 = r.randint(1, s - 1)
        rows.append((p, q, v1, s - v1))
    return (f"{n} {root}\n" + "".join(f"{u} {v}\n" for u, v in edges) + f"{m}\n"
            + "".join("%d %d %d %d\n" % row for row in rows))


def special_cases():
    """替换原第 20..39 组：原数据全是 1-2-3-… 的链、根为 1、v1=v2=1、n<=14。
    规模受单组 .in<=1MB 约束（n,m 无法同时到 2e5），取满 1MB 附近。"""
    r = random.Random(308300)
    plan = [
        (3, 1, "chain"), (3, 3, "star"), (6, 10, "random"), (8, 20, "random"),
        (12, 30, "binary"), (15, 40, "caterpillar"), (30, 60, "random"), (40, 80, "deep"),
        (200, 300, "random"), (500, 500, "broom"), (1000, 2000, "star"), (2000, 3000, "deep"),
        (60000, 8000, "random"), (50000, 12000, "chain"), (50000, 12000, "deep"),
        (55000, 10000, "caterpillar"), (60000, 9000, "binary"), (8000, 38000, "random"),
        (8000, 38000, "chain"), (50000, 12000, "broom"),
    ]
    return [make_case(r, n, m, shape) for n, m, shape in plan]


def main():
    specials = special_cases()
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            elif index >= 20: content = specials[index - 20]
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(30830 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content) and (index == 0 or content not in seen), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
