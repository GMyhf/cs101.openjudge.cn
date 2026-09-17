# Codeforces 2171F Rae Taylor and Trees (hard version) -- reference solution.
# Written for this repository as a hand-off artifact; no external license.
#
# Allowed edges are pairs u < v with u placed before v.  Scan p left to right keeping a
# stack of components (bottom-to-top mins decreasing).  A new value x can join every
# component whose minimum is < x (edge min -> x); those are exactly a top segment of the
# stack.  They merge with x into one component whose minimum is min(x, their mins).
# A tree exists iff one component remains; the n-1 recorded edges then form it.
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); p = 1
    out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        perm = data[p:p + n]; p += n
        stack = []
        edges = []
        for tok in perm:
            x = int(tok)
            mn = x
            while stack and stack[-1] < x:
                m = stack.pop()
                edges.append(f"{m} {x}")
                if m < mn:
                    mn = m
            stack.append(mn)
        if len(stack) == 1:
            out.append("Yes")
            out.extend(edges)
        else:
            out.append("No")
    sys.stdout.write("\n".join(out) + "\n")


main()
