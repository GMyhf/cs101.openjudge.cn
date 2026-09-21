#!/usr/bin/env python3
"""Codeforces 2195E Idiot First Search -- generator, input contract, oracle, build.

Written for this repository.  Run `python3 producecase.py` from this directory.

Input: t (1..1e4); each test: odd n (1..300001), then n lines `l r` (children of
vertex i, `0 0` for a leaf).  Vertex 0 is the parent of 1; every vertex 1..n has
0 or 2 children; sum n <= 300001.  Output: n values per test, mod 1e9+7.

Shapes (seed -> what it attacks):
  1  n=1 single test                         (smallest tree, only `0 0`)
  2  t=1e4 tiny trees n in {1,3,5,7}         (multi-test reset, reading all tests)
  3  many random trees n<=41, shuffled labels (label order != BFS order)
  4  left caterpillars n<=41                 (answers depend on left/right roles)
  5  right caterpillars n<=41
  6  zigzag / complete / broom mix n<=41
  7  all trees of every shape for n<=9 (every distinct shape, random labels)
  8  medium random tree n=2001, labels in DFS order
  9  medium left chain n=2001 (true values ~1e6, check exact arithmetic)
 10  complete binary tree n=65535
 11  left caterpillar n=90001, identity-ish labels (true values > 1e9+7: needs mod)
 12  right caterpillar n=90001, shuffled labels (deep: recursion depth 45000)
 13  zigzag chain n=90001
 14  broom: long chain ending in a complete tree n=90001
 15  random tree (random leaf expansion) n=90001
 16  "deep random" tree (expand the newest leaves mostly) n=90001
 17  many medium tests (t=90, n 801..1001) mixed shapes
 18  children listed with larger label on the left (l > r), deep random tree n=30001
 19  random small tests n<=61, t=150
 20  two big tests: chain + random, sum n ~ 90000
Output limit (<=1 MB) caps total n at ~90001 per file, below the statement's 300001;
chains of length 45000 already push true answers far past the modulus.

Oracle: literal step-by-step simulation of Bob with per-vertex marks, run for every
test whose n <= 61 (so whole files 0-7 and 19 are checked).
"""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

MOD = 1_000_000_007
REFERENCE = Path(__file__).with_name("samplecode.py")
SAMPLE = "3\n1\n0 0\n5\n2 3\n0 0\n4 5\n0 0\n0 0\n7\n2 3\n4 5\n0 0\n6 7\n0 0\n0 0\n0 0\n"
SAMPLE_OUT = "1\n9 10 14 15 15\n13 22 14 27 23 28 28\n"
ORACLE_MAX_N = 61


def shape_tree(r, n, mode):
    """Return children lists (local ids, root 0) for a full binary tree with n nodes."""
    ch = [None]
    leaves = [0]
    k = 0
    while len(ch) < n:
        if mode == "random":
            j = r.randrange(len(leaves)); v = leaves[j]; leaves[j] = leaves[-1]; leaves.pop()
        elif mode == "left":
            v = leaves.pop(-2) if len(leaves) >= 2 else leaves.pop()
        elif mode == "right":
            v = leaves.pop()
        elif mode == "zigzag":
            v = leaves.pop(-2 if (k % 2 == 0 and len(leaves) >= 2) else -1)
        elif mode == "complete":
            v = leaves.pop(0)
        elif mode == "deep":
            v = leaves.pop(-1 - (r.randrange(min(3, len(leaves)))))
        elif mode == "broom":
            if len(ch) < n // 2:
                v = leaves.pop()
            else:
                v = leaves.pop(0)
        else:
            raise ValueError(mode)
        a, b = len(ch), len(ch) + 1
        ch[v] = (a, b); ch.append(None); ch.append(None)
        leaves.append(a); leaves.append(b)
        k += 1
    # For "left" mode the expanded vertex is always the left one of the newest pair.
    return ch


def render(r, ch, labels="shuffle", swap=False):
    n = len(ch)
    if labels == "shuffle":
        perm = [1] + [x + 2 for x in r.sample(range(n - 1), n - 1)]
    elif labels == "dfs":
        perm = [0] * n; order = []; st = [0]
        while st:
            v = st.pop(); order.append(v)
            if ch[v]: st.append(ch[v][1]); st.append(ch[v][0])
        for i, v in enumerate(order): perm[v] = i + 1
    else:  # identity (BFS creation order)
        perm = [i + 1 for i in range(n)]
    rows = [None] * (n + 1)
    for v in range(n):
        if ch[v]:
            a, b = perm[ch[v][0]], perm[ch[v][1]]
            if swap and a < b: a, b = b, a
            rows[perm[v]] = f"{a} {b}"
        else:
            rows[perm[v]] = "0 0"
    return f"{n}\n" + "\n".join(rows[1:]) + "\n"


