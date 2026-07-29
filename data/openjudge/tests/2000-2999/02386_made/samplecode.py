# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2386: Lake Counting
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02386/
# License: not declared in source collection; no license is inferred.
import sys
#1.dfs
import sys

# input = sys.stdin.read
sys.setrecursionlimit(20000)


def dfs(x, y):
    # 标记当前位置为已访问
    field[x][y] = '.'
    # 遍历8个方向
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        # 检查新位置是否在地图范围内且未被访问
        if 0 <= nx < n and 0 <= ny < m and field[nx][ny] == 'W':
            dfs(nx, ny)


# 一次性读取所有输入
# data = input().split()
# n, m = map(int, data[:2])
# field = [list(row) for row in data[2:2+n]]
n, m = map(int, input().split())
field = [list(input()) for _ in range(n)]
# 初始化8个方向
directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
# 计数器
cnt = 0

# 遍历地图
for i in range(n):
    for j in range(m):
        if field[i][j] == 'W':
            dfs(i, j)
            cnt += 1

print(cnt)
