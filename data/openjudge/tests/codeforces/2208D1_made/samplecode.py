#!/usr/bin/env python3
"""Codeforces 2208D1 Tree Orientation (Easy Version) -- reference solution.

Written for this repository as a hand-off artifact; no external license.

In an oriented tree the edge u->v is the only u..v path, so the edges are exactly
the cover pairs of the reachability relation: u reaches v (u != v) and no third
vertex w has u ->* w ->* v.  With bitsets: popcount(row[u] & col[v]) == 2.
If there are exactly n-1 covers, they form a tree, and the tree's reachability
(recomputed bottom-up) equals the matrix, the answer is that tree; otherwise No.
"""
import sys


def solve(n, rows):
    R = [int(s[::-1], 2) for s in rows]          # bit j of R[i]: i reaches j
    C = [0] * n                                    # bit i of C[j]: i reaches j
    for i, s in enumerate(rows):
        bit = 1 << i
        j = s.find("1")
        while j >= 0:
            C[j] |= bit
            j = s.find("1", j + 1)
    edges = []
    for u in range(n):
        ru = R[u]
        if not (ru >> u) & 1:
            return None
        rest = ru & ~(1 << u)
        while rest:
            low = rest & -rest
            v = low.bit_length() - 1
            rest ^= low
            if (ru & C[v]).bit_count() == 2:
                edges.append((u, v))
                if len(edges) > n - 1:
                    return None
    if len(edges) != n - 1:
        return None
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    children = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        a, b = find(u), find(v)
        if a == b:
            return None
        parent[a] = b
        children[u].append(v)
        indeg[v] += 1
    order = [v for v in range(n) if indeg[v] == 0]
    for x in order:
        for y in children[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                order.append(y)
    reach = [0] * n
    for x in reversed(order):
        acc = 1 << x
        for y in children[x]:
            acc |= reach[y]
        reach[x] = acc
    if reach != R:
        return None
    return edges


def main():
    data = sys.stdin.read().split()
    t = int(data[0]); p = 1
    out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        rows = data[p:p + n]; p += n
        edges = solve(n, rows)
        if edges is None:
            out.append("No")
        else:
            out.append("Yes")
            out.extend(f"{u + 1} {v + 1}" for u, v in edges)
    sys.stdout.write("\n".join(out) + "\n")


main()
