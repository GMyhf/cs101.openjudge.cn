# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
# 原写法对每个左上角、每个边长都逐格检查整个正方形，最坏约 O(m*n*min(m,n)^3)，300x300 全 1 跑不动。
# 改用动态规划：dp[i][j] 为以 (i,j) 为右下角的最大全 1 正方形边长，它恰好等于以该格为右下角的正方形个数，求和即答案，O(m*n)。
import sys

data = sys.stdin.read().split()
m, n = int(data[0]), int(data[1])
matrix = data[2:2 + m]

cnt = 0
prev = [0] * (n + 1)          # 上一行的 dp，下标整体右移 1，省去边界判断
for i in range(m):
    row = matrix[i]
    cur = [0] * (n + 1)
    for j in range(n):
        if row[j] == '1':
            step = min(prev[j], prev[j + 1], cur[j]) + 1
            cur[j + 1] = step
            cnt += step
    prev = cur

print(cnt)
