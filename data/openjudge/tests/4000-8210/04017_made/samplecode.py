# External reference: http://cs101.openjudge.cn/practice/04017/statistics/
# Accepted submission: 50765287
# Source: http://cs101.openjudge.cn/practice/solution/50765287/
# License: not declared on the submission page; no license is inferred.

dp = [0]*31
dp[0] = 1
dp[1] = 1
for i in range(2, 31):
    dp[i] = dp[i-1] + dp[i-2]
while True:
    try:
        N = int(input())
        print(dp[N])
    except EOFError:
        break
