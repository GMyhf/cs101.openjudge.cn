# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2385: Apple Catching
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02385/
# License: not declared in source collection; no license is inferred.
import sys
#gpt
'''
dp[i][j] 表示在第i分钟，移动了j次可以接到的最大苹果数量。根据题意，Bessie初始在1号树下，
只有当j为偶数时，它在1号树下；当j为奇数时，它在2号树下。

初始化dp数组为0，然后按照时间顺序逐一遍历各分钟，在每一分钟，它可以选择待在原地，也可以选择移动。
'''
T, W = map(int, input().split())
trees = [0] + [int(input()) for _ in range(T)]
dp = [[0]*(W+1) for _ in range(T+1)]
for i in range(1, T + 1):
    for j in range(min(i, W) + 1):
        if j % 2 + 1 == trees[i]: # 在树下
            dp[i][j] = max(dp[i][j], dp[i-1][j] + 1) #本来就在
            if j > 0:
                dp[i][j] = max(dp[i][j], dp[i-1][j-1] + 1) #在上一分钟结束时刻移动到这里
        else:
            dp[i][j] = dp[i-1][j] # 不在树下
            if j > 0:
                dp[i][j] = max(dp[i][j], dp[i-1][j-1]) #在上一分钟结束时刻离开这里
print(max(dp[T]))
