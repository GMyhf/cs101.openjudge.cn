# External reference: http://cs101.openjudge.cn/practice/16527/statistics/
# Accepted submission: 52606956
# Source: http://cs101.openjudge.cn/practice/solution/52606956/
# License: not declared on the submission page; no license is inferred.

a, b = input(), input()
for i in range(len(a) - 1, -1, -1):
    if a[i:] == b[:len(a) - i]:
        print(i)
        exit()
