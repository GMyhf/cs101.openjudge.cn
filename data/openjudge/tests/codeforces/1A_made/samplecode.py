#!/usr/bin/env python3
"""1A: Theatre Square - ceil(n/a) * ceil(m/a)"""
import sys

def solve():
    n, m, a = map(int, sys.stdin.read().split())
    ans = ((n + a - 1) // a) * ((m + a - 1) // a)
    print(ans)

solve()
