#!/usr/bin/env python3
"""Codeforces 2208D1 Tree Orientation (Easy Version) -- generator, contract, oracle, build.

Written for this repository as a hand-off artifact; no external license.

The answer is not unique only in how the edges are listed (the tree itself is
unique when it exists), so the problem is judged by checker.py.

Shapes target the ways solutions go wrong:
  * Yes instances from random labelled trees with random / all-down / all-up /
    alternating orientations: paths (dense closure), in-stars and out-stars,
    caterpillars, binary trees, brooms; n = 2 minimum and n = 500 maximum;
  * No instances that defeat partial checks:
      - one reachability bit flipped (added or removed) in a valid matrix;
      - transitivity broken (covers form a tree but the closure differs);
      - closures of DAGs that are not trees (diamonds: too many covers);
      - covers count n-1 but form a cycle + a disconnected part;
      - mutual reachability (u reaches v and v reaches u), zero diagonal;
      - unions of two valid trees (a forest: n-2 covers);
  * files with t up to 10^4 tiny tests, and sum n^3 exactly at 500^3.
Oracle: (0) every test is re-decided independently (partial order whose Hasse
diagram is a spanning tree); (1) every test records its verdict when it is provable by construction
(closure of a tree -> Yes; forest, broken transitivity, zero diagonal, mutual
reachability, cover graph with a cycle -> No) and the reference must agree;
(2) every matrix of an oriented labelled tree with n <= 6 is enumerated
(Pruefer codes x orientations); for tests with n <= 6 the Yes/No verdict must
match membership.  Every reference output must be accepted by checker.py, and
three alternative listings (reversed edge order, shuffled, lower/upper case)
must be accepted as well.
"""
from __future__ import annotations
import itertools
import random
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
CHECKER = HERE / "checker.py"
SAMPLE = """11
4
1000
1111
1010
0001
4
1111
0111
0010
0111
4
0011
0111
0011
0001
4
1000
0110
0010
1111
4
1000
0110
1010
1111
5
10000
01011
00111
00010
00001
5
10000
11000
10101
10111
00001
5
10000
01101
00100
01110
10001
4
1100
0100
0011
0001
4
1110
0100
0010
0101
3
100
111
101
"""
SAMPLE_OUT = """Yes
2 3
2 4
3 1
No
No
Yes
2 3
4 1
4 2
No
No
Yes
2 1
3 1
3 5
4 3
No
No
Yes
1 2
1 3
4 2
Yes
2 3
3 1
"""
MAXN = 500
BUDGET = 500 ** 3
ORACLE_N = 6


