#!/usr/bin/env python3
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    trees = []
    for i in range(n):
        x = int(data[idx]); h = int(data[idx+1]); idx += 2
        trees.append((x, h))

    if n == 0:
        print(0)
        return

    count = 0
    last_fallen = -float('inf')  # rightmost position occupied by a fallen/staying tree

    for i in range(n):
        x, h = trees[i]
        # Try to fall left
        if x - h > last_fallen:
            count += 1
            last_fallen = x  # tree falls left, occupies x-h to x, but position x is the rightmost point
        elif i == n - 1:
            # Last tree: try to fall right (no tree to the right)
            count += 1
            last_fallen = x + h
        elif x + h < trees[i + 1][0]:
            # Fall right
            count += 1
            last_fallen = x + h
        else:
            # Stay upright - NOT counted, but occupies position x
            last_fallen = x

    print(count)

solve()
