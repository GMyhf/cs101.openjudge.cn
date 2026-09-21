#!/usr/bin/env python3
"""Codeforces 2171F Rae Taylor and Trees (hard version) -- generator, contract, oracle, build.

Written for this repository as a hand-off artifact; no external license.

Answers are not unique, so the problem is judged by checker.py (next to data/).
The checker decides existence with the prefix-min / suffix-max criterion; the oracle
below decides it independently by BFS over the explicit O(n^2) edge set
{u < v, pos(u) < pos(v)} on every test of a case whose sum of n^2 is small, and its
decision must equal the reference's Yes/No (the reference itself must pass the checker).

Size note: a Yes answer prints n-1 edge lines (~12-14 bytes each).  This repository caps
.out at 1 MB and the judge caps contestant output at 2 MB, so a Yes test with n = 2e5
(~2.7 MB of edges) cannot be judged here at all.  Yes tests therefore total at most
YES_BUDGET vertices per file; No tests (one-word answers) still go up to n = 2e5.

Shapes target the ways solutions go wrong:
  * every permutation of n = 2..6 (exhaustive decisions), t = 1e4 tiny tests;
  * No instances made of value-decreasing blocks (blocks shuffled inside), with a cut at
    the very start (p_1 = n) or very end (p_n = 1), many tiny blocks, zigzags;
  * "barely Yes": the same block structure with one transposition so that exactly one
    allowed edge crosses a split -- greedy edge choices that skip it build a forest;
  * deep component stacks: n-1, n-2, ..., 1, n and descending-then-ascending;
  * star-like identity, random permutations, mixed multi-test files.
Case 0 is the official sample; the checker must accept the official output as well.
"""
from __future__ import annotations
import random
import subprocess
import sys
import tempfile
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
CHECKER = HERE / "checker.py"
SAMPLE = """9
6
1 3 4 5 2 6
4
3 4 1 2
5
4 3 5 1 2
4
1 2 3 4
7
4 3 5 7 6 2 1
6
2 4 6 1 3 5
3
2 1 3
4
2 4 1 3
6
4 2 6 5 1 3
"""
SAMPLE_OUT = """Yes
3 1
4 1
6 5
6 2
6 1
No
No
Yes
2 1
4 3
4 1
No
Yes
4 2
6 2
3 1
5 1
5 2
Yes
3 2
3 1
Yes
4 2
3 1
3 2
Yes
6 4
6 2
3 1
5 4
2 3
"""
SAMPLE_DECISIONS = ["Yes", "No", "No", "Yes", "No", "Yes", "Yes", "Yes", "Yes"]
MAXN = 200000
MAXT = 10000
YES_BUDGET = 80000
ORACLE_SQ = 4_100_000


def exists(p):
    mn = len(p) + 1
    suf = [0] * (len(p) + 1)
    for i in range(len(p) - 1, -1, -1):
        suf[i] = max(suf[i + 1], p[i])
    for k in range(len(p) - 1):
        mn = min(mn, p[k])
        if mn > suf[k + 1]:
            return False
    return True


def blocks_perm(r, n, sizes):
    """value-decreasing blocks: first block holds the largest values; shuffled inside."""
    p = []; hi = n
    for s in sizes:
        blk = list(range(hi - s + 1, hi + 1)); r.shuffle(blk); p += blk; hi -= s
    assert hi == 0
    return p


def random_sizes(r, n, lo, hi):
    sizes = []; left = n
    while left:
        s = min(left, r.randint(lo, hi)); sizes.append(s); left -= s
    return sizes


def barely_yes(r, n):
    """two blocks (high then low) where exactly one allowed edge crosses the split."""
    k = r.randint(1, n - 1)
    high = list(range(k + 1, n + 1)); low = list(range(1, k + 1))
    r.shuffle(high); r.shuffle(low)
    # put k into the prefix and k+1 into the suffix
    i = high.index(k + 1); j = low.index(k)
    high[i], low[j] = low[j], high[i]
    return high + low


def one_swap(r, p):
    q = list(p)
    i, j = r.randrange(len(q)), r.randrange(len(q))
    q[i], q[j] = q[j], q[i]
    return q


def fmt(tests):
    out = [str(len(tests))]
    for p in tests:
        out.append(str(len(p))); out.append(" ".join(map(str, p)))
    return "\n".join(out) + "\n"


