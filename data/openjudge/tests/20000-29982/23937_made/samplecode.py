# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def dfs(mx, visited, x, y):
    # 如果到达右下角，返回True
    if x == n - 1 and y == n - 1:
        return True

    # 定义向右和向下的移动方向
    directions = [(0, 1), (1, 0)]

    for dx, dy in directions:
        nx = x + dx
        ny = y + dy
        # 检查新坐标是否在矩阵范围内，是否已经访问过，以及是否可以通过
        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and mx[nx][ny] == 0:
            visited[nx][ny] = True
            if dfs(mx, visited, nx, ny):
                return True
            visited[nx][ny] = False

    return False

# 读取输入
n = int(input())
mx = [list(map(int, input().split())) for _ in range(n)]

# 初始化访问标记数组
visited = [[False] * n for _ in range(n)]

# 起始点 (0, 0) 必须是可以通过的
if mx[0][0] == 1:
    print('No')
else:
    visited[0][0] = True
    if dfs(mx, visited, 0, 0):
        print('Yes')
    else:
        print('No')
