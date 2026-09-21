#!/usr/bin/env python3
"""433B: Kuriyama Mirai's Stones"""
import sys

def solve():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    v = [int(data[idx + i]) for i in range(n)]; idx += n
    m = int(data[idx]); idx += 1

    # Prefix sums for original array
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + v[i]

    # Prefix sums for sorted array
    u = sorted(v)
    pref2 = [0] * (n + 1)
    for i in range(n):
        pref2[i + 1] = pref2[i] + u[i]

    out = []
    for _ in range(m):
        typ = int(data[idx]); l = int(data[idx + 1]); r = int(data[idx + 2]); idx += 3
        if typ == 1:
            ans = pref[r] - pref[l - 1]
        else:
            ans = pref2[r] - pref2[l - 1]
        out.append(str(ans))
    print("\n".join(out))

solve()
