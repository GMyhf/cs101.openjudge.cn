# External reference: http://cs101.openjudge.cn/practice/02663/statistics/
# Accepted submission: 50532219
# Source: http://cs101.openjudge.cn/practice/solution/50532219/
# License: not declared on the submission page; no license is inferred.

dp = [0]*31
dp[0] = 1
dp[2] = 3
for i in range(4, 31, 2):
    dp[i] = 4*dp[i-2] - dp[i-4]
while True:
    n = int(input())
    if n == -1:
        break
    print(dp[n])
