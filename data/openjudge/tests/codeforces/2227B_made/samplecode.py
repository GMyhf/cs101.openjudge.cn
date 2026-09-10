#!/usr/bin/env python3
import sys

data = sys.stdin.buffer.read().split(); cursor = 1
for _ in range(int(data[0])):
    n = int(data[cursor]); text = data[cursor + 1]; cursor += 2
    print("YES" if text.count(b"(") * 2 == n else "NO")
