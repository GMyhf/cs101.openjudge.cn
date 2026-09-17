#!/usr/bin/env python3
# Reference solution for Codeforces 2109C1 "Hacking Numbers (Easy Version)" (at most 7 commands).
# Written for this repository as a hand-off artifact for judge-data generation;
# no external source, no external license.
#
# digit, digit: x <= 1e9 has S(x) <= 81, and S(y) <= 16 for y <= 81, so x is in [1, 16].
# add -8, add -4, add -2, add -1 each succeed exactly when x stays >= 1, a binary descent
# that leaves x = 1 whatever it was.  Then add n - 1.  Total <= 7 commands.
import sys


def main():
    read = sys.stdin.readline
    out = sys.stdout
    t = int(read())
    for _ in range(t):
        n = int(read())
        commands = ["digit", "digit", "add -8", "add -4", "add -2", "add -1"]
        if n != 1:
            commands.append(f"add {n - 1}")
        for command in commands + ["!"]:
            out.write(command + "\n")
            out.flush()
            if read().strip() == "-1":
                return


main()
