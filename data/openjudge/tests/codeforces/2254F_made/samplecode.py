#!/usr/bin/env python3
# Codeforces 2254F Whiplash -- reference solution.
# Operation: pick i, XOR all other a[j] with a[i].  Determine if a -> b.
# Invariant: extend a with xor(a) to get a multiset of size n+1; do the same for b.
# a -> b iff the two multisets are equal.
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); pos = 1; out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(data[pos + i]) for i in range(n)]; pos += n
        b = [int(data[pos + i]) for i in range(n)]; pos += n
        xa = 0
        for x in a:
            xa ^= x
        xb = 0
        for x in b:
            xb ^= x
        c = sorted([x ^ xa for x in a] + [xa])
        d = sorted([x ^ xb for x in b] + [xb])
        out.append("YES" if c == d else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
