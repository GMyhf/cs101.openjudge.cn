#!/usr/bin/env python3
"""2167F Tree, TREE!!! -- generator, input contract, oracles and data build.

Statement: t test cases (1 <= t <= 1e4); each has n, k (2 <= k <= n <= 2e5) and n-1 edges
forming a tree; sum of n <= 2e5.  Output sum over roots r of |S_r|, where S_r is the set
of LCAs (rooted at r) of all k-subsets.

Shapes are chosen around how solutions go wrong:
  * off-by-one "subtree size > k" instead of ">= k": k is set exactly equal to the side
    sizes of chosen edges (brooms, double stars, binary trees, random edges).
  * forgetting the r = v term (always n per test) or only handling one direction per edge.
  * computing |S_1| only and multiplying by n: asymmetric trees (brooms, caterpillars).
  * 32-bit overflow: answers reach ~n^2 = 4e10 (long chain with small k).
  * recursion depth: chains / deep random trees with n = 2e5.
  * per-test reset bugs: many tiny tests, up to t = 1e4.
  * degenerate k: k = 2 and k = n.

Answers come from samplecode.py (edge contribution formula).  Build checks with two
oracles that do not use the edge formula:
  * exhaustive: for every root, enumerate every k-subset, compute its LCA by climbing
    parents, count distinct LCAs (files whose tests are all tiny);
  * quadratic: for every root, BFS to get subtree sizes and count nodes whose subtree has
    >= k nodes (the lemma itself is covered by the exhaustive oracle on all labelled trees
    with n <= 5 and many random trees with n <= 8).
"""
from __future__ import annotations
import itertools
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
SAMPLE = ("4\n2 2\n1 2\n5 3\n1 2\n1 3\n1 4\n1 5\n6 3\n1 2\n1 3\n2 4\n2 5\n3 6\n"
          "10 5\n5 6\n4 9\n3 9\n2 6\n2 8\n8 9\n6 10\n1 6\n4 7\n")
SAMPLE_OUT = "2\n9\n17\n35\n"
MAX_T, MAX_N, MAX_SUM = 10_000, 200_000, 200_000


