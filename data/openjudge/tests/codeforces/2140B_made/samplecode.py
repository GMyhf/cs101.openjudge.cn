#!/usr/bin/env python3
import sys


def witness(x):
    for y in range(1, 100_000):
        if int(f"{x}{y}") % (x + y) == 0:
            return y
    raise RuntimeError("no witness in the bounded construction domain")


def main():
    values = list(map(int, sys.stdin.buffer.read().split()))
    print("\n".join(map(str, (witness(x) for x in values[1:]))))


if __name__ == "__main__":
    main()
