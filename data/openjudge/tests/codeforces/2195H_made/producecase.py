#!/usr/bin/env python3
"""Codeforces 2195H Codeforces Heuristic Contest 001 -- generator, contract, oracle, build.

Written for this repository as a hand-off artifact; no external license.

Answers are not unique, so the problem is judged by checker.py (next to data/), which
takes the optimum as 2 for n = 1 and 3n^2 for n >= 2.  The oracle below backs that up
without sharing code with the checker:
  * n = 1: exhaustive search over all unit-area triangles of the 3x3 grid with an exact
    closed-triangle intersection test -- 2 disjoint ones exist, 3 do not;
  * n >= 2: 3n^2 is the pigeonhole bound (9n^2 points, 3 per triangle) and the reference
    output reaches it; every reference output is verified by the same exact
    closed-triangle test on all pairs whose bounding boxes meet;
  * the checker's strip algorithm is cross-checked against that brute force on every
    pair of unit triangles in the 3x3 grid and on thousands of random local re-partitions
    (intersecting and not) of reference outputs for n = 2..4.

Size note: an optimal answer has 3n^2 lines of ~22 bytes; n = 166 is ~1.9 MB, right at
the judge's 2 MB contestant-output cap, and this repository caps .out at 1 MB.  Tests
therefore keep sum(3n^2 lines) under ~1 MB: the largest single n is 117 (odd, uses the
9x9 corner packing) and 116 (even).  The construction is uniform in n, so nothing about
correctness changes between 117 and 166.

Shapes target the ways solutions go wrong: n = 1 (answer 2, not 3), n = 2 (smallest
perfect), n = 3 (smallest odd perfect: 2x3 tiling alone leaves points), all n in 1..30
in one file, 30 copies of n = 1 (per-test resets), odd and even large n, n = 1 after a
large test, mixtures up to t = 30.
Case 0 is the official sample; the checker must accept the official output as well.
"""
from __future__ import annotations
import contextlib
import io
import itertools
import random
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
CHECKER = HERE / "checker.py"
SAMPLE = "2\n1\n2\n"
SAMPLE_OUT = """2
1 1 1 2 2 1
2 3 3 2 3 3
12
1 1 1 2 2 1
2 2 3 2 3 1
1 3 1 4 2 3
2 4 3 4 3 3
1 5 1 6 2 5
2 6 3 6 3 5
4 1 4 2 5 1
5 2 6 2 6 1
4 3 4 4 5 3
5 4 6 4 6 3
4 5 4 6 5 5
5 6 6 6 6 5
"""
MAXN = 166
MAXT = 30
MAXSQ = 166 * 166
BRUTE_N = MAXN


def fmt(ns):
    return f"{len(ns)}\n" + "".join(f"{n}\n" for n in ns)


def generate(seed):
    r = random.Random(2195_0008 * 131 + seed)
    if seed == 1:
        ns = [1]
    elif seed == 2:
        ns = [2]
    elif seed == 3:
        ns = [3]
    elif seed == 4:
        ns = list(range(1, 31)); r.shuffle(ns)
    elif seed == 5:
        ns = [1] * 30
    elif seed == 6:
        ns = [117]
    elif seed == 7:
        ns = [116]
    elif seed == 8:
        ns = [r.choice([1, 2, 3]) for _ in range(30)]
    elif seed == 9:
        ns = [5, 7, 9]
    elif seed == 10:
        ns = [4, 6, 8, 10, 12]
    elif seed == 11:
        ns = []
        while len(ns) < 30:
            ns.append(r.randint(1, 25))
    elif seed == 12:
        ns = [100, 1]
    elif seed == 13:
        ns = [99]
    elif seed == 14:
        ns = [50, 51, 52]
    elif seed == 15:
        ns = [1, 83, 84]
    elif seed == 16:
        ns = [11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39]
    elif seed == 17:
        ns = [20] * 30
    elif seed == 18:
        ns = [65, 66, 67]
    elif seed == 19:
        ns = []
        sq = 0
        while len(ns) < 30:
            n = r.randint(1, 60)
            if sq + n * n > 14000:
                break
            ns.append(n); sq += n * n
    elif seed == 20:
        ns = [111]
    else:
        mode = (seed - 21) % 5
        if mode == 0:
            ns = [r.randint(1, 30) for _ in range(r.randint(5, 25))]
        elif mode == 1:
            ns = [r.randint(1, 50) for _ in range(r.randint(3, 15))]
        elif mode == 2:
            ns = []
            sq = 0
            while len(ns) < r.randint(10, 28):
                n = r.randint(1, 50)
                if sq + n * n > MAXSQ:
                    break
                ns.append(n); sq += n * n
        elif mode == 3:
            ns = [r.randint(20, 60) for _ in range(r.randint(3, 8))]
        else:
            ns = [r.randint(1, 20) for _ in range(r.randint(15, 30))]
        while sum(n * n for n in ns) > MAXSQ:
            ns.pop()
    assert 1 <= len(ns) <= MAXT and sum(n * n for n in ns) <= MAXSQ
    return fmt(ns)


