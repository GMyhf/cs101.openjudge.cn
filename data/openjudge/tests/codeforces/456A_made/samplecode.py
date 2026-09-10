#!/usr/bin/env python3
import sys

values = list(map(int, sys.stdin.buffer.read().split()))
rows = sorted(zip(values[1::2], values[2::2]))
print("Happy Alex" if any(left[1] > right[1] for left, right in zip(rows, rows[1:])) else "Poor Alex")
