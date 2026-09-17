#!/usr/bin/env python3
"""Codeforces 2192D Cost of Tree -- generator, input contract, oracle and data build.

Written for this repository as a hand-off artifact; no external license.

Statement: t (1..1e4) test cases; each has n (1..2e5), a_1..a_n (1..2e5), n-1 edges forming a
tree; sum n <= 2e5.  For every r print the max cost of subtree(r) after at most one
"cut u (u != r), re-hang under any v still reachable from r" operation.

Shapes (how solutions go wrong):
  * singles     -- many n=1 / n=2 tests (no operation possible, answer 0 / edge cases).
  * tiny_multi  -- thousands-ish of small random trees, all oracle-checked.
  * on_path     -- a long chain with one fat shallow branch: best move takes a node ON the
                   deepest path, where "deepest node outside" is NOT the global maximum
                   (kills "always use max height of r").
  * twin_depth  -- two branches of equal depth (tie of top-1/top-2 heights).
  * chain       -- long chain (recursion depth, answers ~1e15: 32-bit overflow).
  * star        -- star / broom / caterpillar.
  * random big  -- random recursive trees close to the sum-n bound.
Labels are shuffled and edge orientation/order randomised everywhere.
Output is kept <= ~1 MB, so the deep chain is 50000 nodes rather than 2e5.

Oracle: literal simulation -- for every r, every u != r in subtree(r), every v still reachable,
rebuild the parent array, recompute depths by BFS and sum a*depth.  O(n^4) per test, so it runs
on every test with n <= 12 (cases with bigger tests are checked per-test where n <= 12).
"""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
SAMPLE = """3
5
1 3 2 1 2
1 2
2 3
3 4
3 5
7
1 2 3 1 3 2 1
1 2
2 3
3 4
4 5
4 6
3 7
5
5 4 3 2 1
1 2
2 3
3 4
4 5
"""
SAMPLE_OUT = "18 10 5 0 0 \n40 28 18 8 0 0 0 \n20 10 4 1 0\n"
MAXA = 200000
ORACLE_N = 12


def emit(r, parents, a):
    """parents[i] (i>=1) = parent of node i in 0-based build order; relabel randomly."""
    n = len(a)
    perm = list(range(1, n + 1)); rest = perm[1:]; r.shuffle(rest); perm = [1] + rest
    edges = []
    for i in range(1, n):
        u, v = perm[i], perm[parents[i]]
        edges.append((u, v) if r.random() < 0.5 else (v, u))
    r.shuffle(edges)
    lab = [0] * n
    for i in range(n): lab[perm[i] - 1] = a[i]
    return f"{n}\n{' '.join(map(str, lab))}\n" + "".join(f"{u} {v}\n" for u, v in edges)


def vals(r, n, lo=1, hi=MAXA):
    return [r.randint(lo, hi) for _ in range(n)]


def random_tree(r, n, lo=1, hi=MAXA, width=None):
    par = [0] + [r.randrange(max(0, i - width) if width else 0, i) for i in range(1, n)]
    return emit(r, par, vals(r, n, lo, hi))


def chain(r, n, lo=1, hi=MAXA):
    return emit(r, [0] + list(range(n - 1)), vals(r, n, lo, hi))


