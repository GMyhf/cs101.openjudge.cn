#!/usr/bin/env python3
# Codeforces 2227F It Just Keeps Going Sideways -- reference solution.
# Written for this repo (cs101.openjudge.cn) as a hand-off artifact; no external license.
#
# Row h holds c[h] = #{i : a[i] >= h} cubes; they keep their order and end in columns
# n-c+1..n, whose sum is f(c) = c*n - c*(c-1)/2.  Cubes only move right, so
# total = sum_h f(c[h]) - sum_i i*a[i]  (1-based i).
# Removing the top cube of column i (height a[i], c = c[a[i]]) changes the total by
# f(c-1) - f(c) + i = i + c - n - 1.  Answer = total + max(0, max_i (i + c[a[i]] - n - 1)).
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); pos = 1; out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = list(map(int, data[pos:pos + n])); pos += n
        cnt = [0] * (n + 2)
        for x in a:
            cnt[x] += 1
        c = [0] * (n + 2)
        for h in range(n, 0, -1):
            c[h] = c[h + 1] + cnt[h]
        total = 0
        for h in range(1, n + 1):
            ch = c[h]
            total += ch * n - ch * (ch - 1) // 2
        total -= sum((i + 1) * x for i, x in enumerate(a))
        best = 0
        for i, x in enumerate(a):
            d = i + 1 + c[x] - n - 1
            if d > best:
                best = d
        out.append(str(total + best))
    sys.stdout.write("\n".join(out) + "\n")


main()
