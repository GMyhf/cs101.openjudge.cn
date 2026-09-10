#!/usr/bin/env python3
import sys
MOD = 1_000_000_007
m, days = map(int, sys.stdin.buffer.readline().split())
short = list(map(int, sys.stdin.buffer.readline().split()))
long = list(map(int, sys.stdin.buffer.readline().split()))
state = [1] + [0] * (m - 1)
for _ in range(days):
    next_state = [0] * m
    for source, ways in enumerate(state):
        for target in range(m):
            next_state[target] = (next_state[target] + ways * (long[source] * short[target] + short[source] * long[target] + short[source] * short[target])) % MOD
    state = next_state
print(sum(state) % MOD)