def on_path(r, n, fat_len):
    # root 0 - chain 1..L; a fat branch hanging at depth 1 with short depth, heavy values.
    L = n - fat_len - 1
    par = [0] + list(range(L))            # nodes 1..L chain below 0 (node i parent i-1)
    base = L + 1
    for j in range(fat_len):
        par.append(0 if j == 0 else base + r.randrange(0, j) if r.random() < 0.3 else base)
    a = [r.randint(1, 5) for _ in range(L + 1)] + [r.randint(MAXA // 2, MAXA) for _ in range(fat_len)]
    if r.random() < 0.5:
        a[1] = MAXA; a[2] = MAXA
    return emit(r, par, a)


def twin(r, n):
    half = (n - 1) // 2
    par = [0]
    for b in range(2):
        start = len(par)
        for j in range(half):
            par.append(0 if j == 0 else start + j - 1)
    while len(par) < n:
        par.append(r.randrange(0, len(par)))
    return emit(r, par, vals(r, n))


def star(r, n, kind):
    if kind == "star":
        par = [0] + [0] * (n - 1)
    elif kind == "broom":
        k = n // 2; par = [0] + list(range(k - 1)) + [k - 1] * (n - k)
    else:  # caterpillar
        k = max(1, n // 3); par = [0] + list(range(k - 1)) + [r.randrange(k) for _ in range(n - k)]
    return emit(r, par, vals(r, n))


def pack(tests):
    return f"{len(tests)}\n" + "".join(tests)


def generate(seed):
    r = random.Random(2192_0004 * 1000 + seed)
    if seed == 1:   # singles and pairs
        return pack([random_tree(r, r.randint(1, 2)) for _ in range(10000)])
    if seed == 2:   # t=1, n=1
        return pack([f"1\n{r.randint(1, MAXA)}\n"])
    if seed in (3, 4, 5):   # many tiny random trees
        tests = []; total = 0
        while total < 20000 and len(tests) < 3000:
            n = r.randint(1, ORACLE_N); total += n
            tests.append(random_tree(r, n, 1, [5, MAXA, 3][seed - 3]))
        return pack(tests)
    if seed == 6:   # tiny adversarial mix: small on_path / twin / chain / star
        tests = []
        for i in range(1500):
            k = i % 5; n = r.randint(3, ORACLE_N)
            if k == 0: tests.append(on_path(r, n, r.randint(1, max(1, n // 3))))
            elif k == 1: tests.append(twin(r, n))
            elif k == 2: tests.append(chain(r, n))
            elif k == 3: tests.append(star(r, n, r.choice(["star", "broom", "cater"])))
            else: tests.append(random_tree(r, n, 1, MAXA, width=2))
        return pack(tests)
    if seed == 7:   # hand-made on-path traps
        tests = [
            "4\n1 100 1 1\n1 2\n2 3\n1 4\n",          # moving 2 under 4 beats moving 4 under 3?
            "5\n1 50 1 1 1\n1 2\n2 3\n3 4\n1 5\n",
            "3\n1 1 1\n1 2\n1 3\n",
            "2\n7 9\n2 1\n",
            "6\n1 200000 200000 1 1 1\n1 2\n2 3\n3 4\n4 5\n1 6\n",
        ]
        tests += [on_path(r, r.randint(4, ORACLE_N), r.randint(1, 3)) for _ in range(500)]
        return pack(tests)
    if seed == 8:   # medium random, oracle on the small ones
        tests = [random_tree(r, r.randint(1, 60), 1, MAXA, width=r.choice([None, 3])) for _ in range(800)]
        return pack(tests)
    if seed == 9:   # deep chain, huge values (overflow)
        return pack([chain(r, 50000, MAXA - 5, MAXA)])
    if seed == 10:  # chain split into two tests plus small values
        return pack([chain(r, 30000, 1, 3), chain(r, 20000, MAXA // 2, MAXA)])
    if seed == 11:  # big on_path
        return pack([on_path(r, 40000, 1000), on_path(r, 30000, 5)])
    if seed == 12:  # twin branches
        return pack([twin(r, 40000), twin(r, 7), twin(r, 9)])
    if seed == 13:  # star max n
        return pack([star(r, 200000, "star")])
    if seed == 14:  # broom and caterpillar
        return pack([star(r, 30000, "broom"), star(r, 100000, "cater")])
    if seed == 15:  # random recursive tree, max n
        return pack([random_tree(r, 150000)])
    if seed == 16:  # narrow-window random trees (deep, bushy)
        return pack([random_tree(r, 60000, 1, MAXA, width=3), random_tree(r, 60000, 1, 10, width=50)])
    if seed == 17:  # many medium tests, sum near bound
        return pack([random_tree(r, r.randint(1, 40), 1, MAXA, width=r.choice([None, 2])) for _ in range(8000)])
    if seed == 18:  # binary-ish tree
        n = 150000; par = [0] + [(i - 1) // 2 for i in range(1, n)]
        return pack([emit(r, par, vals(r, n))])
    if seed == 19:  # all a = MAXA random tree + a=1 chain
        return pack([random_tree(r, 80000, MAXA, MAXA, width=10), chain(r, 20000, 1, 1)])
    # seed 20: t = 1e4, many small adversarial tests
    tests = []
    for i in range(10000):
        n = r.randint(1, 8); k = i % 4
        tests.append([random_tree(r, n), chain(r, n), twin(r, max(n, 3)), on_path(r, max(n, 3), 1)][k])
    return pack(tests)


def parse(text):
    tok = text.split(); p = 0
    t = int(tok[p]); p += 1; res = []
    for _ in range(t):
        n = int(tok[p]); p += 1
        a = list(map(int, tok[p:p + n])); p += n
        e = [(int(tok[p + 2 * i]), int(tok[p + 2 * i + 1])) for i in range(n - 1)]; p += 2 * (n - 1)
        res.append((n, a, e))
    return res, p == len(tok)


def valid(text):
    try:
        if not text.endswith("\n"):
            return False
        lines = text.split("\n")[:-1]
        if any(l != l.strip() or "  " in l for l in lines):
            return False
        li = 0
        t = int(lines[li]); li += 1
        if not 1 <= t <= 10000:
            return False
        total = 0
        for _ in range(t):
            n = int(lines[li]); li += 1
            if not 1 <= n <= 200000:
                return False
            total += n
            a = list(map(int, lines[li].split())); li += 1
            if len(a) != n or not all(1 <= x <= MAXA for x in a):
                return False
            dsu = list(range(n + 1))

            def find(x):
                while dsu[x] != x:
                    dsu[x] = dsu[dsu[x]]; x = dsu[x]
                return x
            for _ in range(n - 1):
                uv = list(map(int, lines[li].split())); li += 1
                if len(uv) != 2 or not all(1 <= x <= n for x in uv):
                    return False
                fu, fv = find(uv[0]), find(uv[1])
                if fu == fv:          # self-loop or cycle => not a tree
                    return False
                dsu[fu] = fv
        return li == len(lines) and total <= 200000
    except (ValueError, IndexError):
        return False


def brute(n, a, edges):
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    par = [0] * (n + 1); order = [1]; seen = {1}
    for u in order:
        for v in adj[u]:
            if v not in seen:
                seen.add(v); par[v] = u; order.append(v)

    def cost(root, parent):
        ch = {}
        for x, px in parent.items():
            ch.setdefault(px, []).append(x)
        tot = 0; frontier = [(root, 0)]
        while frontier:
            x, d = frontier.pop(); tot += a[x - 1] * d
            for y in ch.get(x, []):
                frontier.append((y, d + 1))
        return tot

    ans = []
    for r in range(1, n + 1):
        sub = [r]; i = 0
        while i < len(sub):
            x = sub[i]; i += 1
            sub += [y for y in adj[x] if y != par[x]]
        parent = {x: par[x] for x in sub if x != r}
        best = cost(r, parent)
        for u in sub:
            if u == r:
                continue
            below = {u}; stack = [u]
            while stack:
                x = stack.pop()
                for y in adj[x]:
                    if y != par[x] and y not in below:
                        below.add(y); stack.append(y)
            for v in sub:
                if v in below:
                    continue
                np_ = dict(parent); np_[u] = v
                best = max(best, cost(r, np_))
        ans.append(best)
    return ans


def build():
    out = HERE / "data"; out.mkdir(exist_ok=True)
    for f in out.glob("*"):
        f.unlink()
    cases = [SAMPLE] + [generate(s) for s in range(1, 21)]
    if len(set(cases)) != len(cases):
        raise SystemExit("duplicate inputs")
    checked_cases = 0
    for idx, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {idx} violates the input contract")
        res = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                             capture_output=True, check=True, timeout=60)
        got = res.stdout.split("\n")
        if idx == 0 and res.stdout.split() != SAMPLE_OUT.split():
            raise SystemExit(f"sample mismatch: {res.stdout!r}")
        tests, _ = parse(case)
        checked = 0
        for i, (n, a, e) in enumerate(tests):
            if n <= ORACLE_N:
                if list(map(int, got[i].split())) != brute(n, a, e):
                    raise SystemExit(f"case {idx} test {i}: oracle disagreement")
                checked += 1
        if checked:
            checked_cases += 1
        print(f"case {idx}: {len(tests)} tests, {checked} oracle-checked", file=sys.stderr)
        (out / f"{idx}.in").write_text(case); (out / f"{idx}.out").write_text(res.stdout)
    print(f"oracle-checked cases: {checked_cases}", file=sys.stderr)


if __name__ == "__main__":
    build()
