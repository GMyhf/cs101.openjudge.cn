# External reference: http://cs101.openjudge.cn/practice/21458/statistics/
# Accepted submission: 52212724
# Source: http://cs101.openjudge.cn/practice/solution/52212724/
# License: not declared on the submission page; no license is inferred.

T,n=map(int,input().split())
tasks=[]
for i in range(n):
    time,w=map(int,input().split())
    tasks.append((time,w))
dp=[-1]*(T+1)
dp[0]=0
for time,w in tasks:
    for i in range(T,-1,-1):
        if i>=time and dp[i-time]!=-1:
            dp[i]=max(dp[i],dp[i-time]+w)
print(dp[T])
