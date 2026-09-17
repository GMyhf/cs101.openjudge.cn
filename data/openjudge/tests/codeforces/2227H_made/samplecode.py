#!/usr/bin/env python3
# Codeforces 2227H Fallen Leaves -- reference solution.
# Written for this repository as a hand-off artifact for building judge data; no external license.
#
# With k leaves, a minimum-cost perfect matching on a tree costs sum over edges of
# (leaves on one side) mod 2.  Root at a non-leaf r; s[v] = leaves in subtree(v).
# k even: answer = sum_{v != r} s[v] & 1.
# k odd: one leaf l stays unchosen; removing it flips the parity of every edge on the
# path l..r, so answer = base + min_l sum_{edges on path} (+1 if s even else -1).
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); p = 1; out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        adj = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u = int(data[p]); v = int(data[p + 1]); p += 2
            adj[u].append(v); adj[v].append(u)
        root = next(v for v in range(1, n + 1) if len(adj[v]) > 1)
        parent = [0] * (n + 1); parent[root] = -1
        order = [root]
        for v in order:
            for w in adj[v]:
                if w != parent[v]:
                    parent[w] = v; order.append(w)
        s = [0] * (n + 1)
        for v in reversed(order):
            if len(adj[v]) == 1:
                s[v] += 1
            if v != root:
                s[parent[v]] += s[v]
        k = s[root]
        base = 0
        w = [0] * (n + 1)
        for v in order:
            if v == root:
                continue
            if s[v] & 1:
                base += 1; w[v] = w[parent[v]] - 1
            else:
                w[v] = w[parent[v]] + 1
        if k & 1:
            base += min(w[v] for v in range(1, n + 1) if len(adj[v]) == 1)
        out.append(base)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