# ---------------------------------------------------------------- contract
def valid(text):
    try:
        lines = text.split("\n")
        if lines[-1] != "":
            return False
        lines = lines[:-1]
        t = int(lines[0])
        if lines[0] != str(t) or not 1 <= t <= MAXT or len(lines) != t + 1:
            return False
        sq = 0
        for line in lines[1:]:
            n = int(line)
            if line != str(n) or not 1 <= n <= MAXN:
                return False
            sq += n * n
        return sq <= MAXSQ
    except (ValueError, IndexError):
        return False


# ---------------------------------------------------------------- brute force geometry
def orient(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)


def on_seg(a, b, p):
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def seg_meet(p1, p2, p3, p4):
    """closed segments intersect (touching and collinear overlap included)"""
    d1, d2 = orient(p3, p4, p1), orient(p3, p4, p2)
    d3, d4 = orient(p1, p2, p3), orient(p1, p2, p4)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    return ((d1 == 0 and on_seg(p3, p4, p1)) or (d2 == 0 and on_seg(p3, p4, p2)) or
            (d3 == 0 and on_seg(p1, p2, p3)) or (d4 == 0 and on_seg(p1, p2, p4)))


def in_tri(t, p):
    o = [orient(t[i], t[(i + 1) % 3], p) for i in range(3)]
    return not (min(o) < 0 < max(o))


def tri_meet(a, b):
    """closed triangles (non-degenerate) intersect"""
    for i in range(3):
        for j in range(3):
            if seg_meet(a[i], a[(i + 1) % 3], b[j], b[(j + 1) % 3]):
                return True
    return in_tri(a, b[0]) or in_tri(b, a[0])


def brute_valid(n, tris):
    """exact: coordinates in range, area 1/2, pairwise disjoint closed triangles"""
    s = 3 * n
    for t in tris:
        if any(not (1 <= c <= s) for p in t for c in p):
            return False
        if abs((t[1][0] - t[0][0]) * (t[2][1] - t[0][1]) - (t[1][1] - t[0][1]) * (t[2][0] - t[0][0])) != 1:
            return False
    # bucket by the lattice points of each bounding box: two closed integer boxes that
    # meet always share a lattice point, so every candidate pair meets in some bucket
    buckets = {}
    for i, t in enumerate(tris):
        xs = [p[0] for p in t]; ys = [p[1] for p in t]
        for x in range(min(xs), max(xs) + 1):
            for y in range(min(ys), max(ys) + 1):
                buckets.setdefault((x, y), []).append(i)
    seen = set()
    for lst in buckets.values():
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)):
                key = (lst[a], lst[b])
                if key in seen:
                    continue
                seen.add(key)
                if tri_meet(tris[lst[a]], tris[lst[b]]):
                    return False
    return True


def unit_tris(s):
    pts = [(x, y) for x in range(1, s + 1) for y in range(1, s + 1)]
    return [T for T in itertools.combinations(pts, 3)
            if abs((T[1][0] - T[0][0]) * (T[2][1] - T[0][1]) - (T[1][1] - T[0][1]) * (T[2][0] - T[0][0])) == 1]


def oracle_n1():
    tris = unit_tris(3)
    two = any(not tri_meet(a, b) for a, b in itertools.combinations(tris, 2))
    three = any(not tri_meet(a, b) and not tri_meet(a, c) and not tri_meet(b, c)
                for a, b, c in itertools.combinations(tris, 3))
    if not two or three:
        raise SystemExit("oracle: n = 1 optimum is not 2")


def parse_out(text, ns):
    tok = text.split(); p = 0; res = []
    for n in ns:
        m = int(tok[p]); p += 1
        tris = []
        for _ in range(m):
            v = list(map(int, tok[p:p + 6])); p += 6
            tris.append(((v[0], v[1]), (v[2], v[3]), (v[4], v[5])))
        res.append(tris)
    return res


def oracle(case, ans):
    ns = list(map(int, case.split()[1:]))
    outs = parse_out(ans, ns)
    covered = True
    for n, tris in zip(ns, outs):
        best = 2 if n == 1 else 3 * n * n
        if len(tris) != best or 3 * best > 9 * n * n:
            raise SystemExit(f"oracle: n = {n} reference size {len(tris)} != {best}")
        if n <= BRUTE_N:
            if not brute_valid(n, tris) or len({p for t in tris for p in t}) != 3 * len(tris):
                raise SystemExit(f"oracle: reference output for n = {n} is not a valid packing")
        else:
            covered = False
    return covered


