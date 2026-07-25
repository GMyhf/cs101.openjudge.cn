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

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(30830 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
