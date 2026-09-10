#!/usr/bin/env python3
import sys

for value in map(int, sys.stdin.buffer.read().split()[1:]):
    twos = threes = 0
    while value % 2 == 0:
        value //= 2; twos += 1
    while value % 3 == 0:
        value //= 3; threes += 1
    print(2 * threes - twos if value == 1 and threes >= twos else -1)
