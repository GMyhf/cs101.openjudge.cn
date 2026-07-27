# External reference: statistics page /practice/23807/
# Accepted submission: 52686966
# Source: http://cs101.openjudge.cn/practice/solution/52686966/
# License: not declared on the submission page; no license is inferred.

k, n = map(int, input().split())

# 动态规划，dp[i][j] 表示 i 根柱子、j 个盘子的最少步数
# 最大柱子数 100，最大盘子数 100
MAX_K = 100
MAX_N = 100
dp = [[0] * (MAX_N + 1) for _ in range(MAX_K + 1)]

# 初始化：任意不少于3根柱子，1个盘子需要1步
for i in range(3, MAX_K + 1):
    dp[i][0] = 0
    dp[i][1] = 1

# 3根柱子的经典汉诺塔
for j in range(2, MAX_N + 1):
    dp[3][j] = (1 << j) - 1   # 2^j - 1

# 对于4根及以上柱子，使用 Frame-Stewart 递推
for i in range(4, MAX_K + 1):
    for j in range(2, MAX_N + 1):
        best = float('inf')
        # 尝试将上面 x 个盘子先移到辅助柱
        for x in range(1, j):
            val = 2 * dp[i][x] + dp[i - 1][j - x]
            if val < best:
                best = val
        dp[i][j] = best

print(dp[k][n])