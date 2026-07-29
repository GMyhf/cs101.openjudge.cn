# External reference: http://cs101.openjudge.cn/practice/01163/statistics/
# Accepted submission: 51696004
# Source: http://cs101.openjudge.cn/practice/solution/51696004/
# License: not declared on the submission page; no license is inferred.

N = int(input())
dp = [int(input())]
for length in range(2, N+1):
    n_dp = [int(x) for x in input().split()]
    n_dp[0] += dp[0]
    n_dp[-1] += dp[-1]
    for i in range(1, length-1):
        n_dp[i] += max(dp[i-1], dp[i])
    dp = n_dp
print(max(dp))
