# External reference: http://cs101.openjudge.cn/practice/27205/statistics/
# Accepted submission: 52688005
# Source: http://cs101.openjudge.cn/practice/solution/52688005/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

data = sys.stdin.read().strip().splitlines()
m, n = map(int, data[0].strip().split())
matrix = []
for i in range(1, m + 1):
    line = list(map(int, data[i].strip().split()))
    matrix.append(line)


def largestRectangleArea(h):
    st = []
    res = 0
    h.append(0)
    for i, v in enumerate(h):
        while st and h[st[-1]] > v:
            ht = h[st.pop()]
            w = i if not st else i - st[-1] - 1
            res = max(res, ht * w)
        st.append(i)
    return res


height = [0] * n
max_S = 0
for i in range(m):
    h = []
    for j in range(n):
        if matrix[i][j] == 1:
            height[j] = 0
        else:
            height[j] += 1
        h.append((height[j]))
    S = largestRectangleArea(h)
    max_S = max(S, max_S)
print(max_S)
