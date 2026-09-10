#!/usr/bin/env python3
import sys

data = list(map(int, sys.stdin.buffer.read().split())); cursor = 1
for _ in range(data[0]):
    n = data[cursor]; cursor += 1; tasks = [tuple(data[cursor+i*2:cursor+i*2+2]) for i in range(n)]; cursor += 2*n
    best = 0.0
    for value, drop in reversed(tasks): best = max(best, value + (1 - drop / 100) * best)
    print(f"{best:.10f}")
