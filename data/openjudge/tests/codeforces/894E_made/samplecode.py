# Codeforces 894E Ralph and Mushrooms -- reference solution.
# Written for this repo as a hand-off artifact (test-data reference); no external license.
#
# An edge with w mushrooms yields w, w-1, w-3, ... ; pass j gives w - j(j-1)/2 while >= 0, so
# with k = largest k having k(k-1)/2 <= w, the whole edge is worth k*w - (k-1)k(k+1)/6.
# Inside a strongly connected component every edge can be exhausted.  Condense the part
# reachable from s (iterative Tarjan), then longest path over the condensation DAG where a
# component is worth the sum of its exhausted internal edges and a cross edge is worth w.
import sys
from math import isqrt


def total(w):
    k = (1 + isqrt(1 + 8 * w)) // 2
    return k * w - (k - 1) * k * (k + 1) // 6


def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    X = list(map(int, data[2:2 + 3 * m:3]))
    Y = list(map(int, data[3:3 + 3 * m:3]))
    W = list(map(int, data[4:4 + 3 * m:3]))
    s = int(data[2 + 3 * m])
    adj = {}
    for i in range(m):
        x = X[i]
        if x in adj:
            adj[x].append(i)
        else:
            adj[x] = [i]
    empty = []
    # iterative Tarjan from s
    index = {}
    low = {}
    comp = {}
    onstack = set()
    st = []
    counter = 0
    ncomp = 0
    index[s] = low[s] = 0
    counter = 1
    st.append(s); onstack.add(s)
    call = [(s, iter(adj.get(s, empty)))]
    while call:
        v, it = call[-1]
        advanced = False
        for e in it:
            u = Y[e]
            if u not in index:
                index[u] = low[u] = counter
                counter += 1
                st.append(u); onstack.add(u)
                call.append((u, iter(adj.get(u, empty))))
                advanced = True
                break
            elif u in onstack:
                if index[u] < low[v]:
                    low[v] = index[u]
        if advanced:
            continue
        call.pop()
        if call:
            p = call[-1][0]
            if low[v] < low[p]:
                low[p] = low[v]
        if low[v] == index[v]:
            while True:
                u = st.pop()
                onstack.discard(u)
                comp[u] = ncomp
                if u == v:
                    break
            ncomp += 1
    # Tarjan emits components in reverse topological order: comp ids of successors are smaller.
    inner = [0] * ncomp
    out = [[] for _ in range(ncomp)]
    for i in range(m):
        cx = comp.get(X[i])
        if cx is None:
            continue
        cy = comp[Y[i]]
        if cx == cy:
            inner[cx] += total(W[i])
        else:
            out[cx].append((cy, W[i]))
    best = [0] * ncomp
    for c in range(ncomp):
        b = 0
        for cy, w in out[c]:
            v = best[cy] + w
            if v > b:
                b = v
        best[c] = b + inner[c]
    print(best[comp[s]])


main()
