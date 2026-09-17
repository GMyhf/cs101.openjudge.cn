#!/usr/bin/env python3
# Codeforces 2228D Sanae, Cross and Color -- reference solution.
# Written for this repository as a hand-off artifact for building judge data; no external license.
#
# A coloring fixes the set {x <= k1} and the set {y <= k2}, so distinct colorings are
# pairs (cut between consecutive distinct x values, cut between consecutive distinct
# y values) with all four quadrants non-empty.  For the x-cut after value a, the left
# points have y-range [lo1, hi1], right points [lo2, hi2]; a y-cut b works iff
# max(lo1, lo2) <= b < min(hi1, hi2).  Distinct y-cuts in [L, R) (L, R are y values)
# number rank(R) - rank(L) where rank is the index among distinct y values.
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); p = 1; out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        xs = data[p:p + 2 * n:2]; ys = data[p + 1:p + 2 * n:2]; p += 2 * n
        big = n + 1
        mn = [big] * (n + 2); mx = [0] * (n + 2); has_y = [0] * (n + 2)
        for xb, yb in zip(xs, ys):
            x = int(xb); y = int(yb)
            if y < mn[x]: mn[x] = y
            if y > mx[x]: mx[x] = y
            has_y[y] = 1
        rank = [0] * (n + 2); c = 0
        for v in range(1, n + 1):
            c += has_y[v]; rank[v] = c
        present = [x for x in range(1, n + 1) if mx[x]]
        m = len(present)
        # suffix min / max over present x values
        smn = [big] * (m + 1); smx = [0] * (m + 1)
        for i in range(m - 1, -1, -1):
            x = present[i]
            smn[i] = mn[x] if mn[x] < smn[i + 1] else smn[i + 1]
            smx[i] = mx[x] if mx[x] > smx[i + 1] else smx[i + 1]
        pmn = big; pmx = 0; total = 0
        for i in range(m - 1):
            x = present[i]
            if mn[x] < pmn: pmn = mn[x]
            if mx[x] > pmx: pmx = mx[x]
            L = pmn if pmn > smn[i + 1] else smn[i + 1]
            R = pmx if pmx < smx[i + 1] else smx[i + 1]
            if L < R:
                total += rank[R] - rank[L]
        out.append(total)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
