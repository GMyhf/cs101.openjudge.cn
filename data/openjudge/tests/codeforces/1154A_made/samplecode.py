#!/usr/bin/env python3
"""1154A: Restoring Three Numbers"""
import sys

def solve():
    nums = sorted(map(int, sys.stdin.read().split()))
    # The largest is a+b+c
    total = nums[3]
    a = total - nums[2]
    b = total - nums[1]
    c = total - nums[0]
    print(a, b, c)

solve()
