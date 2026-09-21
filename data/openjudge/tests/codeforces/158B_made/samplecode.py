#!/usr/bin/env python3
"""158B: Taxi"""
import sys

def solve():
    data = sys.stdin.read().split()
    n = int(data[0])
    groups = [int(data[i + 1]) for i in range(n)]
    count = [0] * 5
    for g in groups:
        count[g] += 1
    # 4-person groups each need their own taxi
    taxis = count[4]
    # 3-person groups pair with 1-person groups
    taxis += count[3]
    ones_used = min(count[1], count[3])
    count[1] -= ones_used
    # 2-person groups pair together
    taxis += count[2] // 2
    count[2] %= 2
    # Remaining 2-person group takes a taxi
    if count[2] == 1:
        taxis += 1
        # Can fit up to 2 one-person groups
        ones_used = min(count[1], 2)
        count[1] -= ones_used
    # Remaining 1-person groups: 4 per taxi
    taxis += (count[1] + 3) // 4
    print(taxis)

solve()
