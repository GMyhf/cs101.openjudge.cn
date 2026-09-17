#!/usr/bin/env python3
# Reference solution for Codeforces 2167F "Tree, TREE!!!".
# Written for this repository as a hand-off artifact for judge-data generation;
# no external source, no external license.
#
# With root r, node v is the LCA of some k-set iff subtree_r(v) has >= k nodes
# (take v itself plus k-1 other nodes of its subtree).  For r = v the subtree is the
# whole tree (always counts: n per test).  For r on the side of neighbour u, the
# subtree of v is everything except u's side.  So every edge splitting the tree into
# parts of sizes a and b contributes a*[b >= k] + b*[a >= k].
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); p = 1
    out = []
    for _ in range(t):
        n, k = int(data[p]), int(data[p + 1]); p += 2
        adj = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = int(data[p]), int(data[p + 1]); p += 2
            adj[u].append(v); adj[v].append(u)
        parent = [0] * (n + 1)
        order = [1]
        parent[1] = -1
        for x in order:
            for y in adj[x]:
                if y != parent[x]:
                    parent[y] = x
                    order.append(y)
        size = [1] * (n + 1)
        total = n
        for x in reversed(order):
            if x != 1:
                size[parent[x]] += size[x]
                a = size[x]; b = n - a
                if b >= k:
                    total += a
                if a >= k:
                    total += b
        out.append(str(total))
    sys.stdout.write("\n".join(out) + "\n")


main()
