# External reference: http://cs101.openjudge.cn/practice/29886/statistics/
# Accepted submission: 52279807
# Source: http://cs101.openjudge.cn/practice/solution/52279807/
# License: not declared on the submission page; no license is inferred.

import math
power=[int(i) for i in input().split()]
n=len(power)
#dp[i]表示在打赢状态掩码i下的所有boss的基础下，所需的最少天数
dp=[float('inf') for i in range(1<<n)]
dp[0]=0
for i in range(1<<n):
    gain=bin(i).count("1")
    for j,x in enumerate(power):
        if i>>j & 1:
            current=(~(1<<j))&i
            dp[i]=min(dp[i],dp[current]+math.ceil(power[j]/gain))
print(dp[-1])
