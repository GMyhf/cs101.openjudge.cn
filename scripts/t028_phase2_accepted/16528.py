# External reference: http://cs101.openjudge.cn/practice/16528/statistics/
# Accepted submission: 52491463
# Source: http://cs101.openjudge.cn/practice/solution/52491463/
# License: not declared on the submission page; no license is inferred.

n=int(input())
activities=[]
for _ in range(n):
    s,e=[int(i) for i in input().split()]
    if s<0 or e>60:
        continue
    activities.append((s,e))
d={}
for i in range(61):
    d[i]=float('inf')
for s,e in activities:
    d[s]=min(d[s],e)
#dp[i][j]表示只选开始于0-i的活动时，假如最后一天不超过j，那么可以选的最多的活动数
dp=[[0]*61 for i in range(61)]
border=d[0]
for i in range(61):
    dp[0][i]=1 if i>=border else 0
for j in range(1,61):
    dp[j][0]=dp[0][0]
for i in range(1,61):
    s=i
    e=d[i]
    for j in range(61):
        dp[i][j]=dp[i-1][j]
        if e==float('inf'):
            continue
        if j>=e:
            dp[i][j]=max(dp[i][j],dp[i-1][s-1]+1)
print(dp[60][60])
