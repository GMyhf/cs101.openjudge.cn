#!/usr/bin/env python3
"""Codeforces 894E Ralph and Mushrooms -- generator, input contract and data build.

Statement: n m (1 <= n <= 1e6, 0 <= m <= 1e6); m lines x y w (1 <= x, y <= n, 0 <= w <= 1e8),
self loops and parallel edges allowed; last line s (1 <= s <= n).  Output: the maximum number of
mushrooms, a unique integer (token-exact comparison is fine).

Case 0 is official sample 1 (-> 16); seed 1 is official sample 2 (-> 8); both are asserted.

Shapes, by how solutions go wrong:
  * n = 1, m = 0 (answer 0);  n = 1 with one self loop of 1e8 (self loops form a cycle);
  * tiny graphs with self loops / parallel edges / w = 0 edges that must be walked through;
  * heavy parts not reachable from s (edges pointing *into* s) -- kills "best start anywhere";
  * a light cycle vs. heavy DAG edges and branching DAGs -- kills greedy walks;
  * w on triangular-number boundaries k(k-1)/2 - 1, k(k-1)/2, +1 up to 1e8 -- off-by-one in the
    number of productive passes;
  * big SCCs with w = 1e8 on every edge (answer ~1e17) -- kills 32-bit sums;
  * n = 1e6 with a long path / long cycle (deep DFS), many small SCCs in a DAG, random graphs.
m is kept <= 115000 so every .in stays under 3 MB (the statement allows 1e6).

Oracles (independent of Tarjan / the closed-form pass total):
  * state_oracle (tiny graphs): exhaustive search over the states (vertex, passes made on each
    edge, capped once the edge is exhausted); the collected amount is a function of the pass
    counts, so the answer is the max over all reachable states.  Mushrooms are simulated pass by
    pass.  Needs m <= 6 and small w.
  * matrix_oracle (n <= 400, m <= 3000): reachability by BFS from every vertex, u ~ v iff each
    reaches the other; an edge inside a class is worth its pass-by-pass simulated total; longest
    path over classes by repeated relaxation (Bellman-Ford style) from the class of s.
"""
from __future__ import annotations

import random
import subprocess
import sys
from collections import deque
from pathlib import Path

REFERENCE = Path(__file__).with_name("samplecode.py")
SAMPLE = "2 2\n1 2 4\n2 1 4\n1\n"
SAMPLE_OUT = "16\n"
SAMPLE2 = "3 3\n1 2 4\n2 3 3\n1 3 8\n1\n"
SAMPLE2_OUT = "8\n"
MAX_N = MAX_M = 1_000_000
MAX_W = 100_000_000
MAX_BYTES = 3_000_000
BIG_M = 115_000


def fmt(n, edges, s):
    return f"{n} {len(edges)}\n" + "".join(f"{x} {y} {w}\n" for x, y, w in edges) + f"{s}\n"


def relabel(r, n, edges, s, keep=None):
    """Random vertex relabelling (keep: dict of fixed old->new labels), shuffled edge order."""
    labels = list(range(1, n + 1))
    r.shuffle(labels)
    if keep:
        for old, new in keep.items():
            j = labels.index(new)
            labels[j], labels[old - 1] = labels[old - 1], labels[j]
    edges = [(labels[x - 1], labels[y - 1], w) for x, y, w in edges]
    r.shuffle(edges)
    return fmt(n, edges, labels[s - 1])


def tri_ws(r, count):
    out = []
    for _ in range(count):
        k = r.randint(2, 14142)
        t = k * (k - 1) // 2
        out.append(max(0, min(MAX_W, t + r.choice((-1, 0, 1)))))
    return out


