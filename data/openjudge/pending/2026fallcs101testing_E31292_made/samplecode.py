#!/usr/bin/env python3
import sys


def solve(n):
    balloons = list(range(1, n + 1))
    last_released = None
    while balloons:
        last_released = None
        remaining = []
        for position, original_number in enumerate(balloons, 1):
            root = int(position ** 0.5)
            if root * root == position:
                last_released = original_number
            else:
                remaining.append(original_number)
        balloons = remaining
    return last_released


if __name__ == "__main__":
    print(solve(int(sys.stdin.readline())))
