# External reference: cs101.openjudge.cn practice/20138 statistics, Accepted solution 52543271.
# Source: http://cs101.openjudge.cn/practice/solution/52543271/
# Statistics: http://cs101.openjudge.cn/practice/20138/statistics/
# License: not declared on submission page; no license inferred
import sys
from collections import defaultdict, deque, Counter
from itertools import accumulate, permutations, combinations
from heapq import heappush, heappop, heapify
from bisect import bisect_left, bisect_right
from functools import lru_cache
from copy import deepcopy
from fractions import Fraction
from math import gcd

sys.setrecursionlimit(2000000)

input = sys.stdin.readline


def lcm(a: int, b: int):
    return a * b // gcd(a, b)


n = int(input())
coef = [list(map(float, input().split())) for _ in range(n)]

ans = [0] * n

for i in range(n):
    for j in range(i, n):
        if coef[j][i] != 0:
            coef[j], coef[i] = coef[i], coef[j]
            break

    for j in range(i + 1, n):
        if coef[j][i] == 0:
            continue
        d = coef[j][i] / coef[i][i]
        for k in range(i, n + 1):
            coef[j][k] -= coef[i][k] * d


for i in range(n - 1, -1, -1):
    b = coef[i][n]
    for j in range(i + 1, n):
        b -= coef[i][j] * ans[j]
    ans[i] = b / coef[i][i]


for i, x in enumerate(ans):
    print(f"x{i+1} = {float(x):.2f}")
