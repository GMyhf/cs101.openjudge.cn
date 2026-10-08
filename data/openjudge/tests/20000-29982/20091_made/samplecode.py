# External reference: statistics page /practice/20091/
# Accepted submission: 42729047
# Source: http://cs101.openjudge.cn/practice/solution/42729047/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。

# External reference: cs101.openjudge.cn practice/20091 statistics, Accepted solution 42729047.
# Source: http://cs101.openjudge.cn/practice/solution/42729047/
# Statistics: http://cs101.openjudge.cn/practice/20091/statistics/
# License: not declared on submission page; no license inferred
from math import factorial


def c(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))  # 原 AC 代码用 / 走浮点，n 稍大末位全错，改整除


t = int(input())
for i in range(t):
    n = int(input())
    print(int(max(c(n, n // 2), c(n, n // 2 + 1))))
