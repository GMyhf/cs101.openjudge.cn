#!/usr/bin/env python3
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(data[idx]); k = int(data[idx+1]); idx += 2
        # In each block of n numbers, n-1 are not divisible by n
        # k-th not divisible: block = (k-1) // (n-1), rem = (k-1) % (n-1) + 1
        block = (k - 1) // (n - 1)
        rem = (k - 1) % (n - 1) + 1
        ans = block * n + rem
        out.append(str(ans))
    print('\n'.join(out))

solve()
