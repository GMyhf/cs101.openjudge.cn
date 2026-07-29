# External reference: http://cs101.openjudge.cn/practice/02679/statistics/
# Accepted submission: 52502033
# Source: http://cs101.openjudge.cn/practice/solution/52502033/
# License: not declared on the submission page; no license is inferred.

k = int(input())
res = 0
for i in range(1, k + 1):
    res += i ** 3

print(res)
