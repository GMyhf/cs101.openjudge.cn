# External reference: http://cs101.openjudge.cn/practice/29954/statistics/
# Accepted submission: 52726715
# Source: http://cs101.openjudge.cn/practice/solution/52726715/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

def solve():
    # 读取第一行 R, C, K
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    R = int(input_data[0])
    C = int(input_data[1])
    K = int(input_data[2])

    # 读取网格
    grid = input_data[3:]

    start_pos = None
    end_pos = None

    # 找到起点 S 和终点 E 的位置
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S':
                start_pos = (r, c)
            elif grid[r][c] == 'E':
                end_pos = (r, c)

    if not start_pos or not end_pos:
        print("-1")
        return

    # BFS 状态: (row, col, used_blinks, steps)
    sr, sc = start_pos
    er, ec = end_pos

    # visited[r][c][k] 记录坐标 (r,c) 在消耗 k 次闪现时是否到达过
    visited = [[[False] * (K + 1) for _ in range(C)] for _ in range(R)]

    queue = deque([(sr, sc, 0, 0)])
    visited[sr][sc][0] = True

    # 四个移动方向
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        r, c, k, dist = queue.popleft()

        # 到达终点
        if r == er and c == ec:
            print(dist)
            return

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # 边界检查
            if 0 <= nr < R and 0 <= nc < C:
                char = grid[nr][nc]

                if char == '#':
                    # 移动到屏障，消耗 1 次闪现
                    if k < K and not visited[nr][nc][k + 1]:
                        visited[nr][nc][k + 1] = True
                        queue.append((nr, nc, k + 1, dist + 1))
                else:
                    # 移动到走廊（. 或 S 或 E），不消耗闪现
                    if not visited[nr][nc][k]:
                        visited[nr][nc][k] = True
                        queue.append((nr, nc, k, dist + 1))

    # 无法到达
    print("-1")

if __name__ == "__main__":
    solve()
