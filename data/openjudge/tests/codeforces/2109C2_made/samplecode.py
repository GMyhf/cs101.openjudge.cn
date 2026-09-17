#!/usr/bin/env python3
# Reference solution for Codeforces 2109C2 "Hacking Numbers (Medium Version)" (at most 4 commands).
# Written for this repository as a hand-off artifact for judge-data generation;
# no external source, no external license.
#
# mul 9 (always succeeds: 9x <= 9e9), digit: a multiple of 9 below 1e10 has digit sum a multiple
# of 9 that is at most 81 (9x < 1e10 has at most 10 digits, so S <= 89), digit again: every
# multiple of 9 in [9, 81] has digit sum 9.  Then add n - 9 unless n == 9.
import sys


def main():
    read = sys.stdin.readline
    out = sys.stdout
    t = int(read())
    for _ in range(t):
        n = int(read())
        commands = ["mul 9", "digit", "digit"]
        if n != 9:
            commands.append(f"add {n - 9}")
        for command in commands + ["!"]:
            out.write(command + "\n")
            out.flush()
            if read().strip() == "-1":
                return


main()
