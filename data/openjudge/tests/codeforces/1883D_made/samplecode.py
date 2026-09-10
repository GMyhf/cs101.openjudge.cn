#!/usr/bin/env python3
import sys
import heapq
from collections import Counter

lines = sys.stdin.buffer.read().splitlines(); q = int(lines[0]); lefts = Counter(); rights = Counter(); lo = []; hi = []
for line in lines[1:q+1]:
    op, left, right = line.split(); left = int(left); right = int(right)
    if op == b"+":
        lefts[left] += 1; rights[right] += 1; heapq.heappush(hi, -left); heapq.heappush(lo, right)
    else:
        lefts[left] -= 1; rights[right] -= 1
    while lo and not rights[lo[0]]: heapq.heappop(lo)
    while hi and not lefts[-hi[0]]: heapq.heappop(hi)
    print("YES" if lo and lo[0] < -hi[0] else "NO")