def generate(seed):
    r = random.Random(894_005 + seed * 15485863)
    if seed == 1:
        return SAMPLE2
    if seed == 2:                                   # n = 1, no edges
        return "1 0\n1\n"
    if seed == 3:                                   # n = 1, one self loop with w = 1e8
        return f"1 1\n1 1 {MAX_W}\n1\n"
    if seed == 4:                                   # tiny: self loops + parallel edges
        return fmt(3, [(1, 1, 6), (1, 2, 3), (1, 2, 5), (2, 2, 0), (2, 3, 7), (3, 3, 2)], 1)
    if seed == 5:                                   # tiny: heavy cycle upstream of s (unreachable)
        return fmt(4, [(1, 2, 20), (2, 1, 20), (2, 3, 1), (3, 4, 2), (4, 3, 0)], 3)
    if seed == 6:                                   # tiny: light cycle vs one heavy DAG edge
        return fmt(4, [(1, 2, 3), (2, 1, 3), (1, 3, 10), (2, 4, 7), (3, 4, 1)], 1)
    if seed == 7:                                   # tiny: w = 0 cycle edges gate a heavy loop
        return fmt(4, [(1, 2, 0), (2, 1, 0), (2, 3, 0), (3, 3, 9), (1, 4, 12)], 1)
    if seed == 8:                                   # tiny: greedy (largest out edge) trap
        return fmt(5, [(1, 2, 9), (2, 3, 0), (1, 4, 2), (4, 5, 8), (5, 4, 1)], 1)
    if seed == 9:                                   # tiny random, triangular boundaries 0..15
        n = 4
        edges = [(r.randint(1, n), r.randint(1, n), r.choice((0, 1, 2, 3, 5, 6, 7, 9, 10, 11)))
                 for _ in range(6)]
        return fmt(n, edges, r.randint(1, n))
    if seed == 10:                                  # medium random graph, big w
        n, m = 300, 1200
        edges = [(r.randint(1, n), r.randint(1, n), r.randint(0, MAX_W)) for _ in range(m)]
        return fmt(n, edges, r.randint(1, n))
    if seed == 11:                                  # medium: DAG of small SCCs, choose best branch
        n, edges = 400, []
        groups = [list(range(i, min(n, i + r.randint(1, 5)) + 1)) for i in range(1, n + 1, 6)]
        for g in groups:
            if len(g) > 1:
                for a, b in zip(g, g[1:] + g[:1]):
                    edges.append((a, b, r.randint(0, 1000)))
        for i, g in enumerate(groups):
            for _ in range(3):
                j = r.randint(i + 1, min(len(groups) - 1, i + 8)) if i + 1 < len(groups) else None
                if j is not None:
                    edges.append((r.choice(g), r.choice(groups[j]), r.randint(0, MAX_W)))
        return relabel(r, n, edges, 1)
    if seed == 12:                                  # medium: s is a sink, graph elsewhere heavy
        n, m = 200, 2500
        edges = [(r.randint(2, n), r.randint(1, n), r.randint(MAX_W // 2, MAX_W)) for _ in range(m)]
        return relabel(r, n, edges, 1)
    if seed == 13:                                  # medium SCC, triangular-boundary weights
        n, m = 150, 2000
        ws = tri_ws(r, m - n)
        edges = [(i, i % n + 1, MAX_W - r.randint(0, 3)) for i in range(1, n + 1)]
        edges += [(r.randint(1, n), r.randint(1, n), w) for w in ws]
        return relabel(r, n, edges, r.randint(1, n))
    if seed == 14:                                  # overflow: one SCC, every w = 1e8
        n, m = 1000, BIG_M
        edges = [(i, i % n + 1, MAX_W) for i in range(1, n + 1)]
        edges += [(r.randint(1, n), r.randint(1, n), MAX_W) for _ in range(m - n)]
        return relabel(r, n, edges, r.randint(1, n))
    if seed == 15:                                  # n = 1e6, long simple path (deep DFS)
        n, m = MAX_N, BIG_M
        path = r.sample(range(1, n + 1), m + 1)
        edges = [(path[i], path[i + 1], r.randint(0, MAX_W)) for i in range(m)]
        r.shuffle(edges)
        return fmt(n, edges, path[0])
    if seed == 16:                                  # long cycle plus a heavy tail out of it
        n = MAX_N
        cyc = r.sample(range(1, n + 1), 100000)
        edges = [(cyc[i], cyc[(i + 1) % len(cyc)], r.randint(0, 10)) for i in range(len(cyc))]
        on_cycle = set(cyc)
        rest = [v for v in r.sample(range(1, n + 1), 20000) if v not in on_cycle]
        prev = cyc[r.randrange(len(cyc))]
        for v in rest[:14000]:
            edges.append((prev, v, MAX_W)); prev = v
        r.shuffle(edges)
        return fmt(n, edges, cyc[0])
    if seed == 17:                                  # random sparse graph, many SCCs
        n, m = 50000, BIG_M
        edges = [(r.randint(1, n), r.randint(1, n), r.randint(0, MAX_W)) for _ in range(m)]
        return fmt(n, edges, r.randint(1, n))
    if seed == 18:                                  # layered DAG with small SCCs, s mid-way
        n, layers, width = 60000, 600, 100
        edges, node = [], lambda L, i: L * width + i + 1
        for L in range(layers):
            for i in range(0, width, 2):            # 2-cycles inside the layer
                w = r.randint(0, 5000)
                edges.append((node(L, i), node(L, i + 1), w)); edges.append((node(L, i + 1), node(L, i), w))
            if L + 1 < layers:
                for _ in range(90):
                    edges.append((node(L, r.randrange(width)), node(L + 1, r.randrange(width)),
                                  r.randint(0, MAX_W)))
        return relabel(r, n, edges, node(layers // 3, 0))
    if seed == 19:                                  # n = 1e6, edges among a random 40000 subset
        n = MAX_N
        pool = r.sample(range(1, n + 1), 40000)
        edges = [(r.choice(pool), r.choice(pool), r.randint(0, MAX_W)) for _ in range(BIG_M)]
        return fmt(n, edges, r.choice(pool))
    # seed 20: parallel edges and self loops on a few vertices, all w = 1e8 / boundaries
    n = 5
    edges = []
    for _ in range(BIG_M):
        x = r.randint(1, n)
        y = x if r.random() < 0.5 else r.randint(1, n)
        edges.append((x, y, MAX_W if r.random() < 0.7 else tri_ws(r, 1)[0]))
    return fmt(n, edges, r.randint(1, n))


def valid(text):
    if not text.endswith("\n"):
        return False
    rows = text[:-1].split("\n")
    try:
        head = rows[0].split()
        if len(head) != 2 or rows[0] != " ".join(head):
            return False
        n, m = map(int, head)
        if not (1 <= n <= MAX_N and 0 <= m <= MAX_M) or len(rows) != m + 2:
            return False
        for row in rows[1:1 + m]:
            parts = row.split()
            if len(parts) != 3 or row != " ".join(parts):
                return False
            x, y, w = map(int, parts)
            if not (1 <= x <= n and 1 <= y <= n and 0 <= w <= MAX_W):
                return False
        last = rows[-1]
        return last.strip() == last and 1 <= int(last) <= n
    except ValueError:
        return False


def parse(text):
    t = list(map(int, text.split()))
    n, m = t[0], t[1]
    edges = [(t[2 + 3 * i], t[3 + 3 * i], t[4 + 3 * i]) for i in range(m)]
    return n, edges, t[2 + 3 * m]


def passes(w):
    """Amounts collected on successive passes, simulated literally."""
    got, cur, i = [], w, 1
    while cur >= 0:
        got.append(cur)
        cur -= i
        i += 1
    return got


def state_oracle(text):
    n, edges, s = parse(text)
    seqs = [passes(w) for _, _, w in edges]
    caps = [len(q) for q in seqs]
    start = (s,) + (0,) * len(edges)
    seen = {start}
    q = deque([start])
    best = 0
    while q:
        st = q.popleft()
        v, cnt = st[0], st[1:]
        best = max(best, sum(sum(seqs[i][:cnt[i]]) for i in range(len(edges))))
        for i, (x, y, _) in enumerate(edges):
            if x == v:
                c = list(cnt)
                c[i] = min(caps[i], c[i] + 1)
                nxt = (y,) + tuple(c)
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
    return f"{best}\n"


def matrix_oracle(text):
    n, edges, s = parse(text)
    adj = [[] for _ in range(n + 1)]
    for x, y, _ in edges:
        adj[x].append(y)
    reach = []
    for src in range(n + 1):
        seen = bytearray(n + 1)
        if src:
            seen[src] = 1
            q = [src]
            for v in q:
                for u in adj[v]:
                    if not seen[u]:
                        seen[u] = 1
                        q.append(u)
        reach.append(seen)
    cls = [0] * (n + 1)
    for v in range(1, n + 1):
        cls[v] = min(u for u in range(1, n + 1) if reach[v][u] and reach[u][v])
    inner = [0] * (n + 1)
    cross = []
    for x, y, w in edges:
        if cls[x] == cls[y]:
            inner[cls[x]] += sum(passes(w))
        else:
            cross.append((cls[x], cls[y], w))
    NEG = -1
    best = [NEG] * (n + 1)
    best[cls[s]] = inner[cls[s]]
    for _ in range(n + 1):
        changed = False
        for a, b, w in cross:
            if best[a] != NEG and best[a] + w + inner[b] > best[b]:
                best[b] = best[a] + w + inner[b]
                changed = True
        if not changed:
            break
    return f"{max(best)}\n"


def build():
    out = Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    for path in out.glob("*"):
        path.unlink()
    cases = [SAMPLE] + [generate(seed) for seed in range(1, 40)]
    if len(set(cases)) != len(cases):
        raise SystemExit("duplicate inputs")
    checked = {"state": 0, "matrix": 0, "any": 0}
    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {index} violates the input contract")
        if len(case.encode()) > MAX_BYTES:
            raise SystemExit(f"case {index} is too large")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, check=True, timeout=60).stdout
        if index == 0 and answer.split() != SAMPLE_OUT.split():
            raise SystemExit(f"sample 1 mismatch: {answer!r}")
        if index == 1 and answer.split() != SAMPLE2_OUT.split():
            raise SystemExit(f"sample 2 mismatch: {answer!r}")
        n, edges, _ = parse(case)
        used = False
        if len(edges) <= 6 and all(w <= 30 for _, _, w in edges):
            if state_oracle(case).split() != answer.split():
                raise SystemExit(f"state oracle disagreement on case {index}")
            checked["state"] += 1; used = True
        if n <= 400 and len(edges) <= 3000:
            if matrix_oracle(case).split() != answer.split():
                raise SystemExit(f"matrix oracle disagreement on case {index}")
            checked["matrix"] += 1; used = True
        checked["any"] += used
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")
    print(f"built {len(cases)} cases, oracle-checked {checked}")


if __name__ == "__main__":
    build()
