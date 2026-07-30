# External reference: http://cs101.openjudge.cn/practice/19929/statistics/
# Accepted submission: 51527971
# Source: http://cs101.openjudge.cn/practice/solution/51527971/
# License: not declared on the submission page; no license is inferred.

m, n = map(int, input().split())
a = list(map(int, input().split()))
w = list(map(int, input().split()))
dp = [0] * (n + 1)
for i in range(m):
    dp[a[i]] = max(dp[1 : a[i] + 1]) + w[i]
print(max(dp))
