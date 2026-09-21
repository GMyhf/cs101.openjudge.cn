#!/usr/bin/env python3
"""Codeforces 1000E We Need More Bosses -- generator, input contract and data build.

Statement: connected simple undirected graph, 2 <= n <= 3e5, n-1 <= m <= 3e5, no self loops,
no repeated pairs.  Output the maximum over (s, t) of the number of edges that every s-t path
must use -- a unique integer, so token-exact comparison is fine.

Case 0 is official sample 1 (-> 2); seed 1 is official sample 2 (-> 3); both are asserted.

Graphs are built from "blobs" (2-edge-connected pieces: a single vertex, or a cycle with
random chords) joined by bridges arranged in a chosen blob-tree, then relabelled at random and
edge order / orientation shuffled.  Shapes, by how solutions go wrong:
  * minimum n = 2, one bridge;  whole graph one cycle / complete graph (answer 0);
  * star of bridges (many bridges, answer 2) -- kills "count all bridges";
  * vertex 1 in the middle of a long bridge path / spider -- kills "eccentricity from vertex 1"
    instead of a real diameter (double BFS);
  * mixed cactus / caterpillar / random blob trees, random tree + extra edges;
  * deep structures with n = 2e5 (path, big cycle) -- kill recursive DFS;
  * large mixed graphs with m ~ 2.2e5.
File size keeps n, m <= 220000 so every .in stays under 3 MB (the statement allows 3e5).

Oracle (independent brute force, used when n <= ORACLE_N): for every edge, delete it and label
connected components by BFS; for every pair (s, t) count the edges whose deletion separates s
from t; answer = the maximum.  No bridge / low-link / tree-diameter logic involved.
"""
from __future__ import annotations

import random
import subprocess
import sys
from collections import deque
from pathlib import Path

REFERENCE = Path(__file__).with_name("samplecode.py")
SAMPLE = "5 5\n1 2\n2 3\n3 1\n4 1\n5 2\n"
SAMPLE_OUT = "2\n"
SAMPLE2 = "4 3\n1 2\n4 3\n3 2\n"
SAMPLE2_OUT = "3\n"
MAX_N = MAX_M = 300_000
ORACLE_N = 90
MAX_BYTES = 3_000_000


def _blob_edges(r, nodes, chords):
    k = len(nodes)
    if k == 1:
        return []
    assert k >= 3
    edges = {(min(nodes[i], nodes[(i + 1) % k]), max(nodes[i], nodes[(i + 1) % k])) for i in range(k)}
    limit = k * (k - 1) // 2
    target = min(limit, len(edges) + chords)
    while len(edges) < target:
        a, b = r.sample(nodes, 2)
        edges.add((min(a, b), max(a, b)))
    return list(edges)


def assemble(r, sizes, parents, chord_fn=lambda k: 0, fixed_one=None):
    """sizes[i] = blob size (1 or >= 3); parents[i] < i is the blob-tree parent (parents[0] unused).
    fixed_one = blob index whose first vertex becomes label 1 (otherwise random labels)."""
    n = sum(sizes)
    blobs, start = [], 0
    for s in sizes:
        blobs.append(list(range(start, start + s)))
        start += s
    edges = []
    for b in blobs:
        edges += _blob_edges(r, b, chord_fn(len(b)))
    for i in range(1, len(sizes)):
        edges.append((r.choice(blobs[parents[i]]), r.choice(blobs[i])))
    labels = list(range(1, n + 1))
    r.shuffle(labels)
    if fixed_one is not None:
        v = blobs[fixed_one][0]
        j = labels.index(1)
        labels[j], labels[v] = labels[v], labels[j]
    r.shuffle(edges)
    lines = []
    for a, b in edges:
        a, b = labels[a], labels[b]
        if r.random() < 0.5:
            a, b = b, a
        lines.append(f"{a} {b}\n")
    return f"{n} {len(edges)}\n" + "".join(lines)


