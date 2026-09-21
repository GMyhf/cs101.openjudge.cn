#!/usr/bin/env python3
import sys

def solve():
    data = sys.stdin.buffer.read().decode()
    lines = data.split('\n')
    s = lines[0].strip()
    n = len(s)

    # Build prefix sum: p[i] = number of j in [0, i-1] where s[j] == s[j+1]
    # (0-indexed internally)
    p = [0] * (n + 1)
    for i in range(1, n):
        p[i + 1] = p[i] + (1 if s[i] == s[i - 1] else 0)

    m = int(lines[1].strip())
    out = []
    for i in range(2, 2 + m):
        parts = lines[i].strip().split()
        l, r = int(parts[0]), int(parts[1])
        # Count j in [l, r-1] (1-indexed) where s[j-1] == s[j] (0-indexed)
        # This equals p[r] - p[l]
        # Because p[r] counts matches in positions 0..r-2 (i.e., pairs (0,1),(1,2),...,(r-2,r-1))
        # which in 1-indexed is pairs (1,2),(2,3),...,(r-1,r)
        # We want pairs (l,l+1),...,(r-1,r) which is indices l-1 to r-2 in 0-indexed
        # p[r] - p[l] gives us matches at 0-indexed positions l-1 through r-2
        ans = p[r] - p[l]
        out.append(str(ans))
    sys.stdout.write('\n'.join(out) + '\n')

solve()
