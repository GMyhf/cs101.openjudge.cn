# External reference: http://cs101.openjudge.cn/practice/27598/statistics/
# Accepted submission: 52735684
# Source: http://cs101.openjudge.cn/practice/solution/52735684/
# License: not declared on the submission page; no license is inferred.

n = int(input())
m = int(input())
price = list(map(int, input().split()))

# dp[i][j] = 切长度 i，切成 j 段的最大价值
INF = -10**18
dp = [[INF] * (m + 1) for _ in range(n + 1)]
dp[0][0] = 0

for i in range(1, n + 1):       # 长度
    for j in range(1, m + 1):   # 段数
        for k in range(1, i + 1):  # 最后一段切 k
            dp[i][j] = max(dp[i][j], dp[i - k][j - 1] + price[k - 1])

print(dp[n][m])
