# Codeforces 2146D1 Max Sum OR (Easy Version) -- reference solution.
# Written for this repository as a hand-off artifact; no external license.
#
# a|b = a + b - (a&b), so the sum is at most 2*(0+1+...+r) = r(r+1), reached exactly
# when every a_i & i == 0.  Such a permutation always exists: with m = 2^k - 1 the
# smallest all-ones number >= r, pair i <-> m-i for i in [m-r, r] (complements, AND 0),
# then recurse on the untouched prefix [0, m-r-1].
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    p = 1
    for _ in range(t):
        l = int(data[p]); r = int(data[p + 1]); p += 2
        a = [0] * (r + 1)
        hi = r
        while hi > 0:
            m = (1 << hi.bit_length()) - 1
            lo = m - hi
            for i in range(lo, hi + 1):
                a[i] = m - i
            hi = lo - 1
        out.append(str(r * (r + 1)))
        out.append(" ".join(map(str, a)))
    sys.stdout.write("\n".join(out) + "\n")


main()
