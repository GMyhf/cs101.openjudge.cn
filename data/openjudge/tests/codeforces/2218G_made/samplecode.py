#!/usr/bin/env python3
# Reference solution for Codeforces 2218G "The 67th Iteration of 'Counting is Fun'".
# Written for this repository as a hand-off artifact; no external license.
#
# Given b, each person's constraint is independent.  Let cnt[t] = #{b = t},
# before[t] = #{b < t}, s_i = 1 + min(b of neighbours).
#   b_i = 0            -> a_i = 0 (1 way)
#   s_i > b_i          -> impossible
#   s_i = b_i = t      -> a_i in [1, before[t]]          (before[t] ways)
#   s_i < b_i = t      -> a_i in (before[t-1], before[t]] (cnt[t-1] ways)
import sys
MOD = 676767677


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); p = 1; out = []
    for _ in range(t):
        n = int(data[p]); m = int(data[p + 1]); p += 2
        b = list(map(int, data[p:p + n])); p += n
        cnt = [0] * (m + 1)
        for x in b: cnt[x] += 1
        before = [0] * (m + 1)
        for i in range(1, m + 1): before[i] = before[i - 1] + cnt[i - 1]
        ans = 1; INF = 1 << 30
        for i in range(n):
            x = b[i]
            if x == 0: continue
            nb = INF
            if i > 0: nb = b[i - 1]
            if i + 1 < n and b[i + 1] < nb: nb = b[i + 1]
            s = nb + 1
            if s > x: ans = 0; break
            ans = ans * (before[x] if s == x else cnt[x - 1]) % MOD
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
