#!/usr/bin/env python3
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    h1 = [int(data[idx + i]) for i in range(n)]; idx += n
    h2 = [int(data[idx + i]) for i in range(n)]; idx += n

    # dp0 = best sum ending by picking from row 0 at current column
    # dp1 = best sum ending by picking from row 1 at current column
    # best0 = max of all dp0 values seen so far
    # best1 = max of all dp1 values seen so far
    best0 = 0
    best1 = 0
    for i in range(n):
        new0 = h1[i] + best1
        new1 = h2[i] + best0
        # Also can just pick this one alone (best0/best1 might be 0)
        new0 = max(new0, h1[i])
        new1 = max(new1, h2[i])
        best0 = max(best0, new0)
        best1 = max(best1, new1)
    print(max(best0, best1))

solve()
