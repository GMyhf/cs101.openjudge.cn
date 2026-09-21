#!/usr/bin/env python3
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    results = []
    for _ in range(t):
        n = int(data[idx]); k = int(data[idx+1]); idx += 2
        a = [int(data[idx + i]) for i in range(n)]; idx += n
        b = [int(data[idx + i]) for i in range(n)]; idx += n
        # Sort indices of a by value, sort b by value, match by rank
        order_a = sorted(range(n), key=lambda i: a[i])
        sorted_b = sorted(b)
        ans = [0] * n
        for j in range(n):
            ans[order_a[j]] = sorted_b[j]
        results.append(' '.join(map(str, ans)))
    sys.stdout.write('\n'.join(results) + '\n')

solve()
