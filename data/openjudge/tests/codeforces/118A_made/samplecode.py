#!/usr/bin/env python3
"""118A: String Task"""
import sys

def solve():
    s = sys.stdin.read().strip()
    vowels = set("AOYEUIaoyeui")
    result = []
    for ch in s:
        if ch in vowels:
            continue
        result.append(".")
        result.append(ch.lower())
    print("".join(result))

solve()
