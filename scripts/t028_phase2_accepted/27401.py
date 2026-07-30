# External reference: http://cs101.openjudge.cn/practice/27401/statistics/
# Accepted submission: 52417980
# Source: http://cs101.openjudge.cn/practice/solution/52417980/
# License: not declared on the submission page; no license is inferred.

n,t=[int(i) for i in input().split()]
cost=[int(i) for i in input().split()]
#dp[i][j]表示，只考虑前i个物品，凑出大于j的最小可能值。如果凑不出，就是inf
dp=[[float('inf') for j in range(t+1)] for i in range(n+1)]
for i in range(n+1):
    dp[i][0]=0
for i in range(1,n+1):
    for j in range(1,t+1):
        dp[i][j]=min(dp[i-1][j],dp[i-1][max(0,j-cost[i-1])]+cost[i-1]) #看看过去存储的和加上cost[i-1]超过j且最小的

print(dp[n][t] if dp[n][t]!=float('inf') else 0)
