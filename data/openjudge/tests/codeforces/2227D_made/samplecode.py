#!/usr/bin/env python3
# Codeforces 2227D Palindromex -- reference solution.
# Written for this repo (cs101.openjudge.cn) as a hand-off artifact; no external license.
#
# A palindromic subarray with mex >= 1 contains a 0 at some position p; its mirror
# is also a 0, so the palindrome's centre is either a 0 itself or the midpoint of the
# two 0s.  At most three centres; for each, take the maximal palindrome (a superset
# never has smaller mex) and compute its mex.  Answer >= 1 (a single [0]).
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); pos = 1; out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = data[pos:pos + 2 * n]; pos += 2 * n
        m = 2 * n
        zeros = [i for i in range(m) if a[i] == b"0"]
        p, q = zeros
        centres = {(p, p), (q, q), ((p + q) // 2, (p + q + 1) // 2)}
        best = 1
        for l, r in centres:
            if a[l] != a[r]:
                continue
            while l > 0 and r < m - 1 and a[l - 1] == a[r + 1]:
                l -= 1; r += 1
            seen = set(a[l:r + 1])
            mex = 0
            while str(mex).encode() in seen:
                mex += 1
            best = max(best, mex)
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


main()
