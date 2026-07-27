# External reference: statistics page /practice/24755/
# Accepted submission: 52682226
# Source: http://cs101.openjudge.cn/practice/solution/52682226/
# License: not declared on the submission page; no license is inferred.

import math

n = int(input())
# 卡特兰数 C(2n, n) / (n+1)
print(math.comb(2 * n, n) // (n + 1))