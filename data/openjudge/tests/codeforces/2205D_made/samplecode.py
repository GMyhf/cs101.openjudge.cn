#!/usr/bin/env python3
# Reference solution for Codeforces 2205D "Simons and Beating Peaks".
# Written for this repository as a hand-off artifact; no external license.
#
# The maximum can never be removed and must end at an array end, so one whole side
# of it is deleted and the other side is solved recursively (its maximum plays the
# same role).  On the Cartesian tree (max at root):
#   f(v) = min(size(left) + f(right), size(right) + f(left)),  f(empty) = 0.
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); p = 1; out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        a = data[p:p + n]; p += n
        a = list(map(int, a))
        left = [-1] * n; right = [-1] * n
        stack = []
        for i in range(n):
            x = a[i]; last = -1
            while stack and a[stack[-1]] < x:
                last = stack.pop()
            left[i] = last
            if stack:
                right[stack[-1]] = i
            stack.append(i)
        root = stack[0]
        order = [root]
        for v in order:
            if left[v] >= 0: order.append(left[v])
            if right[v] >= 0: order.append(right[v])
        size = [1] * n; f = [0] * n
        for v in reversed(order):
            l = left[v]; r = right[v]
            sl = size[l] if l >= 0 else 0; fl = f[l] if l >= 0 else 0
            sr = size[r] if r >= 0 else 0; fr = f[r] if r >= 0 else 0
            size[v] = sl + sr + 1
            x = sl + fr; y = sr + fl
            f[v] = x if x < y else y
        out.append(str(f[root]))
    sys.stdout.write("\n".join(out) + "\n")


main()
