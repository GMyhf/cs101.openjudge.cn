#!/usr/bin/env python3
"""Codeforces 2227H Fallen Leaves -- generator, input contract, oracle, build.

Written for this repository as a hand-off artifact; no external license.

Shapes target the ways solutions go wrong:
  * odd number of leaves where *which* leaf is left out matters (spiders with legs of
    different lengths, brooms, double spiders) -- kills "drop the deepest/first leaf";
  * subtrees holding an even number of leaves that are non-contiguous-friendly for
    "pair consecutive leaves in DFS order" -- random/caterpillar/binary trees;
  * n = 3 minimum, stars (k = n-1 odd/even), long paths (k = 2, answer n-1, deep
    recursion), complete binary trees, caterpillars at sum n = 2e5;
  * multi-test files with t up to 1e4 many small trees;
  * every tree has its labels shuffled so vertex 1 is not a convenient root.
Oracle: BFS all-pairs leaf distances + exhaustive bitmask DP over leaf matchings
(allowing exactly one skipped leaf when k is odd), run on every test whose leaf
count is <= ORACLE_K; a case is oracle-checked only if all its tests are.
"""
from __future__ import annotations
import hashlib
import random
import subprocess
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
SAMPLE = """4
4
1 2
2 3
2 4
6
1 2
2 3
2 4
4 5
4 6
7
1 2
2 3
3 4
2 5
5 6
5 7
5
1 2
1 3
3 4
3 5
"""
SAMPLE_OUT = "2\n4\n5\n2\n"
MAXN = 200000
ORACLE_K = 12


# ---------------------------------------------------------------- tree shapes
def relabel(r, n, edges):
    perm = list(range(1, n + 1)); r.shuffle(perm)
    es = [(perm[u - 1], perm[v - 1]) for u, v in edges]
    es = [(v, u) if r.random() < 0.5 else (u, v) for u, v in es]
    r.shuffle(es)
    return es


def random_tree(r, n, window=None):
    e = []
    for i in range(2, n + 1):
        lo = 1 if window is None else max(1, i - window)
        e.append((r.randint(lo, i - 1), i))
    return e


def path(n):
    return [(i, i + 1) for i in range(1, n)]


def star(n):
    return [(1, i) for i in range(2, n + 1)]


def spider(legs):
    e = []; nxt = 2
    for L in legs:
        prev = 1
        for _ in range(L):
            e.append((prev, nxt)); prev = nxt; nxt += 1
    return nxt - 1, e


def caterpillar(r, spine, n):
    e = path(spine)
    for i in range(spine + 1, n + 1):
        e.append((r.randint(1, spine), i))
    return e


