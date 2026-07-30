# External reference: http://cs101.openjudge.cn/practice/23421/statistics/
# Accepted submission: 52740151
# Source: http://cs101.openjudge.cn/practice/solution/52740151/
# License: not declared on the submission page; no license is inferred.

# 01背包标准解法
n, b = map(int, input().split())
val = list(map(int, input().split()))  # 价值
wt = list(map(int, input().split()))   # 重量

# dp[j] 表示承重 j 时的最大价值
dp = [0] * (b + 1)

for i in range(n):
    # 逆序遍历，保证每个物品只选一次
    for j in range(b, wt[i] - 1, -1):
        dp[j] = max(dp[j], dp[j - wt[i]] + val[i])

print(dp[b])
