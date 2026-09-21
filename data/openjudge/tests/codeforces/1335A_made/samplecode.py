#!/usr/bin/env python3
"""1335A: Candies and Two Sisters"""
import sys

def solve():
    data = sys.stdin.read().split()
    t = int(data[0])
    results = []
    for i in range(1, t + 1):
        n = int(data[i])
        # a > b > 0, a + b = n => b ranges from 1 to (n-1)//2
        # Number of valid b values = (n-1) // 2
        ans = (n - 1) // 2
        results.append(ans)
    print("\n".join(map(str, results)))

solve()
