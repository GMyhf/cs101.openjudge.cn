# External reference: http://cs101.openjudge.cn/practice/18155/statistics/
# Accepted submission: 47911639
# Source: http://cs101.openjudge.cn/practice/solution/47911639/
# License: not declared on the submission page; no license is inferred.

import sys
from itertools import combinations

# 读取输入
t = int(input())
a = list(map(int, sys.stdin.read().split()))

# 枚举所有可能的子集
n = len(a)
for i in range(1, 1 << n):  # 遍历从 1 到 (2^n - 1)
    product = 1
    for j in range(n):
        if (i >> j) & 1:  # 检查第 j 位是否被选中
            product *= a[j]
            if product == t:
                print("YES")
                exit(0)

print("NO")
