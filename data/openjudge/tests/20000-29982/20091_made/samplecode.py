# External reference: statistics page /practice/20091/
# Accepted submission: 42729047
# Source: http://cs101.openjudge.cn/practice/solution/42729047/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/20091 statistics, Accepted solution 42729047.
# Source: http://cs101.openjudge.cn/practice/solution/42729047/
# Statistics: http://cs101.openjudge.cn/practice/20091/statistics/
# License: not declared on submission page; no license inferred
from math import factorial


def c(n, k):
    return factorial(n) / (factorial(k) * factorial(n - k))


t = int(input())
for i in range(t):
    n = int(input())
    print(int(max(c(n, n // 2), c(n, n // 2 + 1))))
