# External reference: http://cs101.openjudge.cn/practice/01936/statistics/
# Accepted submission: 51847642
# Source: http://cs101.openjudge.cn/practice/solution/51847642/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import defaultdict, deque, Counter
from itertools import accumulate, permutations, combinations
from heapq import heappush, heappop, heapify
from bisect import bisect_left, bisect_right
from functools import lru_cache

sys.setrecursionlimit(2000000)

input = sys.stdin.readline

while True:
    line = input()
    if not line:
        break
    s, t = line.split()
    i = 0
    for _ in t:
        if s[i] == _:
            i += 1
        if i == len(s):
            break
    print("Yes" if i == len(s) else "No")
