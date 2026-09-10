#!/usr/bin/env python3
import sys

data = list(map(int, sys.stdin.buffer.read().split())); cursor = 1
for _ in range(data[0]):
    n = data[cursor]; values = sorted(data[cursor + 1:cursor + 1 + n]); cursor += n + 1
    answer = n // 2
    for split in range(1, n):
        if values[split - 1] != values[split]: answer = max(answer, split * (n - split))
    print(answer)
