# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2942: 吃糖果
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02942/
# License: not declared; no license is inferred.
import sys
# 读取输入的巧克力数量
n = int(input())

# 初始化 dp 数组，长度为 n，用于存储不同巧克力数量对应的方案数
dp = [0] * n

# 当 n 为 1 时，只有 1 种方案
if n >= 1:
    dp[0] = 1
# 当 n 为 2 时，有 2 种方案
if n >= 2:
    dp[1] = 2

# 从第 3 块巧克力开始，利用动态规划递推公式计算方案数
for i in range(2, n):
    dp[i] = dp[i - 1] + dp[i - 2]

# 输出吃完 n 块巧克力的方案数
print(dp[n - 1])
