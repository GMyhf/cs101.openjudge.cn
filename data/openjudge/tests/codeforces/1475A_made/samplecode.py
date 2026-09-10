#!/usr/bin/env python3
import sys

for value in map(int, sys.stdin.buffer.read().split()[1:]):
    print("NO" if value & (value - 1) == 0 else "YES")
