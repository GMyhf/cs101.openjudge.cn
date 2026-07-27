# External reference: statistics page /practice/27318/
# Accepted submission: 52736004
# Source: http://cs101.openjudge.cn/practice/solution/52736004/
# License: not declared on the submission page; no license is inferred.

MOD = 10**9 + 7

n, k = map(int, input().split())

# dp[i][j] 表示 1~i 恰好 j 个逆序对的方案数
dp = [[0] * (k + 1) for _ in range(n + 1)]
dp[0][0] = 1

for i in range(1, n + 1):
    # 前缀和优化
    pre_sum = [0] * (k + 1)
    pre_sum[0] = dp[i-1][0]
    for j in range(1, k + 1):
        pre_sum[j] = (pre_sum[j-1] + dp[i-1][j]) % MOD

    for j in range(0, k + 1):
        # dp[i][j] = sum(dp[i-1][j-t])  t=0~min(i-1,j)
        left = j - (i - 1)
        if left <= 0:
            dp[i][j] = pre_sum[j] % MOD
        else:
            dp[i][j] = (pre_sum[j] - pre_sum[left-1]) % MOD

# 保证答案非负
ans = dp[n][k] % MOD
print(ans)