# External reference: statistics page /practice/24192/
# Accepted submission: 52740123
# Source: http://cs101.openjudge.cn/practice/solution/52740123/
# License: not declared on the submission page; no license is inferred.

n, m = map(int, input().split())
total = n * m
ans = (total + 1) // 2
print(ans)