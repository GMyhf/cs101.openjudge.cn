# Reference strategy for Codeforces 2209C (Find the Zero).
# Written for this repository as a hand-off artifact; no external license.
#
# Query (1,2), (3,4), ..., (2n-3, 2n-2): any 1 reveals two zeros. If all are 0, each of
# those n-1 pairs holds at most one zero, so positions 2n-1, 2n hold at least one zero.
# Query (2n-1, 1) and (2n-1, 2): a 1 means a_{2n-1} = 0. If both are 0, then either
# a_{2n-1} != 0 (so a_{2n} = 0), or a_{2n-1} = 0 with pair (1,2) zero-free, which forces
# both last positions to be zero. Either way a_{2n} = 0. Total n+1 queries.
import sys


def main():
    readline = sys.stdin.readline
    out = sys.stdout

    def ask(i, j):
        out.write(f"? {i} {j}\n")
        out.flush()
        return int(readline())

    t = int(readline())
    for _ in range(t):
        n = int(readline())
        answer = 0
        for i in range(1, 2 * n - 2, 2):
            if ask(i, i + 1):
                answer = i
                break
        if not answer:
            if ask(2 * n - 1, 1) or ask(2 * n - 1, 2):
                answer = 2 * n - 1
            else:
                answer = 2 * n
        out.write(f"! {answer}\n")
        out.flush()


main()
