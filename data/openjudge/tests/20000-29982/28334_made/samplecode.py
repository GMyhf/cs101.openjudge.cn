# External reference: http://cs101.openjudge.cn/practice/28334/statistics/
# Accepted submission: 52692251
# Source: http://cs101.openjudge.cn/practice/solution/52692251/
# License: not declared on the submission page; no license is inferred.

import sys

data = sys.stdin.read().strip().splitlines()
n,m=map(int,data[0].strip().split())
print(n*(n-1)//2-m)
