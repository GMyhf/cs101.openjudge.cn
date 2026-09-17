# Codeforces 1000E We Need More Bosses -- reference solution.
# Written for this repo as a hand-off artifact (test-data reference); no external license.
#
# Bosses on an s-t route are exactly the bridges every s-t path must cross.  Contract every
# 2-edge-connected component to a vertex; the bridges form a tree, and the answer is the
# diameter (in edges) of that bridge tree.
# Bridges without recursion: a stack DFS ("visit on pop, parent = vertex that pushed it")
# yields a genuine DFS tree; low-links are then folded up in reverse preorder, and the tree
# edge (parent[v], v) is a bridge iff low[v] == tin[v].
import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    xs = data[2:2 + 2 * m:2]
    ys = data[3:3 + 2 * m:2]
    for i in range(m):
        x = int(xs[i]); y = int(ys[i])
        adj[x].append(y); adj[y].append(x)
    tin = [0] * (n + 1)
    parent = [0] * (n + 1)
    order = []
    stack = [(1, 0)]
    timer = 0
    while stack:
        v, p = stack.pop()
        if tin[v]:
            continue
        timer += 1
        tin[v] = timer
        parent[v] = p
        order.append(v)
        for u in adj[v]:
            if not tin[u]:
                stack.append((u, v))
    low = tin[:]
    # simple graph: the edge to the parent is the only edge between v and parent[v]
    for v in reversed(order):
        lv = low[v]
        p = parent[v]
        tv = tin[v]
        for u in adj[v]:
            if u != p:
                tu = tin[u]
                if tu < tv:                 # back edge to an ancestor
                    if tu < lv:
                        lv = tu
                elif parent[u] == v:        # tree child (already folded)
                    if low[u] < lv:
                        lv = low[u]
        low[v] = lv
    # component id: bridges are tree edges (parent[v], v) with low[v] == tin[v];
    # in preorder a vertex joins its parent's component unless its parent edge is a bridge
    comp = [0] * (n + 1)
    c = 0
    for v in order:
        if parent[v] == 0 or low[v] == tin[v]:
            comp[v] = c; c += 1
        else:
            comp[v] = comp[parent[v]]
    tree = [[] for _ in range(c)]
    for v in order:
        p = parent[v]
        if p and low[v] == tin[v]:
            a = comp[v]; b = comp[p]
            tree[a].append(b); tree[b].append(a)

    def far(src):
        dist = [-1] * c
        dist[src] = 0
        q = [src]
        for v in q:
            dv = dist[v] + 1
            for u in tree[v]:
                if dist[u] < 0:
                    dist[u] = dv
                    q.append(u)
        return q[-1], dist[q[-1]]

    a, _ = far(0)
    print(far(a)[1])


main()
