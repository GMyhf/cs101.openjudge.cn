#!/usr/bin/env python3
"""1352A: Sum of Round Numbers"""
import sys

def solve():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        n = int(data[i])
        s = str(n)
        rounds = []
        for j, ch in enumerate(s):
            if ch != '0':
                rounds.append(ch + '0' * (len(s) - 1 - j))
        out.append(str(len(rounds)))
        out.append(" ".join(rounds))
    print("\n".join(out))

solve()