def rand_size(r, lo_cycle, hi_cycle, p_single):
    return 1 if r.random() < p_single else r.randint(lo_cycle, hi_cycle)


def generate(seed):
    r = random.Random(1000_005 + seed * 104729)
    if seed == 1:
        return SAMPLE2
    if seed == 2:                                       # minimum: n = 2, one bridge
        return "2 1\n2 1\n"
    if seed == 3:                                       # single cycle -> 0
        return assemble(r, [7], [0])
    if seed == 4:                                       # complete graph K8 -> 0
        return assemble(r, [8], [0], chord_fn=lambda k: 100)
    if seed == 5:                                       # star of bridges -> 2
        return assemble(r, [1] * 9, [0] * 9)
    if seed == 6:                                       # small cactus, random blob tree
        sizes = [rand_size(r, 3, 5, 0.4) for _ in range(14)]
        return assemble(r, sizes, [0] + [r.randrange(i) for i in range(1, 14)], lambda k: r.randint(0, 1))
    if seed == 7:                                       # small random tree + few extra edges
        n = 30
        par = [0] + [r.randrange(i) for i in range(1, n)]
        text = assemble(r, [1] * n, par)
        return _add_edges(r, text, 6)
    if seed == 8:                                       # vertex 1 in the middle of a bridge path
        k = 21
        sizes = [rand_size(r, 3, 4, 0.5) for _ in range(k)]
        return assemble(r, sizes, [0] + list(range(k - 1)), lambda k: 1, fixed_one=k // 2)
    if seed == 9:                                       # spider: 3 legs, vertex 1 inside a leg
        sizes, par = [3], [0]
        for leg in range(3):
            prev = 0
            for _ in range(r.randint(5, 9)):
                sizes.append(rand_size(r, 3, 3, 0.5)); par.append(prev); prev = len(sizes) - 1
        return assemble(r, sizes, par, fixed_one=4)
    if seed == 10:                                      # random tree, n = 80 (all bridges)
        n = 80
        return assemble(r, [1] * n, [0] + [r.randrange(max(0, i - 3), i) for i in range(1, n)])
    if seed == 11:                                      # dense blobs with pendant bridge paths
        sizes = [12, 1, 1, 1, 6, 1, 1, 10, 1, 1, 1, 1, 5]
        par = [0, 0, 1, 2, 3, 4, 5, 0, 7, 8, 0, 10, 11]
        return assemble(r, sizes, par, lambda k: 3 * k, fixed_one=0)
    if seed == 12:                                      # deep path, n = 200000
        n = 200000
        return assemble(r, [1] * n, [0] + list(range(n - 1)))
    if seed == 13:                                      # one huge cycle -> 0
        return assemble(r, [200000], [0])
    if seed == 14:                                      # long chain of triangles/singletons
        sizes = [rand_size(r, 3, 3, 0.3) for _ in range(70000)]
        return assemble(r, sizes, [0] + list(range(len(sizes) - 1)))
    if seed == 15:                                      # random tree with a long spine
        n = 200000
        par = [0] + [(i - 1 if i < 3000 else r.randrange(i)) for i in range(1, n)]
        return assemble(r, [1] * n, par)
    if seed == 16:                                      # big spider, vertex 1 mid-leg
        sizes, par = [50], [0]
        for leg in range(6):
            prev = 0
            for _ in range(r.randint(8000, 12000)):
                sizes.append(rand_size(r, 3, 5, 0.6)); par.append(prev); prev = len(sizes) - 1
        return assemble(r, sizes, par, lambda k: k // 2, fixed_one=5000)
    if seed == 17:                                      # huge star -> 2
        n = 200000
        return assemble(r, [1] * n, [0] * n)
    if seed == 18:                                      # random tree + many extra edges
        n = 150000
        text = assemble(r, [1] * n, [0] + [r.randrange(i) for i in range(1, n)])
        return _add_edges(r, text, 60000)
    if seed == 19:                                      # caterpillar of cycles with leaves
        sizes, par, spine = [4], [0], 0
        while len(sizes) < 60000:
            sizes.append(rand_size(r, 3, 6, 0.3)); par.append(spine); spine = len(sizes) - 1
            for _ in range(r.randint(0, 2)):
                sizes.append(1); par.append(spine)
        return assemble(r, sizes, par, lambda k: r.randint(0, 2))
    # seed 20: dense blobs in a random blob tree, m ~ 2.2e5
    sizes = [r.randint(3, 60) if r.random() < 0.3 else 1 for _ in range(7000)]
    par = [0] + [r.randrange(max(0, i - 20), i) for i in range(1, len(sizes))]
    return assemble(r, sizes, par, lambda k: 2 * k)


def _add_edges(r, text, extra):
    rows = text.split("\n")
    n, m = map(int, rows[0].split())
    have = {tuple(sorted(map(int, row.split()))) for row in rows[1:1 + m]}
    lines = rows[1:1 + m]
    target = min(n * (n - 1) // 2, m + extra)
    while len(have) < target:
        a, b = r.sample(range(1, n + 1), 2)
        key = (min(a, b), max(a, b))
        if key not in have:
            have.add(key); lines.append(f"{a} {b}")
    r.shuffle(lines)
    return f"{n} {len(lines)}\n" + "".join(line + "\n" for line in lines)


def valid(text):
    if not text.endswith("\n"):
        return False
    rows = text[:-1].split("\n")
    try:
        head = rows[0].split()
        if len(head) != 2:
            return False
        n, m = map(int, head)
        if not (2 <= n <= MAX_N and n - 1 <= m <= MAX_M) or len(rows) != m + 1:
            return False
        parent = list(range(n + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        seen, comps = set(), n
        for row in rows[1:]:
            parts = row.split()
            if len(parts) != 2 or row != f"{parts[0]} {parts[1]}":
                return False
            x, y = int(parts[0]), int(parts[1])
            if not (1 <= x <= n and 1 <= y <= n and x != y):
                return False
            key = (min(x, y), max(x, y))
            if key in seen:
                return False
            seen.add(key)
            a, b = find(x), find(y)
            if a != b:
                parent[a] = b; comps -= 1
        return comps == 1
    except ValueError:
        return False


def oracle(text):
    t = list(map(int, text.split()))
    n, m = t[0], t[1]
    edges = [(t[2 + 2 * i], t[3 + 2 * i]) for i in range(m)]
    sep = [[0] * (n + 1) for _ in range(n + 1)]
    for skip in range(m):
        adj = [[] for _ in range(n + 1)]
        for i, (x, y) in enumerate(edges):
            if i != skip:
                adj[x].append(y); adj[y].append(x)
        lab = [0] * (n + 1)
        c = 0
        for s in range(1, n + 1):
            if lab[s]:
                continue
            c += 1; lab[s] = c; q = deque([s])
            while q:
                v = q.popleft()
                for u in adj[v]:
                    if not lab[u]:
                        lab[u] = c; q.append(u)
        if c == 1:
            continue
        for s in range(1, n + 1):
            row, ls = sep[s], lab[s]
            for u in range(1, n + 1):
                if lab[u] != ls:
                    row[u] += 1
    return f"{max(max(row) for row in sep)}\n"


def build():
    out = Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    for path in out.glob("*"):
        path.unlink()
    cases = [SAMPLE] + [generate(seed) for seed in range(1, 40)]
    if len(set(cases)) != len(cases):
        raise SystemExit("duplicate inputs")
    checked = 0
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
        if int(case.split()[0]) <= ORACLE_N:
            if oracle(case).split() != answer.split():
                raise SystemExit(f"oracle disagreement on case {index}")
            checked += 1
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")
    print(f"built {len(cases)} cases, {checked} oracle-checked")


if __name__ == "__main__":
    build()