# ---------------------------------------------------------------- matrices
def closure(n, edges):
    """edges: directed (u, v) 0-based on any DAG; returns list of row strings."""
    ch = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        ch[u].append(v); indeg[v] += 1
    order = [v for v in range(n) if indeg[v] == 0]
    for x in order:
        for y in ch[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                order.append(y)
    assert len(order) == n
    reach = [0] * n
    for x in reversed(order):
        acc = 1 << x
        for y in ch[x]:
            acc |= reach[y]
        reach[x] = acc
    return ["".join("1" if (reach[i] >> j) & 1 else "0" for j in range(n)) for i in range(n)]


def random_tree(r, n, kind):
    if n == 1:
        return []
    if kind == "path":
        e = [(i, i + 1) for i in range(n - 1)]
    elif kind == "star":
        e = [(0, i) for i in range(1, n)]
    elif kind == "cater":
        spine = max(1, n // 3)
        e = [(i, i + 1) for i in range(spine - 1)] + [(r.randrange(spine), i) for i in range(spine, n)]
    elif kind == "binary":
        e = [((i - 1) // 2, i) for i in range(1, n)]
    elif kind == "broom":
        h = max(1, n // 2)
        e = [(i, i + 1) for i in range(h - 1)] + [(h - 1, i) for i in range(h, n)]
    elif kind == "deep":
        e = [(r.randint(max(0, i - 3), i - 1), i) for i in range(1, n)]
    else:
        e = [(r.randrange(i), i) for i in range(1, n)]
    return e


def orient(r, n, e, mode):
    """e: parent-child pairs (p, c) with p < c in construction order."""
    out = []
    for idx, (p, c) in enumerate(e):
        if mode == "down":
            d = True
        elif mode == "up":
            d = False
        elif mode == "alt":
            d = (idx % 2 == 0)
        else:
            d = r.random() < 0.5
        out.append((p, c) if d else (c, p))
    return out


def relabel(r, n, edges):
    perm = list(range(n)); r.shuffle(perm)
    return [(perm[u], perm[v]) for u, v in edges]


EXPECT = {}   # id(rows) -> (rows, verdict); rows kept alive so ids are never reused


def known(rows, verdict):
    EXPECT[id(rows)] = (rows, verdict)
    return rows


def yes_case(r, n, kind=None, mode=None):
    kind = kind or r.choice(["path", "star", "cater", "binary", "broom", "deep", "rand", "rand"])
    mode = mode or r.choice(["down", "up", "alt", "rand", "rand"])
    edges = relabel(r, n, orient(r, n, random_tree(r, n, kind), mode))
    return known(closure(n, edges), True)


def flip_bit(r, rows, want_off_diag=True):
    n = len(rows)
    grid = [list(s) for s in rows]
    while True:
        i, j = r.randrange(n), r.randrange(n)
        if i != j or not want_off_diag:
            break
    grid[i][j] = "1" if grid[i][j] == "0" else "0"
    return ["".join(g) for g in grid]


def break_transitivity(r, n):
    """Tree with a directed path a->b->c; remove bit a->c (covers stay a tree)."""
    if n < 3:
        return None
    for _ in range(50):
        edges = relabel(r, n, orient(r, n, random_tree(r, n, r.choice(["path", "deep", "rand"])), r.choice(["down", "rand"])))
        rows = closure(n, edges)
        cand = [(i, j) for i in range(n) for j in range(n) if i != j and rows[i][j] == "1"]
        far = [(i, j) for i, j in cand if sum(1 for k in range(n) if rows[i][k] == "1" and rows[k][j] == "1") > 2]
        if far:
            i, j = r.choice(far)
            g = [list(s) for s in rows]; g[i][j] = "0"
            return known(["".join(x) for x in g], False)   # no longer transitive
    return None


def diamond_dag(r, n):
    """DAG closure with an undirected cycle (not a tree)."""
    if n < 4:
        return None
    e = [(r.randrange(i), i) for i in range(1, n)]
    # add one extra edge from an earlier vertex to a later vertex that is not its parent
    for _ in range(100):
        a, b = sorted(r.sample(range(n), 2))
        if (a, b) not in e:
            e.append((a, b)); break
    return closure(n, relabel(r, n, e))


def cycle_plus_forest(r, n):
    """n-1 covers: an oriented undirected cycle (zig-zag, so closure = covers) + separate tree."""
    if n < 5:
        return None
    k = r.choice([4, 6, 8]) if n >= 8 else 4
    k = min(k, n - 1 if (n - 1) % 2 == 0 else n - 2)
    if k < 4:
        return None
    # zig-zag cycle on k vertices (k even): sources at even, sinks at odd
    e = []
    for i in range(k):
        j = (i + 1) % k
        e.append((i, j) if i % 2 == 0 else (j, i))
    rest = list(range(k, n))
    for idx, v in enumerate(rest[1:], 1):
        p = rest[r.randrange(idx)]
        e.append((p, v) if r.random() < 0.5 else (v, p))
    # covers: k (cycle) + (n-k-1) = n-1; the underlying cover graph has a cycle
    return known(closure(n, relabel(r, n, e)), False)


def mutual(r, n):
    rows = yes_case(r, n)
    g = [list(s) for s in rows]
    for i in range(n):
        for j in range(n):
            if g[i][j] == "1" and i != j:
                g[j][i] = "1"
                return known(["".join(x) for x in g], False)   # mutual reachability
    return ["".join(x) for x in g]


def zero_diag(r, n):
    rows = yes_case(r, n)
    g = [list(s) for s in rows]
    i = r.randrange(n); g[i][i] = "0"
    return known(["".join(x) for x in g], False)


def forest(r, n):
    if n < 2:
        return None
    a = r.randint(1, n - 1)
    e = orient(r, a, random_tree(r, a, "rand"), "rand")
    e2 = [(u + a, v + a) for u, v in orient(r, n - a, random_tree(r, n - a, "rand"), "rand")]
    return known(closure(n, relabel(r, n, e + e2)), False)   # disconnected: n-2 covers


NO_MAKERS = [break_transitivity, diamond_dag, cycle_plus_forest, mutual, zero_diag, forest]


def no_case(r, n):
    for _ in range(20):
        mk = r.choice(NO_MAKERS + ["flip"])
        rows = flip_bit(r, yes_case(r, n)) if mk == "flip" else mk(r, n)
        if rows is not None:
            return rows
    return zero_diag(r, n)


def fmt(tests):
    global LAST_EXPECT
    LAST_EXPECT = [EXPECT[id(rows)][1] if id(rows) in EXPECT and EXPECT[id(rows)][0] is rows else None
                   for rows in tests]
    out = [str(len(tests))]
    for rows in tests:
        out.append(str(len(rows)))
        out.extend(rows)
    return "\n".join(out) + "\n"


def mixed(r, count, lo, hi, p_yes=0.5, budget=BUDGET):
    tests = []; used = 0
    while len(tests) < count:
        n = r.randint(lo, hi)
        if used + n ** 3 > budget:
            break
        used += n ** 3
        tests.append(yes_case(r, n) if r.random() < p_yes else no_case(r, n))
    return tests


def generate(seed):
    r = random.Random(22080401 + seed * 1000003)
    if seed == 1:        # every tiny n: n = 2 (all 4 matrices + many), n = 3 mixed, t = 1e4
        tests = [["10", "01"], ["11", "01"], ["10", "11"], ["11", "11"], ["00", "01"], ["01", "10"]]
        tests += mixed(r, 10000 - len(tests), 2, 3)
    elif seed == 2:      # n = 4..6 heavy oracle coverage, half No
        tests = mixed(r, 4000, 4, 6)
    elif seed == 3:      # n = 5..6 No instances of every kind
        tests = []
        for i in range(3000):
            n = r.randint(5, 6)
            mk = NO_MAKERS[i % len(NO_MAKERS)]
            rows = mk(r, n) or no_case(r, n)
            tests.append(rows)
    elif seed == 4:      # n = 6 single-bit flips of valid matrices (close calls)
        tests = [flip_bit(r, yes_case(r, 6)) if i % 3 else yes_case(r, 6) for i in range(3000)]
    elif seed == 5:      # max n = 500, oriented path all down (full upper triangle)
        tests = [yes_case(r, MAXN, "path", "down")]
    elif seed == 6:      # max n = 500, out-star / in-star halves -> two tests of 396 (budget)
        tests = [yes_case(r, 396, "star", "down"), yes_case(r, 396, "star", "up")]
    elif seed == 7:      # max n = 500, random tree, random orientation
        tests = [yes_case(r, MAXN, "rand", "rand")]
    elif seed == 8:      # max n = 500, transitivity broken on a deep tree
        tests = [break_transitivity(r, MAXN)]
    elif seed == 9:      # max n = 500, extra DAG edge (diamond)
        tests = [diamond_dag(r, MAXN)]
    elif seed == 10:     # max n = 500, cycle + forest with exactly n-1 covers
        tests = [cycle_plus_forest(r, MAXN)]
    elif seed == 11:     # 8 x n = 250: alternating orientations, binary, caterpillar, broom
        tests = [yes_case(r, 250, k, m) for k, m in
                 [("path", "alt"), ("binary", "down"), ("cater", "rand"), ("broom", "up"),
                  ("deep", "alt"), ("binary", "up"), ("rand", "alt"), ("path", "rand")]]
    elif seed == 12:     # 8 x n = 250 No: flips, mutual, zero diagonal, forest
        tests = [flip_bit(r, yes_case(r, 250)), mutual(r, 250), zero_diag(r, 250), forest(r, 250),
                 flip_bit(r, yes_case(r, 250, "path", "down")), break_transitivity(r, 250),
                 diamond_dag(r, 250), cycle_plus_forest(r, 250)]
    elif seed == 13:     # medium n 20..60 mixed, fills budget
        tests = mixed(r, 10000, 20, 60)
    elif seed == 14:     # n 7..15 mixed, many tests
        tests = mixed(r, 10000, 7, 15)
    elif seed == 15:     # max n = 500 forest (n-2 covers) -- "Yes" if you skip the count check
        tests = [forest(r, MAXN)]
    elif seed == 16:     # max n = 500, removing a single cover bit of a path (still n-1-ish covers)
        rows = yes_case(r, MAXN, "path", "rand")
        tests = [flip_bit(r, rows)]
    elif seed == 17:     # n 100..200 all Yes, varied shapes
        tests = mixed(r, 10000, 100, 200, p_yes=1.0)
    elif seed == 18:     # n 2..6 all Yes (oracle), t = 1e4, every shape
        tests = mixed(r, 10000, 2, 6, p_yes=1.0)
    elif seed == 19:     # n 30..120 all No, every maker
        tests = []; used = 0
        while True:
            n = r.randint(30, 120)
            if used + n ** 3 > BUDGET:
                break
            mk = NO_MAKERS[len(tests) % len(NO_MAKERS)]
            rows = mk(r, n) or no_case(r, n)
            tests.append(rows); used += n ** 3
    else:                # seed 20: one n = 400 Yes plus a max of small tests sharing the budget
        tests = [yes_case(r, 400, "rand", "alt")]
        tests += mixed(r, 10000 - 1, 2, 30, budget=BUDGET - 400 ** 3)
    return fmt(tests)


# ---------------------------------------------------------------- contract
def parse(text):
    tok = text.split(); p = 1
    tests = []
    for _ in range(int(tok[0])):
        n = int(tok[p]); p += 1
        tests.append(tok[p:p + n]); p += n
    return tests


def valid(text):
    try:
        lines = text.split("\n")
        if lines[-1] != "":
            return False
        lines = lines[:-1]
        t = int(lines[0])
        if lines[0] != str(t) or not 1 <= t <= 10 ** 4:
            return False
        i = 1; cube = 0
        for _ in range(t):
            n = int(lines[i])
            if lines[i] != str(n) or not 2 <= n <= MAXN:
                return False
            i += 1; cube += n ** 3
            for _ in range(n):
                s = lines[i]; i += 1
                if len(s) != n or s.strip("01") != "":
                    return False
        return i == len(lines) and cube <= BUDGET
    except (ValueError, IndexError):
        return False


# ---------------------------------------------------------------- oracle
def all_tree_matrices(nmax):
    table = {}
    for n in range(2, nmax + 1):
        seen = set()
        for code in itertools.product(range(n), repeat=n - 2):
            # Pruefer decode
            degree = [1] * n
            for x in code:
                degree[x] += 1
            e = []
            for x in code:
                leaf = min(i for i in range(n) if degree[i] == 1)
                e.append((leaf, x)); degree[leaf] -= 1; degree[x] -= 1
            u, v = [i for i in range(n) if degree[i] == 1]
            e.append((u, v))
            for mask in range(1 << (n - 1)):
                de = [(a, b) if (mask >> k) & 1 else (b, a) for k, (a, b) in enumerate(e)]
                seen.add(tuple(closure(n, de)))
        table[n] = seen
    return table


def order_verdict(rows):
    """Independent Yes/No: the matrix must be a partial order (reflexive, antisymmetric,
    transitive) whose Hasse diagram is a spanning tree.  Uses row unions, not the
    reference's popcount test."""
    n = len(rows)
    R = [int(s[::-1], 2) for s in rows]
    for i in range(n):
        if not (R[i] >> i) & 1:
            return False
    strict = [R[i] & ~(1 << i) for i in range(n)]
    for i in range(n):
        x = strict[i]
        while x:
            low = x & -x; j = low.bit_length() - 1; x ^= low
            if (strict[j] >> i) & 1:          # mutual reachability
                return False
            if R[j] & ~R[i]:                  # not transitive
                return False
    parent = list(range(n)); edges = 0
    for i in range(n):
        below = 0
        x = strict[i]
        while x:
            low = x & -x; j = low.bit_length() - 1; x ^= low
            below |= strict[j]
        cover = strict[i] & ~below
        while cover:
            low = cover & -cover; j = low.bit_length() - 1; cover ^= low
            edges += 1
            a, b = i, j
            while parent[a] != a:
                a = parent[a]
            while parent[b] != b:
                b = parent[b]
            if a == b:
                return False
            parent[a] = b
    return edges == n - 1


def check_output(inp, out, ans):
    with tempfile.TemporaryDirectory() as d:
        pi, po, pa = Path(d, "in"), Path(d, "out"), Path(d, "ans")
        pi.write_text(inp); po.write_text(out); pa.write_text(ans)
        res = subprocess.run([sys.executable, "-I", str(CHECKER), str(pi), str(po), str(pa)],
                             capture_output=True, text=True)
    return res.returncode, res.stdout.strip()


def alternatives(text, ans):
    """Three differently-listed correct outputs derived from the reference."""
    tests = parse(text)
    tok = ans.split(); p = 0
    alt_rev, alt_shuf, alt_case = [], [], []
    r = random.Random(len(text))
    for rows in tests:
        n = len(rows)
        word = tok[p]; p += 1
        if word == "No":
            alt_rev.append("no"); alt_shuf.append("NO"); alt_case.append("nO")
            continue
        edges = [(tok[p + 2 * k], tok[p + 2 * k + 1]) for k in range(n - 1)]; p += 2 * (n - 1)
        alt_rev.append("yes"); alt_rev.extend(f"{a} {b}" for a, b in reversed(edges))
        sh = edges[:]; r.shuffle(sh)
        alt_shuf.append("YES " + " ".join(f"{a} {b}" for a, b in sh))
        alt_case.append("yEs"); alt_case.extend(f"  {a}\t{b}" for a, b in edges)
    return ["\n".join(alt_rev) + "\n", "\n".join(alt_shuf) + "\n", "\n".join(alt_case)]


def build():
    out = HERE / "data"; out.mkdir(exist_ok=True)
    table = all_tree_matrices(ORACLE_N)
    cases = [SAMPLE]; expects = [[None] * 11]
    for seed in range(1, 40):
        EXPECT.clear()
        cases.append(generate(seed)); expects.append(LAST_EXPECT)
    assert len(set(cases)) == len(cases)
    code, msg = check_output(SAMPLE, SAMPLE_OUT, SAMPLE_OUT)
    if code != 0:
        raise SystemExit(f"checker rejects the official sample output: {msg}")
    for idx, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {idx}: input contract violated")
        ans = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                             capture_output=True, check=True).stdout
        if idx == 0:
            code, msg = check_output(case, SAMPLE_OUT, ans)
            if code != 0 or [w for w in ans.split() if w in ("Yes", "No")] != \
                    [w for w in SAMPLE_OUT.split() if w in ("Yes", "No")]:
                raise SystemExit(f"sample verdicts differ from the official output: {msg}")
        tests = parse(case)
        verdicts = [w for w in ans.split() if w in ("Yes", "No")]
        assert len(verdicts) == len(tests)
        small = 0; structural = 0
        for rows, v, e in zip(tests, verdicts, expects[idx]):
            if order_verdict(rows) != (v == "Yes"):
                raise SystemExit(f"case {idx}: independent partial-order check disagrees")
            if e is not None:
                structural += 1
                if e != (v == "Yes"):
                    raise SystemExit(f"case {idx}: verdict contradicts how the test was built")
            if len(rows) <= ORACLE_N:
                small += 1
                if (tuple(rows) in table[len(rows)]) != (v == "Yes"):
                    raise SystemExit(f"case {idx}: oracle disagreement on n={len(rows)}")
        code, msg = check_output(case, ans, ans)
        if code != 0:
            raise SystemExit(f"case {idx}: checker rejects the reference: {msg}")
        for k, alt in enumerate(alternatives(case, ans)):
            code, msg = check_output(case, alt, ans)
            if code != 0:
                raise SystemExit(f"case {idx}: checker rejects alternative listing {k}: {msg}")
        (out / f"{idx}.in").write_text(case, encoding="utf-8")
        (out / f"{idx}.out").write_text(ans, encoding="utf-8")
        yes = verdicts.count("Yes")
        print(f"case {idx}: t={len(tests)} yes={yes} no={len(tests) - yes} maxn={max(map(len, tests))} "
              f"in={len(case)}B out={len(ans)}B oracle={small} by-construction={structural}")


if __name__ == "__main__":
    build()
