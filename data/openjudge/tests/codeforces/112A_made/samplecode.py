#!/usr/bin/env python3
"""112A: Petya and Strings"""
import sys

def solve():
    lines = sys.stdin.read().split("\n")
    s1 = lines[0].strip().lower()
    s2 = lines[1].strip().lower()
    if s1 < s2:
        print(-1)
    elif s1 > s2:
        print(1)
    else:
        print(0)

solve()
