#!/usr/bin/env python3
import sys

def solve():
    MOD = 1000000007
    data = sys.stdin.buffer.read().split()
    n, k, d = int(data[0]), int(data[1]), int(data[2])

    # dp0[w] = number of paths of total weight w using only edges 1..d-1
    # dp1[w] = number of paths of total weight w using edges 1..k
    # Answer = dp1[n] - dp0[n]

    dp0 = [0] * (n + 1)
    dp1 = [0] * (n + 1)
    dp0[0] = 1
    dp1[0] = 1

    for w in range(1, n + 1):
        # dp0: edges from 1 to min(w, d-1)
        for j in range(1, min(w, d - 1) + 1):
            dp0[w] = (dp0[w] + dp0[w - j]) % MOD
        # dp1: edges from 1 to min(w, k)
        for j in range(1, min(w, k) + 1):
            dp1[w] = (dp1[w] + dp1[w - j]) % MOD

    print((dp1[n] - dp0[n]) % MOD)

solve()
