#!/usr/bin/env python3
# Codeforces 2227E It All Went Sideways -- reference solution.
# Written for this repo (cs101.openjudge.cn) as a hand-off artifact; no external license.
#
# The cube at (column i, height h) stays put iff every column i..n has height >= h,
# i.e. h <= sm[i] = min(a[i..n]).  Moved = sum(a) - sum(sm).
# Lowering a[i] by one: the moved count loses 1 (the removed cube, unless it was a
# non-moving one) and sm[j] for j <= i becomes min(sm[j], a[i]-1).  Exactly the j <= i
# with sm[j] == a[i] (a contiguous block ending at i, only if sm[i] == a[i]) drop by 1.
# Gain = (size of that block) - 1; take the best non-negative gain.
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); pos = 1; out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = list(map(int, data[pos:pos + n])); pos += n
        sm = [0] * n; cur = n + 1
        for i in range(n - 1, -1, -1):
            if a[i] < cur:
                cur = a[i]
            sm[i] = cur
        base = sum(a) - sum(sm)
        gain = 0; run = 0
        for i in range(n):
            if i > 0 and sm[i] == sm[i - 1]:
                run += 1
            else:
                run = 1
            if sm[i] == a[i] and run - 1 > gain:
                gain = run - 1
        out.append(str(base + gain))
    sys.stdout.write("\n".join(out) + "\n")


main()
