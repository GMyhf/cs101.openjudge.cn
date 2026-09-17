# Codeforces 2192D Cost of Tree -- reference solution.
# Written for this repository as a hand-off artifact for building judge data; no external license.
#
# Moving subtree u under v changes the cost by S_u * (dep(v) + 1 - dep(u)), so v is the deepest
# node outside subtree(u).  Inside subtree(r), for u in the subtree of child c of r, the deepest
# node outside is max(deepest outside u within subtree(c), X_c) where X_c is the deepest node of
# r's other children (or r itself).  S_u and dep-difference both shrink going down, so against
# X_c the best u is c itself.  Hence gain(r) = max_c max(gain(c), S_c * X_c) with X_c measured
# relative to r (0 if no other child), answer(r) = base(r) + gain(r).
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); p = 1; out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        a = [0] + [int(x) for x in data[p:p + n]]; p += n
        adj = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u = int(data[p]); v = int(data[p + 1]); p += 2
            adj[u].append(v); adj[v].append(u)
        parent = [0] * (n + 1); order = [1]; parent[1] = -1
        for u in order:
            for v in adj[u]:
                if v != parent[u]:
                    parent[v] = u; order.append(v)
        S = a[:]; base = [0] * (n + 1); h = [0] * (n + 1); gain = [0] * (n + 1)
        for u in reversed(order):
            kids = [v for v in adj[u] if v != parent[u]]
            if not kids:
                continue
            best1 = best2 = 0; arg = -1
            s = 0; b = 0
            for c in kids:
                s += S[c]; b += base[c] + S[c]
                hv = h[c] + 1
                if hv > best1:
                    best2 = best1; best1 = hv; arg = c
                elif hv > best2:
                    best2 = hv
            S[u] += s; base[u] = b; h[u] = best1
            g = 0
            for c in kids:
                x = best2 if c == arg else best1
                val = S[c] * x
                if val > g: g = val
                if gain[c] > g: g = gain[c]
            gain[u] = g
        out.append(" ".join(str(base[i] + gain[i]) for i in range(1, n + 1)))
    sys.stdout.write("\n".join(out) + "\n")


main()