def small_mixed(r, count, lo, hi):
    tests = []
    for _ in range(count):
        n = r.randint(lo, hi)
        kind = r.randrange(5)
        if kind == 0:
            p = list(range(1, n + 1)); r.shuffle(p)
        elif kind == 1:
            p = blocks_perm(r, n, random_sizes(r, n, 1, max(1, n // 2)))
        elif kind == 2:
            p = one_swap(r, blocks_perm(r, n, random_sizes(r, n, 1, 3)))
        elif kind == 3:
            p = barely_yes(r, n)
        else:
            p = list(range(n, 0, -1))
            if r.random() < 0.5:
                p = one_swap(r, p)
        tests.append(p)
    return tests


def generate(seed):
    r = random.Random(2171_0006 * 131 + seed)
    tests = []
    if seed == 1:        # every permutation of n = 2..6
        import itertools
        for n in range(2, 7):
            tests += [list(q) for q in itertools.permutations(range(1, n + 1))]
        r.shuffle(tests)
    elif seed == 2:      # t = 1e4 random tiny permutations
        for _ in range(MAXT):
            n = r.randint(2, 8); p = list(range(1, n + 1)); r.shuffle(p); tests.append(p)
    elif seed == 3:      # tiny structured Yes/No
        tests = [[1, 2], [2, 1]] + small_mixed(r, 3000, 2, 30)
    elif seed == 4:      # max n, fully reversed (No)
        tests = [list(range(MAXN, 0, -1))]
    elif seed == 5:      # identity, star from 1
        tests = [list(range(1, YES_BUDGET + 1))]
    elif seed == 6:      # n-1, ..., 1, n: stack depth n-1 collapses at the end
        n = YES_BUDGET
        tests = [list(range(n - 1, 0, -1)) + [n]]
    elif seed == 7:      # max n No, value-decreasing random blocks
        tests = [blocks_perm(r, MAXN, random_sizes(r, MAXN, 1, 40000))]
    elif seed == 8:      # random permutation Yes
        p = list(range(1, YES_BUDGET + 1)); r.shuffle(p); tests = [p]
    elif seed == 9:      # a single cut at the very start / very end
        n = MAXN // 2
        a = list(range(1, n)); r.shuffle(a); tests.append([n] + a)
        b = list(range(2, n + 1)); r.shuffle(b); tests.append(b + [1])
    elif seed == 10:     # near-No medium tests with one transposition (oracle)
        for _ in range(300):
            n = r.randint(20, 90)
            tests.append(one_swap(r, blocks_perm(r, n, random_sizes(r, n, 1, 12))))
    elif seed == 11:     # medium block structures, both answers (oracle)
        tests = small_mixed(r, 700, 30, 60)
    elif seed == 12:     # t = 1e4, n = 20, mostly structured
        tests = small_mixed(r, MAXT, 20, 20)
        yes = 0
        for i, p in enumerate(tests):
            if exists(p):
                yes += 1
                if yes * 20 > YES_BUDGET:
                    tests[i] = list(range(20, 0, -1))
    elif seed == 13:     # descending then ascending
        h = YES_BUDGET // 2; n = YES_BUDGET
        tests = [list(range(h, 0, -1)) + list(range(h + 1, n + 1))]
    elif seed == 14:     # zigzag pairs: No at 120000, Yes (1 moved first) at 80000
        n = 120000
        z = []
        for k in range(n // 2, 0, -1):
            z += [2 * k - 1, 2 * k]
        tests.append(z)
        n = YES_BUDGET
        z = []
        for k in range(n // 2, 0, -1):
            z += [2 * k - 1, 2 * k]
        z.remove(1); tests.append([1] + z)
    elif seed == 15:     # max n No with tiny blocks
        tests = [blocks_perm(r, MAXN, random_sizes(r, MAXN, 1, 5))]
    elif seed == 16:     # barely Yes, large
        tests = [barely_yes(r, YES_BUDGET)]
        while not exists(tests[0]):
            tests = [barely_yes(r, YES_BUDGET)]
    elif seed == 17:     # many medium random permutations (mostly Yes)
        used = 0
        while True:
            n = r.randint(100, 2000)
            if used + n > YES_BUDGET:
                break
            p = list(range(1, n + 1)); r.shuffle(p); tests.append(p); used += n
    elif seed == 18:     # many No blocks up to max sum, a few barely-Yes
        used = 0; yes = 0
        while used < MAXN and len(tests) < MAXT:
            n = min(r.randint(2, 5000), MAXN - used)
            if n < 2:
                break
            if r.random() < 0.3 and yes + n <= YES_BUDGET:
                p = barely_yes(r, n)
            else:
                p = blocks_perm(r, n, random_sizes(r, n, 1, max(1, n // 3)))
            if exists(p):
                if yes + n > YES_BUDGET:
                    p = list(range(n, 0, -1))
                else:
                    yes += n
            tests.append(p); used += n
    elif seed == 19:     # t = 1e4, n = 2
        tests = [r.choice([[1, 2], [2, 1]]) for _ in range(MAXT)]
    else:                # seed 20: mixed small shapes (oracle)
        tests = small_mixed(r, 2500, 2, 40)
    total = sum(len(p) for p in tests)
    yes = sum(len(p) for p in tests if exists(p))
    assert 1 <= len(tests) <= MAXT and total <= MAXN and yes <= YES_BUDGET, (seed, total, yes)
    return fmt(tests)


# ---------------------------------------------------------------- contract
def valid(text):
    try:
        lines = text.split("\n")
        if lines[-1] != "":
            return False
        lines = lines[:-1]
        t = int(lines[0])
        if lines[0] != str(t) or not 1 <= t <= MAXT or len(lines) != 2 * t + 1:
            return False
        total = 0
        for k in range(t):
            n = int(lines[1 + 2 * k])
            if lines[1 + 2 * k] != str(n) or not 2 <= n <= MAXN:
                return False
            p = [int(x) for x in lines[2 + 2 * k].split(" ")]
            if " ".join(map(str, p)) != lines[2 + 2 * k] or len(p) != n or sorted(p) != list(range(1, n + 1)):
                return False
            total += n
        return total <= MAXN
    except (ValueError, IndexError):
        return False


def parse(text):
    tok = text.split(); t = int(tok[0]); q = 1; tests = []
    for _ in range(t):
        n = int(tok[q]); q += 1
        tests.append([int(x) for x in tok[q:q + n]]); q += n
    return tests


# ---------------------------------------------------------------- oracle
def brute_exists(p):
    n = len(p)
    pos = [0] * (n + 1)
    for i, v in enumerate(p):
        pos[v] = i
    seen = [False] * (n + 1); seen[1] = True; dq = deque([1]); cnt = 1
    while dq:
        u = dq.popleft()
        for v in range(1, n + 1):
            if not seen[v] and (u - v) * (pos[u] - pos[v]) > 0:
                seen[v] = True; cnt += 1; dq.append(v)
    return cnt == n


def oracle(text):
    tests = parse(text)
    if sum(len(p) ** 2 for p in tests) > ORACLE_SQ:
        return None
    return ["Yes" if brute_exists(p) else "No" for p in tests]


def run_checker(inp, out):
    with tempfile.TemporaryDirectory() as d:
        paths = []
        for name, data in (("in", inp), ("out", out), ("ans", out)):
            p = Path(d) / name; p.write_text(data); paths.append(str(p))
        res = subprocess.run([sys.executable, "-I", str(CHECKER), *paths], capture_output=True, text=True)
    return res.returncode, res.stdout.strip()


def decisions(ans):
    return [w for w in ans.split() if w in ("Yes", "No")]


# ---------------------------------------------------------------- build
def build():
    out = HERE / "data"; out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 40):
        case = generate(seed)
        assert case not in cases, seed
        cases.append(case)
    code, msg = run_checker(SAMPLE, SAMPLE_OUT)
    if code != 0:
        raise SystemExit(f"checker rejects the official sample output: {msg}")
    checked = 0
    for idx, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {idx}: input contract violated")
        ans = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                             capture_output=True, check=True).stdout
        code, msg = run_checker(case, ans)
        if code != 0:
            raise SystemExit(f"case {idx}: checker rejects the reference ({code}): {msg}")
        if idx == 0 and decisions(ans) != SAMPLE_DECISIONS:
            raise SystemExit(f"sample decisions mismatch: {decisions(ans)}")
        o = oracle(case)
        if o is not None:
            if decisions(ans) != o:
                raise SystemExit(f"case {idx}: oracle disagreement")
            checked += 1
        if len(case) > 3 << 20 or len(ans) > 1 << 20:
            raise SystemExit(f"case {idx}: too large ({len(case)}, {len(ans)})")
        (out / f"{idx}.in").write_text(case, encoding="utf-8")
        (out / f"{idx}.out").write_text(ans, encoding="utf-8")
        d = decisions(ans)
        print(f"case {idx}: in={len(case)}B out={len(ans)}B yes={d.count('Yes')} no={d.count('No')} "
              f"oracle={'yes' if o is not None else 'no'}")
    print(f"oracle-checked {checked}/21")


if __name__ == "__main__":
    build()
