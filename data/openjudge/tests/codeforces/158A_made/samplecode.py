#!/usr/bin/env python3
"""158A: Next Round"""
import sys

def solve():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    scores = [int(data[i + 2]) for i in range(n)]
    threshold = scores[k - 1]
    count = 0
    for s in scores:
        if s >= threshold and s > 0:
            count += 1
        else:
            break
    print(count)

solve()
