# External reference: http://cs101.openjudge.cn/practice/01005/statistics/
# Accepted submission: 52722958
# Source: http://cs101.openjudge.cn/practice/solution/52722958/
# License: not declared on the submission page; no license is inferred.

import math

n = int(input())
for case in range(1, n+1):
    x, y = map(float, input().split())
    dist_sq = x*x + y*y
    val = math.pi * dist_sq / 100
    # 向上取整
    if val.is_integer():
        z = int(val)
    else:
        z = int(val) + 1
    print(f"Property {case}: This property will begin eroding in year {z}.")
print("END OF OUTPUT.")
