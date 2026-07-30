# External reference: http://cs101.openjudge.cn/practice/30911/statistics/
# Accepted submission: 52663625
# Source: http://cs101.openjudge.cn/practice/solution/52663625/
# License: not declared on the submission page; no license is inferred.

n,d,f = map(int,input().split())
MOD = 1000000007
dp = [0]*(n+1)
dp[1] = 1
for i in range(2,n+1):
    for j in range(max(0,i-f)+1,max(0,i-d)+1):
        dp[i] += dp[j]
    dp[i] %= MOD
print(sum(dp[-f:])%MOD)
