# External reference: cs101.openjudge.cn practice/04150 statistics, Accepted solution 44330785.
# Source: http://cs101.openjudge.cn/practice/solution/44330785/
# Statistics: http://cs101.openjudge.cn/practice/04150/statistics/
# License: not declared on submission page; no license inferred
n=int(input())
a=[0]+list(map(int,input().split()))
b=[0]+list(map(int,input().split()))
c=[0]+list(map(int,input().split()))
dp=[[0]*(n+1) for _ in range(2)]
dp[0][1],dp[1][1]=a[1],b[1]
for i in range(2,n+1):
    dp[0][i]=max(dp[0][i-1]+b[i],dp[1][i-1]+a[i])
    dp[1][i]=max(dp[0][i-1]+c[i],dp[1][i-1]+b[i])
print(dp[0][n])