#!/usr/bin/env python3
import sys

v = list(map(int, sys.stdin.buffer.read().split())); cursor = 1
for _ in range(v[0]):
    a, b, c = v[cursor:cursor + 3]; cursor += 3
    print("YES" if a + b == c or a + c == b or b + c == a else "NO")
