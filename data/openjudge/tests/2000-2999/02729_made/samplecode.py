# External reference: http://cs101.openjudge.cn/practice/02729/statistics/
# Accepted submission: 51866464
# Source: http://cs101.openjudge.cn/practice/solution/51866464/
# License: not declared on the submission page; no license is inferred.

def f(n):
    if n==0:
        return 1
    return n*f(n-1)
print(f(int(input())))