# ---------------------------------------------------------------- checker self-test
def load_checker():
    src = CHECKER.read_text()
    head, tail = src.rsplit("main()", 1)
    assert tail.strip() == ""
    env = {"__name__": "checker_selftest"}
    exec(compile(head, str(CHECKER), "exec"), env)
    return env["check_test"]


def checker_says(check_test, n, tris):
    toks = [str(len(tris)).encode()] + [str(c).encode() for t in tris for p in t for c in p]
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            check_test(1, n, toks, 0, len(toks))
            return True
        except SystemExit as e:
            if e.code != 42:
                raise
            return False


def selftest(ref_outputs):
    check_test = load_checker()
    stats = {"agree_ok": 0, "agree_bad": 0}

    def compare(n, tris):
        distinct = len({p for t in tris for p in t}) == 3 * len(tris)
        want = distinct and brute_valid(n, tris)
        got = checker_says(check_test, n, tris)
        if got != want:
            raise SystemExit(f"checker disagrees with brute force (n={n}): {tris}")
        stats["agree_ok" if want else "agree_bad"] += 1

    # every pair of unit triangles of the 3x3 grid
    for a, b in itertools.combinations(unit_tris(3), 2):
        compare(1, [a, b])
    r = random.Random(21950008)
    for n, tris in ref_outputs:
        s = 3 * n
        for _ in range(1500):
            w, h = r.choice([(3, 3), (4, 3), (3, 4), (4, 4), (5, 3)])
            x0 = r.randint(1, s - w + 1); y0 = r.randint(1, s - h + 1)
            inside = [t for t in tris if all(x0 <= p[0] < x0 + w and y0 <= p[1] < y0 + h for p in t)]
            if len(inside) < 2:
                continue
            k = r.randint(2, min(4, len(inside)))
            pick = r.sample(inside, k)
            pts = [p for t in pick for p in t]
            for _ in range(200):
                r.shuffle(pts)
                new = [tuple(pts[i:i + 3]) for i in range(0, len(pts), 3)]
                if all(abs((t[1][0] - t[0][0]) * (t[2][1] - t[0][1]) - (t[1][1] - t[0][1]) * (t[2][0] - t[0][0])) == 1
                       for t in new):
                    break
            else:
                continue
            rest = [t for t in tris if t not in pick]
            compare(n, rest + new)
    if stats["agree_bad"] < 100 or stats["agree_ok"] < 100:
        raise SystemExit(f"self-test did not exercise both verdicts: {stats}")
    return stats


def run_checker(inp, out):
    with tempfile.TemporaryDirectory() as d:
        paths = []
        for name, data in (("in", inp), ("out", out), ("ans", out)):
            p = Path(d) / name; p.write_text(data); paths.append(str(p))
        res = subprocess.run([sys.executable, "-I", str(CHECKER), *paths], capture_output=True, text=True)
    return res.returncode, res.stdout.strip()


# ---------------------------------------------------------------- build
def build():
    out = HERE / "data"; out.mkdir(exist_ok=True)
    oracle_n1()
    cases = [SAMPLE]
    for seed in range(1, 40):
        case = generate(seed)
        assert case not in cases, seed
        cases.append(case)
    code, msg = run_checker(SAMPLE, SAMPLE_OUT)
    if code != 0:
        raise SystemExit(f"checker rejects the official sample output: {msg}")
    checked = 0
    small_refs = {}
    for idx, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {idx}: input contract violated")
        ans = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                             capture_output=True, check=True).stdout
        code, msg = run_checker(case, ans)
        if code != 0:
            raise SystemExit(f"case {idx}: checker rejects the reference ({code}): {msg}")
        if idx == 0 and [ln for ln in ans.split("\n") if len(ln.split()) == 1] != ["2", "12"]:
            raise SystemExit("sample sizes mismatch")
        full = oracle(case, ans)
        checked += full
        ns = list(map(int, case.split()[1:]))
        for n, tris in zip(ns, parse_out(ans, ns)):
            if 2 <= n <= 4:
                small_refs.setdefault(n, tris)
        if len(case) > 3 << 20 or len(ans) > 1 << 20:
            raise SystemExit(f"case {idx}: too large ({len(case)}, {len(ans)})")
        (out / f"{idx}.in").write_text(case, encoding="utf-8")
        (out / f"{idx}.out").write_text(ans, encoding="utf-8")
        print(f"case {idx}: in={len(case)}B out={len(ans)}B brute-verified={'all' if full else 'n<=%d' % BRUTE_N}")
    stats = selftest(sorted(small_refs.items()))
    print(f"brute-verified every test in {checked}/21 cases; checker self-test {stats}")


if __name__ == "__main__":
    build()
