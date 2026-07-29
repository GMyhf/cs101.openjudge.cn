# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1191: 棋盘分割
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01191/
# License: not declared in source collection; no license is inferred.
import sys
# https://blog.csdn.net/Dante__Alighieri/article/details/38823005
# https://blog.csdn.net/qq_40774175/article/details/82704582
# 时间: 93ms
from collections import defaultdict

def f(n, x1, y1, x2, y2):
    if dp[(n, x1, y1, x2, y2)] > 0:
        return dp[(n, x1, y1, x2, y2)]
    if n == 1:
        su = 0
        for i in range(x1, x2+1):
            for j in range(y1, y2+1):
                su += l[i][j]
        dp[(n, x1, y1, x2, y2)] = su*su
        return su*su
    #mi = 10000000
    mi = float('inf')
    for i in range(x1, x2):
        mi = min(mi, f(n-1, x1, y1, i, y2)+f(1, i+1, y1, x2, y2))
        mi = min(mi, f(1, x1, y1, i, y2)+f(n-1, i+1, y1, x2, y2))
    for i in range(y1, y2):
        mi = min(mi, f(n-1, x1, y1, x2, i)+f(1, x1, i+1, x2, y2))
        mi = min(mi, f(1, x1, y1, x2, i)+f(n-1, x1, i+1, x2, y2))
    dp[(n, x1, y1, x2, y2)] = mi
    return mi


n = int(input())
l = []
for i in range(8):
    l.append([int(x) for x in input().split()])
s = 0
for i in l:
    for j in i:
        s += j
dp = defaultdict(int)

print("%.3f"%(f(n, 0,0,7,7)/n-s*s/n/n)**0.5)
