#!/usr/bin/env python3
import sys


def main():
    values = list(map(int, sys.stdin.buffer.read().split()))
    if not values:
        return
    counts = {}
    for value in values[1:]:
        counts[value] = counts.get(value, 0) + 1
    print(max(counts.values()))


if __name__ == "__main__":
    main()
