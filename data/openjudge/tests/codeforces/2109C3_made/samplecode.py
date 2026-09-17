#!/usr/bin/env python3
# Reference solution for Codeforces 2109C3 "Hacking Numbers (Hard Version)" (at most f(n) commands).
# Written for this repository as a hand-off artifact for judge-data generation;
# no external source, no external license.
#
# For 1 <= x <= 1e9, x * 999999999 = x * 10^9 - x, whose decimal digits are (x - 1) followed by
# the nine's complement of x - 1 padded to 9 digits, so its digit sum is always 81.
# mul 999999999, digit gives 81 (2 commands, optimal for n = 81); otherwise add n - 81 (3).
import sys


def main():
    read = sys.stdin.readline
    out = sys.stdout
    t = int(read())
    for _ in range(t):
        n = int(read())
        commands = ["mul 999999999", "digit"]
        if n != 81:
            commands.append(f"add {n - 81}")
        for command in commands + ["!"]:
            out.write(command + "\n")
            out.flush()
            if read().strip() == "-1":
                return


main()
