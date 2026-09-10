#!/usr/bin/env python3
import sys
from functools import lru_cache


@lru_cache(None)
def reachable(n, target):
    return n == target or (n > target and n % 3 == 0 and
                           (reachable(n // 3, target) or reachable(2 * n // 3, target)))


v = list(map(int, sys.stdin.buffer.read().split())); cursor = 1
for _ in range(v[0]):
    n, target = v[cursor:cursor + 2]; cursor += 2
    print("YES" if reachable(n, target) else "NO")
