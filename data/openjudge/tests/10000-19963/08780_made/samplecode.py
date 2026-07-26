# External reference: statistics page /practice/08780/
# Accepted submission: 52735269
# Source: http://cs101.openjudge.cn/practice/solution/52735269/
# License: not declared on the submission page; no license is inferred.

n = int(input())
a = [*map(int, input().split())]
dp = [1] * n
maxn = -1
for i in range(n):
    for j in range(i):
        if a[j] >= a[i]:
            dp[i] = max(dp[i], dp[j] + 1)
    maxn = max(maxn, dp[i])
print(maxn)