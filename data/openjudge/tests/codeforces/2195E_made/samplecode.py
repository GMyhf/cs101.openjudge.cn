#!/usr/bin/env python3
# Reference solution for Codeforces 2195E "Idiot First Search".
# Written for this repository as a hand-off artifact; no external license.
#
# S(v): moves to fully walk v's subtree when entering v with every mark empty and
# end up at v's parent.  Leaf: 1.  Internal: 1 + S(l) + 1 + S(r) + 1.
# All marks are erased again afterwards, so from the parent p (still empty) Bob
# performs S(p) moves, and so on: answer(k) = sum of S over the path k .. 1.
import sys
MOD = 1_000_000_007


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); p = 1; out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        L = [0] * (n + 1); R = [0] * (n + 1)
        for i in range(1, n + 1):
            L[i] = int(data[p]); R[i] = int(data[p + 1]); p += 2
        order = [1]
        for v in order:
            if L[v]:
                order.append(L[v]); order.append(R[v])
        S = [1] * (n + 1)
        for v in reversed(order):
            if L[v]:
                S[v] = S[L[v]] + S[R[v]] + 3
        ans = [0] * (n + 1)
        ans[1] = S[1] % MOD
        for v in order:
            if L[v]:
                a = ans[v]
                ans[L[v]] = (a + S[L[v]]) % MOD
                ans[R[v]] = (a + S[R[v]]) % MOD
        out.append(" ".join(map(str, ans[1:])))
    sys.stdout.write("\n".join(out) + "\n")


main()
