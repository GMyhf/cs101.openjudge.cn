# Reference strategy for Codeforces 2173E (Shiro's Mirror Duel).
# Written for this repository as a hand-off artifact; no external license.
#
# Orbits are position pairs {i, n+1-i}.
# 0. Odd n: bring value m=(n+1)/2 to the centre with `? pos[m] m` (expected 2 ops).
# 1. For every value x whose partner x' = n+1-x is not in the mirrored slot, query
#    (pos[x], n+1-pos[x']): either outcome makes {x, x'} occupy one orbit (<= n/2 ops),
#    and only positions of not-yet-symmetric values move.
# 2. For i = 1..n/2 move the orbit holding {i, i'} into orbit i. The two needed swaps are
#    mirrors of each other, so query one, then the other: 1/2 done, 1/2 undone
#    (expected 4 ops per misplaced orbit; orientation fix is one deterministic swap).
import sys


def main():
    data = sys.stdin.buffer
    out = sys.stdout

    def read_line():
        return data.readline().split()

    t = int(read_line()[0])
    for _ in range(t):
        n = int(read_line()[0])
        p = [0] + list(map(int, read_line()))
        pos = [0] * (n + 1)
        for i in range(1, n + 1):
            pos[p[i]] = i

        def ask(x, y):
            out.write(f"? {x} {y}\n")
            out.flush()
            a, b = map(int, read_line())
            va, vb = p[a], p[b]
            p[a], p[b] = vb, va
            pos[vb], pos[va] = a, b

        if n % 2 == 1:
            m = (n + 1) // 2
            while pos[m] != m:
                ask(pos[m], m)
        for x in range(1, n + 1):
            y = n + 1 - x
            if x != y and pos[x] + pos[y] != n + 1:
                ask(pos[x], n + 1 - pos[y])
        for i in range(1, n // 2 + 1):
            j = n + 1 - i
            while p[i] != i or p[j] != j:
                if pos[i] != i:
                    ask(i, pos[i])
                else:
                    ask(j, pos[j])
        out.write("!\n")
        out.flush()


main()