# ---------------------------------------------------------------- tree shapes
# Each shape returns a parent array par[1..n-1] over internal ids 0..n-1 (par[i] < i).
def shape_parents(r, n, shape):
    if shape == "chain":
        return [i - 1 for i in range(n)]
    if shape == "star":
        return [0] * n
    if shape == "random":
        return [0] + [r.randrange(i) for i in range(1, n)]
    if shape == "deep":
        return [0] + [r.randrange(max(0, i - 3), i) for i in range(1, n)]
    if shape == "binary":
        return [0] + [(i - 1) // 2 for i in range(1, n)]
    if shape == "caterpillar":
        spine = max(1, n // 3)
        return [0] + [i - 1 if i < spine else r.randrange(spine) for i in range(1, n)]
    if shape == "broom":   # handle then bristles on its end
        handle = max(1, r.randint(1, n - 1))
        return [0] + [i - 1 if i < handle else handle - 1 for i in range(1, n)]
    if shape == "doublestar":   # two hubs 0 and 1, leaves split between them
        return [0, 0] + [r.randint(0, 1) for _ in range(2, n)]
    raise ValueError(shape)


def edges_from_parents(r, par):
    n = len(par)
    label = list(range(1, n + 1)); r.shuffle(label)
    edges = []
    for i in range(1, n):
        u, v = label[i], label[par[i]]
        if r.random() < 0.5:
            u, v = v, u
        edges.append((u, v))
    r.shuffle(edges)
    return edges


def side_sizes(par):
    n = len(par)
    size = [1] * n
    for i in range(n - 1, 0, -1):
        size[par[i]] += size[i]
    return size


def make_test(r, n, shape, kmode="random"):
    par = shape_parents(r, n, shape)
    if kmode == "random":
        k = r.randint(2, n)
    elif kmode == "two":
        k = 2
    elif kmode == "n":
        k = n
    elif kmode == "half":
        k = max(2, n // 2)
    else:   # "exact": k equals one side of a random edge (clamped to [2, n])
        size = side_sizes(par)
        cands = [x for i in range(1, n) for x in (size[i], n - size[i]) if 2 <= x <= n]
        k = r.choice(cands) if cands else r.randint(2, n)
    return n, k, edges_from_parents(r, par)


def fmt(tests):
    lines = [str(len(tests))]
    for n, k, edges in tests:
        lines.append(f"{n} {k}")
        lines.extend(f"{u} {v}" for u, v in edges)
    return "\n".join(lines) + "\n"


SHAPES = ("chain", "star", "random", "deep", "binary", "caterpillar", "broom", "doublestar")


def all_labelled_trees():
    tests = []
    for n in range(2, 6):
        for prufer in itertools.product(range(1, n + 1), repeat=n - 2):
            degree = [1] * (n + 1)
            for x in prufer:
                degree[x] += 1
            edges = []
            for x in prufer:
                leaf = min(i for i in range(1, n + 1) if degree[i] == 1)
                edges.append((leaf, x)); degree[leaf] -= 1; degree[x] -= 1
            u, v = [i for i in range(1, n + 1) if degree[i] == 1]
            edges.append((u, v))
            for k in range(2, n + 1):
                tests.append((n, k, edges))
    return tests


def fill_tests(r, count, lo, hi, shapes, kmodes, budget=MAX_SUM):
    tests, total = [], 0
    while len(tests) < count:
        n = r.randint(lo, hi)
        if total + n > budget:
            break
        tests.append(make_test(r, n, r.choice(shapes), r.choice(kmodes)))
        total += n
    return tests


def generate(seed, attempt=0):
    r = random.Random(2167_600_000 + seed * 7919 + attempt * 104729)
    N = MAX_N
    if seed == 1:
        return fmt([(2, 2, [(2, 1)])])
    if seed == 2:     # every labelled tree with n <= 5, every k
        return fmt(all_labelled_trees())
    if seed == 3:     # many random tiny trees, exhaustive oracle
        return fmt(fill_tests(r, 700, 2, 8, SHAPES, ("random", "exact", "two", "n")))
    if seed == 4:     # t = 1e4 small trees
        return fmt(fill_tests(r, MAX_T, 2, 38, SHAPES, ("random", "exact", "two", "n", "half")))
    if seed == 5:     # medium trees, k at exact edge sides
        return fmt(fill_tests(r, 40, 100, 400, SHAPES, ("exact",)))
    if seed == 6:     # k = n everywhere (answer = n) mixed with k = n-1
        tests = fill_tests(r, 300, 2, 60, SHAPES, ("n",))
        tests += [(n, max(2, n - 1), e) for n, _, e in fill_tests(r, 300, 3, 60, SHAPES, ("n",))]
        return fmt(tests)
    if seed == 7:     # k = 2 on chains/stars/brooms, medium
        return fmt(fill_tests(r, 200, 20, 120, ("chain", "star", "broom", "deep"), ("two",)))
    if seed == 8:     # chain n = 2e5, k = 2: answer ~ n^2 (32-bit overflow)
        return fmt([make_test(r, N, "chain", "two")])
    if seed == 9:     # chain, k = n/2
        return fmt([make_test(r, N, "chain", "half")])
    if seed == 10:    # star, k = 2
        return fmt([make_test(r, N, "star", "two")])
    if seed == 11:    # star, k = n
        return fmt([make_test(r, N, "star", "n")])
    if seed == 12:    # random tree, random k
        return fmt([make_test(r, N, "random", "random")])
    if seed == 13:    # binary tree, k equal to a subtree size
        return fmt([make_test(r, N, "binary", "exact")])
    if seed == 14:    # caterpillar, exact k
        return fmt([make_test(r, N, "caterpillar", "exact")])
    if seed == 15:    # broom, exact k
        return fmt([make_test(r, N, "broom", "exact")])
    if seed == 16:    # deep random tree (recursion depth ~ n/2), small k
        n = N; return fmt([(n, r.randint(2, 10), make_test(r, n, "deep", "two")[2])])
    if seed == 17:    # two big tests
        return fmt([make_test(r, 100_000, "random", "exact"), make_test(r, 100_000, "chain", "exact")])
    if seed == 18:    # many medium tests, exact k, quadratic oracle
        return fmt(fill_tests(r, 60, 150, 300, SHAPES, ("exact",)))
    if seed == 19:    # double stars with k = one hub's side exactly, medium, oracle
        return fmt(fill_tests(r, 150, 4, 200, ("doublestar", "broom"), ("exact",)))
    # seed 20: sum n = 2e5 over ~200 mixed tests
    return fmt(fill_tests(r, 400, 200, 1800, SHAPES, ("random", "exact", "two", "n", "half")))


# ---------------------------------------------------------------- contract
def valid(text):
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    try:
        rows = [[int(x) for x in line.split(" ")] for line in lines]
    except ValueError:
        return False
    if len(rows[0]) != 1 or not 1 <= rows[0][0] <= MAX_T:
        return False
    t, p, total = rows[0][0], 1, 0
    for _ in range(t):
        if p >= len(rows) or len(rows[p]) != 2:
            return False
        n, k = rows[p]; p += 1
        if not 2 <= k <= n <= MAX_N:
            return False
        total += n
        if total > MAX_SUM or p + n - 1 > len(rows):
            return False
        dsu = list(range(n + 1))

        def find(x):
            while dsu[x] != x:
                dsu[x] = dsu[dsu[x]]; x = dsu[x]
            return x

        for row in rows[p:p + n - 1]:
            if len(row) != 2:
                return False
            u, v = row
            if not (1 <= u <= n and 1 <= v <= n and u != v):
                return False
            a, b = find(u), find(v)
            if a == b:          # cycle -> with n-1 edges also disconnected
                return False
            dsu[a] = b
        p += n - 1
    return p == len(rows)


def parse(text):
    tok = list(map(int, text.split()))
    t, p, tests = tok[0], 1, []
    for _ in range(t):
        n, k = tok[p], tok[p + 1]; p += 2
        edges = [(tok[p + 2 * i], tok[p + 2 * i + 1]) for i in range(n - 1)]
        p += 2 * (n - 1)
        tests.append((n, k, edges))
    return tests


def rooted(n, adj, root):
    parent = [0] * (n + 1); depth = [0] * (n + 1)
    parent[root] = 0
    order = [root]
    for x in order:
        for y in adj[x]:
            if y != parent[x]:
                parent[y] = x; depth[y] = depth[x] + 1; order.append(y)
    return parent, depth, order


def oracle_exhaustive(n, k, edges):
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    total = 0
    for root in range(1, n + 1):
        parent, depth, _ = rooted(n, adj, root)
        seen = set()
        for subset in itertools.combinations(range(1, n + 1), k):
            a = subset[0]
            for b in subset[1:]:
                x, y = a, b
                while depth[x] > depth[y]: x = parent[x]
                while depth[y] > depth[x]: y = parent[y]
                while x != y: x, y = parent[x], parent[y]
                a = x
            seen.add(a)
        total += len(seen)
    return total


def oracle_quadratic(n, k, edges):
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    total = 0
    for root in range(1, n + 1):
        parent, _, order = rooted(n, adj, root)
        size = [1] * (n + 1)
        for x in reversed(order):
            if x != root:
                size[parent[x]] += size[x]
        total += sum(1 for x in range(1, n + 1) if size[x] >= k)
    return total


def comb_count(n, k):
    from math import comb
    return comb(n, k)


def oracle(text):
    tests = parse(text)
    ex_cost = sum(n * comb_count(n, k) * k * n for n, k, _ in tests)
    if all(n <= 9 for n, _, _ in tests) and ex_cost <= 20_000_000:
        return "exhaustive", [oracle_exhaustive(*tc) for tc in tests]
    if sum(n * n for n, _, _ in tests) <= 8_000_000:
        return "quadratic", [oracle_quadratic(*tc) for tc in tests]
    if len(tests) > 1:
        # partial: check the smallest tests of a multi-test file within a budget
        budget, picked = 4_000_000, {}
        for i in sorted(range(len(tests)), key=lambda i: tests[i][0]):
            cost = tests[i][0] ** 2
            if cost > budget:
                break
            budget -= cost
            picked[i] = oracle_quadratic(*tests[i])
        if picked:
            return f"quadratic-partial {len(picked)}/{len(tests)} tests", picked
    return None, None


def run_reference(text):
    return subprocess.run([sys.executable, str(REFERENCE)], input=text, text=True,
                          capture_output=True, check=True).stdout


def build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 21):
        attempt = 0
        case = generate(seed)
        while case in cases:
            attempt += 1
            case = generate(seed, attempt)
        cases.append(case)
    checked = 0
    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {index}: violates input contract")
        answer = run_reference(case)
        if index == 0 and answer.split() != SAMPLE_OUT.split():
            raise SystemExit(f"sample mismatch: {answer!r}")
        how, expect = oracle(case)
        if how is not None:
            got = answer.split()
            if len(got) != len(parse(case)):
                raise SystemExit(f"case {index}: reference printed {len(got)} answers")
            pairs = expect.items() if isinstance(expect, dict) else enumerate(expect)
            if any(got[i] != str(x) for i, x in pairs):
                raise SystemExit(f"case {index}: oracle ({how}) disagrees with reference")
            checked += 1
        print(f"case {index}: {'ok (' + how + ')' if how else 'no oracle'}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")
    if checked < 10:
        raise SystemExit(f"only {checked} oracle-checked cases")


if __name__ == "__main__":
    build()
