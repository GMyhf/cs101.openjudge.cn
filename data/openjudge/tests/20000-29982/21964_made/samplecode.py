# External reference: statistics page /practice/21964/
# Accepted submission: 52244442
# Source: http://cs101.openjudge.cn/practice/solution/52244442/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/21964/
# Accepted submission: 52244442
# Source: http://cs101.openjudge.cn/practice/solution/52244442/
# License: not declared on the submission page; no license is inferred.

n,m=map(int,input().split())
need=[]
value=[]
for i in range(n):
    a,b=map(int,input().split())
    need.append(a)
    value.append(b)
dp=[0]*(m+1)
for i in range(n):
    w=need[i]
    for j in range(m,w-1,-1):
        dp[j]=max(dp[j],dp[j-w]+value[i])
print(dp[m])