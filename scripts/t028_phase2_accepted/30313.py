# External reference: http://cs101.openjudge.cn/practice/30313/statistics/
# Accepted submission: 52809923
# Source: http://cs101.openjudge.cn/practice/solution/52809923/
# License: not declared on the submission page; no license is inferred.

import sys

input = sys.stdin.readline
write = sys.stdout.write

n, m = map(int, input().split())

edges = [None] * m
forbidden = [set() for _ in range(n + 1)]

for i in range(m):
    u, v, w = map(int, input().split())
    edges[i] = (w, u, v)
    forbidden[u].add(v)
    forbidden[v].add(u)

# ---------- 并查集（带按秩合并 + 路径压缩） ----------
parent = list(range(n + 1))
size = [1] * (n + 1)


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(a, b):
    pa = find(a)
    pb = find(b)
    if pa == pb:
        return
    if size[pa] < size[pb]:
        pa, pb = pb, pa
    parent[pb] = pa
    size[pa] += size[pb]


# ---------- 补图 BFS（集合运算优化） ----------
unvisited = set(range(1, n + 1))

while unvisited:
    start = unvisited.pop()
    stack = [start]

    while stack:
        u = stack.pop()
        forbid_u = forbidden[u]

        if len(forbid_u) < len(unvisited):
            # forbidden 边少 → 大多数节点可连接，只计算"保留"的
            keep = forbid_u & unvisited
            to_visit = unvisited - keep
            unvisited = keep
        else:
            # forbidden 边多 → 遍历 unvisited 找可连接的
            to_visit = {v for v in unvisited if v not in forbid_u}
            unvisited -= to_visit

        for v in to_visit:
            union(u, v)
            stack.append(v)

# ---------- Kruskal（提前终止） ----------
edges.sort()

ans = 0
used = 0
target = n - 1

for w, u, v in edges:
    if find(u) != find(v):
        union(u, v)
        ans += w
        used += 1
        if used == target:
            break

write(str(ans) + '\n')
