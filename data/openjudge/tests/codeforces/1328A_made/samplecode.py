#!/usr/bin/env python3
"""1328A: Divisibility Problem"""
import sys

def solve():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    results = []
    for _ in range(t):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        rem = a % b
        if rem == 0:
            results.append(0)
        else:
            results.append(b - rem)
    print("\n".join(map(str, results)))

solve()
