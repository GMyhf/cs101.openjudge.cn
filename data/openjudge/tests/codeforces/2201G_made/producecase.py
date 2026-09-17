#!/usr/bin/env python3
"""Codeforces 2201G Codeforces Heuristic Contest 1001 -- inputs, contract, oracle, build.

Written for this repository as a hand-off artifact; no external license.

The statement allows exactly two inputs ("n in {5, 1001}", "There are only two
input files for this problem"), so the data is the whole input domain: case 0 is
the official sample n = 5, case 1 is n = 1001.  Twenty cases are impossible
without inventing inputs the statement forbids.

Judged by checker.py (any induced cycle with >= floor(n^2/e) vertices).
Build-time verification:
  * valid(): input is exactly "5\\n" or "1001\\n";
  * n = 5: every simple cycle of the 5x5 Zebra Graph is enumerated by DFS; the
    induced ones with >= 9 vertices are listed (there is exactly one, the official
    sample output), the reference must print one of them, and the checker must
    accept the official output and reject all other induced cycles / near misses;
  * n = 1001: an independent verifier (union-find over all edges, not the
    checker's bitset + walk) confirms the reference output is one induced cycle
    of >= floor(n^2/e) vertices (threshold from exact rational bounds on e);
  * the checker accepts the reference and its 7 images under the symmetries of
    the grid (transpose / row flip / column flip), and rejects the output with one
    vertex added or removed;
  * build aborts on any disagreement.  Reference: samplecode.cpp (g++ -O2).
"""
from __future__ import annotations
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.cpp"
CHECKER = HERE / "checker.py"
SAMPLE = "5\n"
SAMPLE_OUT = "01110\n11011\n10001\n11011\n01110\n"
CASES = [SAMPLE, "1001\n"]
MOVES = [(2, 3), (3, 2), (-2, 3), (-3, 2), (2, -3), (3, -2), (-2, -3), (-3, -2)]
E_LOW = Fraction(27182818284590452353, 10 ** 19)      # e lies strictly between these
E_HIGH = Fraction(27182818284590452354, 10 ** 19)


def valid(text):
    return text in ("5\n", "1001\n")


def threshold(n):
    lo, hi = int(Fraction(n * n) / E_HIGH), int(Fraction(n * n) / E_LOW)
    assert lo == hi, "floor(n^2/e) not determined by the bounds"
    return lo


def check(inp, out):
    with tempfile.TemporaryDirectory() as d:
        pi, po = Path(d, "in"), Path(d, "out")
        pi.write_text(inp); po.write_text(out)
        r = subprocess.run([sys.executable, "-I", str(CHECKER), str(pi), str(po), str(po)],
                           capture_output=True, text=True)
    if r.returncode not in (0, 42):
        raise SystemExit(f"checker crashed: {r.returncode} {r.stderr[-500:]}")
    return r.returncode == 0


def grid_text(n, cells):
    rows = [["0"] * n for _ in range(n)]
    for r, c in cells:
        rows[r][c] = "1"
    return "".join("".join(row) + "\n" for row in rows)


def cells_of(text):
    return {(r, c) for r, line in enumerate(text.split()) for c, ch in enumerate(line) if ch == "1"}


def independent_verdict(n, text):
    """Union-find over all edges inside S; S must be 2-regular and connected."""
    lines = text.split()
    if len(lines) != n or any(len(s) != n or set(s) - {"0", "1"} for s in lines):
        return False
    S = cells_of(text)
    if len(S) < threshold(n):
        return False
    index = {p: i for i, p in enumerate(sorted(S))}
    parent = list(range(len(S)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for (r, c), i in index.items():
        deg = 0
        for dr, dc in MOVES:
            j = index.get((r + dr, c + dc))
            if j is not None:
                deg += 1
                a, b = find(i), find(j)
                if a != b:
                    parent[a] = b
        if deg != 2:
            return False
    return len({find(i) for i in range(len(S))}) == 1


def all_induced_cycles_5():
    n = 5
    verts = [(r, c) for r in range(n) for c in range(n)]
    adj = {v: [(v[0] + a, v[1] + b) for a, b in MOVES if 0 <= v[0] + a < n and 0 <= v[1] + b < n] for v in verts}
    found = set()
    for start in verts:                       # cycles whose smallest vertex is start
        stack = [(start, [start])]
        while stack:
            v, path = stack.pop()
            for w in adj[v]:
                if w == start and len(path) >= 3:
                    cyc = frozenset(path)
                    if all(sum(1 for x in adj[u] if x in cyc) == 2 for u in cyc):
                        found.add(cyc)
                elif w > start and w not in path:
                    stack.append((w, path + [w]))
    return [c for c in found if len(c) >= threshold(5)]


def symmetries(n, text):
    S = cells_of(text)
    maps = [lambda r, c: (c, r), lambda r, c: (n - 1 - r, c), lambda r, c: (r, n - 1 - c),
            lambda r, c: (n - 1 - r, n - 1 - c), lambda r, c: (c, n - 1 - r),
            lambda r, c: (n - 1 - c, r), lambda r, c: (n - 1 - c, n - 1 - r)]
    return [grid_text(n, {f(r, c) for r, c in S}) for f in maps]


def build():
    out = HERE / "data"; out.mkdir(exist_ok=True)
    cycles5 = all_induced_cycles_5()
    if [grid_text(5, c) for c in cycles5] != [SAMPLE_OUT]:
        raise SystemExit(f"n=5 oracle: expected the official output to be the only answer, got {len(cycles5)}")
    if not check(SAMPLE, SAMPLE_OUT):
        raise SystemExit("checker rejects the official sample output")
    with tempfile.TemporaryDirectory() as d:
        exe = Path(d, "ref")
        subprocess.run(["g++", "-O2", "-o", str(exe), str(REFERENCE)], check=True)
        for idx, case in enumerate(CASES):
            if not valid(case):
                raise SystemExit(f"case {idx}: input contract violated")
            n = int(case)
            ans = subprocess.run([str(exe)], input=case, text=True, capture_output=True, check=True).stdout
            if not independent_verdict(n, ans):
                raise SystemExit(f"case {idx}: independent verifier rejects the reference")
            if not check(case, ans):
                raise SystemExit(f"case {idx}: checker rejects the reference")
            if n == 5 and ans != SAMPLE_OUT:
                raise SystemExit("n=5: reference differs from the unique answer")
            for k, alt in enumerate(symmetries(n, ans)):
                if independent_verdict(n, alt) != check(case, alt) or not check(case, alt):
                    raise SystemExit(f"case {idx}: symmetry image {k} judged wrongly")
            S = sorted(cells_of(ans))
            removed = grid_text(n, set(S[1:]))
            added = grid_text(n, set(S) | {next((r, c) for r in range(n) for c in range(n) if (r, c) not in set(S))})
            for bad in (removed, added):
                if check(case, bad) or independent_verdict(n, bad):
                    raise SystemExit(f"case {idx}: a broken answer was accepted")
            if n == 5:
                for c in range(5):              # every single-cell change of the unique answer
                    for r in range(5):
                        cells = set(S) ^ {(r, c)}
                        if check(case, grid_text(5, cells)):
                            raise SystemExit("n=5: checker accepts a non-answer")
            (out / f"{idx}.in").write_text(case, encoding="utf-8")
            (out / f"{idx}.out").write_text(ans, encoding="utf-8")
            print(f"case {idx}: n={n} |S|={len(S)} need>={threshold(n)} in={len(case)}B out={len(ans)}B")


if __name__ == "__main__":
    build()
