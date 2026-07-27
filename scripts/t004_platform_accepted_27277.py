# External reference: statistics page /practice/27277/
# Accepted submission: 52740040
# Source: http://cs101.openjudge.cn/practice/solution/52740040/
# License: not declared on the submission page; no license is inferred.

# 读取输入
coins = list(map(int, input().split()))
amount = int(input())

# 边界：金额为0直接返回0
if amount == 0:
    print(0)
    exit()

INF = float('inf')
# dp[i] = 凑出金额i需要的最小硬币数
dp = [INF] * (amount + 1)
dp[0] = 0

# 完全背包
for coin in coins:
    for i in range(coin, amount + 1):
        if dp[i - coin] != INF:
            dp[i] = min(dp[i], dp[i - coin] + 1)

# 输出答案
print(dp[amount] if dp[amount] != INF else -1)