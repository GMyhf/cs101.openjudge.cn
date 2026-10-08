# External reference: http://cs101.openjudge.cn/practice/02184/statistics/
# Accepted submission: 41485620
# Source: http://cs101.openjudge.cn/practice/solution/41485620/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。

#import pdb
#pdb.set_trace()
n=int(input())
data=[]
for i in range(n):
    data.append(list(map(int,input().split())))
data.sort(key=lambda x:x[0],reverse=True)
mx=0
for i in range(n):
    if data[i][0]>0:
        mx+=data[i][0]
    else:
        break
inf=10000000;
dp=[-inf for i in range(mx+1)]
mx=0
dp[0]=0
for i in range(n):
    if data[i][0]>0:
        mx+=data[i][0]
        for j in range(mx,data[i][0]-1,-1):
            dp[j]=max(dp[j],dp[j-data[i][0]]+data[i][1])
    else:
        for j in range(0,mx+data[i][0]+1):
            dp[j]=max(dp[j],dp[j-data[i][0]]+data[i][1])

# 2026-10 数据审计修正：原提交写成 dp[i]>0，漏掉了 TF 恰为 0 的方案（如单头牛 5 0 应输出 5）
ans=0
for i in range(mx+1):
    if dp[i]>=0:
        ans=max(ans,dp[i]+i)
print(ans)
