# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 1376: Robot
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01376/
# License: not declared in source collection; no license is inferred.
import sys
from collections import deque


def bfs_min_time(grid, start, end, direction):
    N, M = len(grid), len(grid[0])
    # 定义朝向：0-东, 1-南, 2-西, 3-北
    dir_map = {'E': 0, 'S': 1, 'W': 2, 'N': 3}
    start_dir = dir_map[direction]
    sr, sc, tr, tc = start[0], start[1], end[0], end[1]

    # 机器人中心只能位于网格交点，合法交点要求其周围四个相邻的格子都不能有障碍。
    # 对于交点 (i, j) (i,j均从1开始计数，i∈[1,N-1], j∈[1,M-1])，对应的格子为
    # (i-1,j-1), (i-1,j), (i,j-1), (i,j)
    valid = [[False] * (M) for _ in range(N)]
    for i in range(1, N):
        for j in range(1, M):
            if grid[i - 1][j - 1] == 0 and grid[i - 1][j] == 0 and grid[i][j - 1] == 0 and grid[i][j] == 0:
                valid[i][j] = True

    # 检查起始点和目标点是否合法
    if not valid[sr][sc] or not valid[tr][tc]:
        return -1

    # 定义方向移动，顺序：东, 南, 西, 北
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]

    # BFS: 状态 (r, c, d)
    visited = [[[False] * 4 for _ in range(M)] for _ in range(N)]
    q = deque()
    q.append((sr, sc, start_dir, 0))
    visited[sr][sc][start_dir] = True

    while q:
        r, c, d, steps = q.popleft()
        # 判断是否到达目标位置（朝向不要求匹配）
        if r == tr and c == tc:
            return steps

        # 转向操作
        # Left: d_new = (d+3)%4, Right: d_new = (d+1)%4
        for nd in [(d + 3) % 4, (d + 1) % 4]:
            if not visited[r][c][nd]:
                visited[r][c][nd] = True
                q.append((r, c, nd, steps + 1))

        # 前进1,2,3步，每一步中间都必须合法
        for k in range(1, 4):
            nr = r + dr[d] * k
            nc = c + dc[d] * k
            # 判断越界
            if nr < 1 or nr >= N or nc < 1 or nc >= M:
                break
            # 如果当前位置不合法，则不能继续向前走
            if not valid[nr][nc]:
                break
            if not visited[nr][nc][d]:
                visited[nr][nc][d] = True
                q.append((nr, nc, d, steps + 1))
    return -1


# 读取输入数据
while True:
    n, m = map(int, input().split())
    if n == 0 and m == 0:
        break
    grid = [list(map(int, input().split())) for _ in range(n)]
    sx, sy, ex, ey, direction = input().split()
    sx, sy, ex, ey = map(int, [sx, sy, ex, ey])

    direction = direction.upper()  # 确保方向是大写

    # 计算最短时间
    result = bfs_min_time(grid, (sx, sy), (ex, ey), direction[0])
    print(result)