def all_shapes(n):
    if n == 1:
        return [[None]]
    res = []
    for ln in range(1, n - 1, 2):
        rn = n - 1 - ln
        for L in all_shapes(ln):
            for R in all_shapes(rn):
                ch = [(1, 1 + ln)]
                ch += [None if c is None else (c[0] + 1, c[1] + 1) for c in L]
                ch += [None if c is None else (c[0] + 1 + ln, c[1] + 1 + ln) for c in R]
                res.append(ch)
    return res


def tests_file(tests):
    return f"{len(tests)}\n" + "".join(tests)


def odd(r, lo, hi):
    return r.randrange(lo // 2, (hi - 1) // 2 + 1) * 2 + 1


def generate(seed):
    r = random.Random(2195_0005 * 1009 + seed)
    MODES_SMALL = ["random", "left", "right", "zigzag", "complete", "deep", "broom"]
    if seed == 1:
        return tests_file([render(r, [None])])
    if seed == 2:
        return tests_file([render(r, shape_tree(r, r.choice([1, 3, 5, 7]), r.choice(MODES_SMALL))) for _ in range(10000)])
    if seed == 3:
        return tests_file([render(r, shape_tree(r, odd(r, 1, 41), "random")) for _ in range(400)])
    if seed == 4:
        return tests_file([render(r, shape_tree(r, odd(r, 3, 41), "left")) for _ in range(300)])
    if seed == 5:
        return tests_file([render(r, shape_tree(r, odd(r, 3, 41), "right")) for _ in range(300)])
    if seed == 6:
        return tests_file([render(r, shape_tree(r, odd(r, 9, 41), r.choice(["zigzag", "complete", "broom", "deep"]))) for _ in range(300)])
    if seed == 7:
        tests = []
        for n in (1, 3, 5, 7, 9):
            for ch in all_shapes(n):
                tests.append(render(r, ch, r.choice(["shuffle", "identity", "dfs"])))
        return tests_file(tests)
    if seed == 8:
        return tests_file([render(r, shape_tree(r, 2001, "random"), "dfs")])
    if seed == 9:
        return tests_file([render(r, shape_tree(r, 2001, "left"), "identity")])
    if seed == 10:
        return tests_file([render(r, shape_tree(r, 65535, "complete"))])
    if seed == 11:
        return tests_file([render(r, shape_tree(r, 90001, "left"), "identity")])
    if seed == 12:
        return tests_file([render(r, shape_tree(r, 90001, "right"))])
    if seed == 13:
        return tests_file([render(r, shape_tree(r, 90001, "zigzag"), "dfs")])
    if seed == 14:
        return tests_file([render(r, shape_tree(r, 90001, "broom"))])
    if seed == 15:
        return tests_file([render(r, shape_tree(r, 90001, "random"))])
    if seed == 16:
        return tests_file([render(r, shape_tree(r, 90001, "deep"))])
    if seed == 17:
        return tests_file([render(r, shape_tree(r, odd(r, 801, 1001), r.choice(MODES_SMALL))) for _ in range(90)])
    if seed == 18:
        return tests_file([render(r, shape_tree(r, 30001, "deep"), "shuffle", swap=True)])
    if seed == 19:
        return tests_file([render(r, shape_tree(r, odd(r, 1, 61), r.choice(MODES_SMALL)), r.choice(["shuffle", "identity", "dfs"]), swap=r.random() < 0.3) for _ in range(150)])
    if seed == 20:
        return tests_file([render(r, shape_tree(r, 45001, "left"), "shuffle"),
                           render(r, shape_tree(r, 44999, "random"), "dfs")])
    # Extended range: random combinations for seeds 21+
    shape_modes = ["random", "left", "right", "zigzag", "complete", "deep", "broom"]
    label_modes = ["shuffle", "identity", "dfs"]
    tests = []
    for _ in range(r.randint(20, 80)):
        n = odd(r, 1, 2001)
        tests.append(render(r, shape_tree(r, n, r.choice(shape_modes)), r.choice(label_modes), swap=r.random() < 0.3))
    return tests_file(tests)


def parse(text):
    tok = text.split(); p = 1; tests = []
    for _ in range(int(tok[0])):
        n = int(tok[p]); p += 1
        L = [0] * (n + 1); R = [0] * (n + 1)
        for i in range(1, n + 1):
            L[i] = int(tok[p]); R[i] = int(tok[p + 1]); p += 2
        tests.append((n, L, R))
    return tests


def valid(text):
    if not text.endswith("\n"):
        return False
    lines = text.split("\n")[:-1]
    try:
        t = int(lines[0])
        if lines[0] != str(t) or not 1 <= t <= 10**4:
            return False
        ln = 1; total = 0
        for _ in range(t):
            n = int(lines[ln]); ln += 1
            if lines[ln - 1] != str(n) or not (1 <= n <= 300001 and n % 2 == 1):
                return False
            total += n
            parent = [-1] * (n + 1)
            L = [0] * (n + 1); R = [0] * (n + 1)
            for i in range(1, n + 1):
                parts = lines[ln].split(" "); ln += 1
                if len(parts) != 2 or any(x != str(int(x)) for x in parts):
                    return False
                a, b = int(parts[0]), int(parts[1])
                if not (0 <= a <= n and 0 <= b <= n):
                    return False
                if (a == 0) != (b == 0):
                    return False
                if a:
                    if a == b or a == 1 or b == 1 or parent[a] != -1 or parent[b] != -1:
                        return False
                    parent[a] = i; parent[b] = i
                L[i], R[i] = a, b
            # every vertex except 1 has exactly one parent and is reachable from 1
            if any(parent[v] == -1 for v in range(2, n + 1)):
                return False
            seen = [False] * (n + 1); st = [1]; seen[1] = True; cnt = 1
            while st:
                v = st.pop()
                for c in (L[v], R[v]):
                    if c and not seen[c]:
                        seen[c] = True; cnt += 1; st.append(c)
            if cnt != n:
                return False
        return ln == len(lines) and total <= 300001
    except (ValueError, IndexError):
        return False


def simulate(n, L, R, k):
    par = [0] * (n + 1)
    for i in range(1, n + 1):
        if L[i]: par[L[i]] = i; par[R[i]] = i
    mark = [0] * (n + 1)  # 0 none, 1 'L', 2 'R'
    v = k; steps = 0
    while v != 0:
        if L[v] == 0:
            v = par[v]
        elif mark[v] == 0:
            mark[v] = 1; v = L[v]
        elif mark[v] == 1:
            mark[v] = 2; v = R[v]
        else:
            mark[v] = 0; v = par[v]
        steps += 1
    return steps


def oracle_lines(text):
    """Per test: expected line if n is small enough to simulate, else None."""
    res = []
    for n, L, R in parse(text):
        if n > ORACLE_MAX_N:
            res.append(None)
        else:
            res.append(" ".join(str(simulate(n, L, R, k) % MOD) for k in range(1, n + 1)))
    return res


def build():
    out = Path(__file__).with_name("data"); out.mkdir(exist_ok=True)
    for f in out.glob("*"): f.unlink()
    cases = [SAMPLE] + [generate(seed) for seed in range(1, 40)]
    if len(set(cases)) != len(cases):
        raise SystemExit("duplicate inputs")
    full = 0
    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {index} violates the input contract")
        ans = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                             capture_output=True, check=True, timeout=120).stdout
        if index == 0 and ans.split() != SAMPLE_OUT.split():
            raise SystemExit(f"sample mismatch: {ans!r}")
        got = ans.split("\n")[:-1]
        exp = oracle_lines(case)
        if len(got) != len(exp):
            raise SystemExit(f"case {index}: wrong number of output lines")
        checked = 0
        for g, e in zip(got, exp):
            if e is not None:
                checked += 1
                if g != e:
                    raise SystemExit(f"case {index}: oracle disagreement")
        if checked == len(exp):
            full += 1
        print(f"case {index}: {checked}/{len(exp)} tests oracle-checked", file=sys.stderr)
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(ans, encoding="utf-8")
    print(f"{full} files fully oracle-checked", file=sys.stderr)


if __name__ == "__main__":
    build()
