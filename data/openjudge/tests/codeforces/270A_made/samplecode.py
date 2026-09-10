#!/usr/bin/env python3
import sys

for angle in map(int, sys.stdin.buffer.read().split()[1:]):
    print("YES" if 360 % (180 - angle) == 0 else "NO")