def complete_binary(n):
    return [(i // 2, i) for i in range(2, n + 1)]


def broom(handle, bristles):
    n = handle + bristles
    e = path(handle) + [(handle, i) for i in range(handle + 1, n + 1)]
    return n, e


def double_spider(r, legs_a, legs_b, bridge):
    na, ea = spider(legs_a)
    nb, eb = spider(legs_b)
    e = list(ea)
    # bridge path from a's centre (1) to b's centre
    prev = 1; nxt = na + 1
    for _ in range(bridge):
        e.append((prev, nxt)); prev = nxt; nxt += 1
    off = nxt - 1  # b vertex x maps to off + x
    e.append((prev, off + 1))
    for u, v in eb:
        e.append((off + u, off + v))
    return off + nb, e


def fmt(tests):
    out = [str(len(tests))]
    for n, e in tests:
        out.append(str(n))
        out.extend(f"{u} {v}" for u, v in e)
    return "\n".join(out) + "\n"


def small_mixed(r, count, lo, hi):
    tests = []
    for _ in range(count):
        n = r.randint(lo, hi)
        kind = r.randrange(5)
        if kind == 0:
            e = random_tree(r, n)
        elif kind == 1:
            e = random_tree(r, n, 2)
        elif kind == 2:
            e = caterpillar(r, max(1, n // 3), n)
        elif kind == 3:
            legs = []
            left = n - 1
            while left > 0:
                L = min(left, r.randint(1, 4)); legs.append(L); left -= L
            n, e = spider(legs)
        else:
            e = star(n) if r.random() < 0.3 else random_tree(r, n)
        tests.append((n, relabel(r, n, e)))
    return tests


def fill_budget(r, tests, total, lo, hi):
    used = sum(n for n, _ in tests)
    while len(tests) < 10000 and used + lo <= total:
        n = min(r.randint(lo, hi), total - used)
        if n < 3:
            break
        tests.append((n, relabel(r, n, random_tree(r, n, r.choice([None, 1, 2, 3])))))
        used += n
    return tests


def generate(seed, attempt=0):
    r = random.Random(2227_0008 * 131 + seed * 7919 + attempt)
    tests = []
    if seed == 1:        # every labelled-shape tree with n = 3..7, many tiny tests
        tests = small_mixed(r, 3000, 3, 7)
    elif seed == 2:      # n = 3 minimum and all tiny stars/paths
        for n in range(3, 12):
            tests.append((n, relabel(r, n, star(n))))
            tests.append((n, relabel(r, n, path(n))))
        tests.append((3, [(1, 2), (2, 3)])); tests.append((3, [(3, 1), (1, 2)]))
        tests += small_mixed(r, 500, 3, 9)
    elif seed == 3:      # spiders with odd leg count and very uneven legs (small, oracle)
        for _ in range(600):
            legs = [r.choice([1, 1, 2, 5, 9]) for _ in range(r.choice([3, 5, 7, 9, 11]))]
            n, e = spider(legs); tests.append((n, relabel(r, n, e)))
    elif seed == 4:      # double spiders / brooms, odd leaves, choice of omitted leaf matters
        for _ in range(400):
            a = [r.randint(1, 6) for _ in range(r.randint(2, 6))]
            b = [r.randint(1, 6) for _ in range(r.randint(1, 6))]
            n, e = double_spider(r, a, b, r.randint(0, 5)); tests.append((n, relabel(r, n, e)))
        for _ in range(200):
            n, e = broom(r.randint(1, 12), r.randint(2, 11)); tests.append((n, relabel(r, n, e)))
    elif seed == 5:      # medium random trees with <= ORACLE_K leaves (oracle), deep-ish
        for _ in range(120):
            n = r.randint(15, 60)
            while True:
                e = random_tree(r, n, r.choice([1, 2, 3]))
                deg = [0] * (n + 1)
                for u, v in e:
                    deg[u] += 1; deg[v] += 1
                if sum(1 for d in deg[1:] if d == 1) <= ORACLE_K:
                    break
            tests.append((n, relabel(r, n, e)))
    elif seed == 6:      # caterpillars small (oracle)
        for _ in range(800):
            n = r.randint(4, 13)
            tests.append((n, relabel(r, n, caterpillar(r, r.randint(2, n - 2), n))))
    elif seed == 7:      # t = 1e4 small random trees, sum n = 2e5
        tests = small_mixed(r, 10000, 3, 30)
        used = sum(n for n, _ in tests)
        while used > MAXN:
            n, _ = tests.pop(); used -= n
    elif seed == 8:      # max star, k = n-1 odd
        tests = [(MAXN, relabel(r, MAXN, star(MAXN)))]
    elif seed == 9:      # max path, k = 2
        tests = [(MAXN, relabel(r, MAXN, path(MAXN)))]
    elif seed == 10:     # max caterpillar
        tests = [(MAXN, relabel(r, MAXN, caterpillar(r, 60000, MAXN)))]
    elif seed == 11:     # max uniform random tree
        tests = [(MAXN, relabel(r, MAXN, random_tree(r, MAXN)))]
    elif seed == 12:     # complete binary tree, n even -> odd leaves count
        n = MAXN - 1
        tests = [(n, relabel(r, n, complete_binary(n)))]
    elif seed == 13:     # max spider: odd #legs, one very long leg vs many short
        legs = [100001] + [1] * 20000 + [2] * 20000 + [3] * 13332
        n, e = spider(legs)
        tests = [(n, relabel(r, n, e))]
    elif seed == 14:     # max broom with long handle, odd bristles
        n, e = broom(100000, 99999)
        tests = [(n, relabel(r, n, e))]
    elif seed == 15:     # deep random tree (window 3) at max
        tests = [(MAXN, relabel(r, MAXN, random_tree(r, MAXN, 3)))]
    elif seed == 16:     # double spider at max: odd legs, uneven, long bridge
        a = [r.randint(1, 50) for _ in range(1501)]
        b = [r.randint(1, 50) for _ in range(1500)]
        n, e = double_spider(r, a, b, 0)
        extra = MAXN - n
        n, e = double_spider(r, a, b, max(0, extra - 1) if extra > 0 else 0)
        tests = [(n, relabel(r, n, e))]
    elif seed == 17:     # medium multi: n ~ 1000..5000 mixed
        tests = fill_budget(r, [], MAXN, 1000, 5000)
    elif seed == 18:     # tiny spiders/brooms mixed with stars at t = 1e4
        tests = []
        for _ in range(3500):
            legs = [r.randint(1, 3) for _ in range(r.choice([3, 4, 5]))]
            n, e = spider(legs); tests.append((n, relabel(r, n, e)))
        for _ in range(3500):
            n, e = broom(r.randint(1, 8), r.randint(2, 7)); tests.append((n, relabel(r, n, e)))
    elif seed == 19:     # small random trees n 8..16 (oracle; all leaves <= 15)
        tests = small_mixed(r, 1500, 8, 13)
    else:                # seed 20: several large trees of different kinds summing to 2e5
        n1 = 50000; tests.append((n1, relabel(r, n1, random_tree(r, n1, 1))))
        n2 = 49999; tests.append((n2, relabel(r, n2, star(n2))))
        n3, e3 = spider([r.randint(1, 30) for _ in range(3001)]); tests.append((n3, relabel(r, n3, e3)))
        rest = MAXN - n1 - n2 - n3
        tests.append((rest, relabel(r, rest, random_tree(r, rest, 2))))
    return fmt(tests)


# ---------------------------------------------------------------- contract
def parse(text):
    tok = text.split(); p = 0
    t = int(tok[p]); p += 1
    tests = []
    for _ in range(t):
        n = int(tok[p]); p += 1
        e = []
        for _ in range(n - 1):
            e.append((int(tok[p]), int(tok[p + 1]))); p += 2
        tests.append((n, e))
    return tests, p == len(tok)


def valid(text):
    try:
        lines = text.split("\n")
        if lines[-1] != "":
            return False
        lines = lines[:-1]
        t = int(lines[0])
        if lines[0] != str(t) or not 1 <= t <= 10000:
            return False
        i = 1; total = 0
        for _ in range(t):
            n = int(lines[i]); i += 1
            if lines[i - 1] != str(n) or not 3 <= n <= MAXN:
                return False
            total += n
            par = list(range(n + 1))

            def find(x):
                while par[x] != x:
                    par[x] = par[par[x]]; x = par[x]
                return x
            for _ in range(n - 1):
                parts = lines[i].split(" "); i += 1
                if len(parts) != 2:
                    return False
                u, v = int(parts[0]), int(parts[1])
                if f"{u} {v}" != lines[i - 1] or not (1 <= u <= n and 1 <= v <= n and u != v):
                    return False
                a, b = find(u), find(v)
                if a == b:          # cycle or multi-edge -> not a tree
                    return False
                par[a] = b
        return i == len(lines) and total <= MAXN
    except (ValueError, IndexError):
        return False


# ---------------------------------------------------------------- oracle
def brute_one(n, e):
    adj = [[] for _ in range(n + 1)]
    for u, v in e:
        adj[u].append(v); adj[v].append(u)
    leaves = [v for v in range(1, n + 1) if len(adj[v]) <= 1]
    k = len(leaves)
    if k > ORACLE_K:
        return None
    dist = []
    for s in leaves:
        d = [-1] * (n + 1); d[s] = 0; q = deque([s])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if d[y] < 0:
                    d[y] = d[x] + 1; q.append(y)
        dist.append([d[l] for l in leaves])
    INF = float("inf")
    full = (1 << k) - 1
    f = [INF] * (1 << k)    # f[mask] = min cost to finish when `mask` leaves remain unchosen
    f[0] = 0
    for mask in range(1, full + 1):
        pc = bin(mask).count("1")
        i = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << i)
        best = f[rest] if pc & 1 else INF   # odd: leaf i is the one left unchosen
        m = rest
        while m:
            j = (m & -m).bit_length() - 1
            m ^= 1 << j
            c = dist[i][j] + f[rest ^ (1 << j)]
            if c < best:
                best = c
        f[mask] = best
    return f[full]


def oracle(text):
    tests, _ = parse(text)
    res = []
    for n, e in tests:
        a = brute_one(n, e)
        if a is None:
            return None
        res.append(a)
    return res


# ---------------------------------------------------------------- build
def build():
    out = HERE / "data"; out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 21):
        attempt = 0; case = generate(seed)
        while case in cases:
            attempt += 1; case = generate(seed, attempt)
        cases.append(case)
    checked = 0
    for idx, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {idx}: input contract violated")
        ans = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                             capture_output=True, check=True).stdout
        if idx == 0 and ans.split() != SAMPLE_OUT.split():
            raise SystemExit(f"sample mismatch: {ans!r}")
        o = oracle(case)
        if o is not None:
            if list(map(int, ans.split())) != o:
                raise SystemExit(f"case {idx}: oracle disagreement")
            checked += 1
        (out / f"{idx}.in").write_text(case, encoding="utf-8")
        (out / f"{idx}.out").write_text(ans, encoding="utf-8")
        print(f"case {idx}: in={len(case)}B out={len(ans)}B oracle={'yes' if o is not None else 'no'}")
    print(f"oracle-checked {checked}/21")


if __name__ == "__main__":
    build()
