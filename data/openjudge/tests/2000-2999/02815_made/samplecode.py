# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2815: 城堡问题
# Fenced code block index: 3
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02815/
# License: not declared in source collection; no license is inferred.
import sys
from collections import deque

# 四个方向：西、北、东、南
dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]
walls = [1, 2, 4, 8]  # 按顺序对应西北东南

def bfs(start_r, start_c, m, n, castle, visited):
    q = deque()
    q.append((start_r, start_c))
    visited[start_r][start_c] = True
    area = 0

    while q:
        r, c = q.popleft()
        area += 1
        val = castle[r][c]

        for d, (dr, dc) in enumerate(dirs):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                # 如果这个方向没有墙，并且未访问过
                if not (val & walls[d]) and not visited[nr][nc]:
                    visited[nr][nc] = True
                    q.append((nr, nc))
    return area

def main():
    m = int(input().strip())  # 行数（南北）
    n = int(input().strip())  # 列数（东西）

    castle = [list(map(int, input().split())) for _ in range(m)]
    visited = [[False] * n for _ in range(m)]

    room_count = 0
    max_area = 0

    for r in range(m):
        for c in range(n):
            if not visited[r][c]:
                room_count += 1
                area = bfs(r, c, m, n, castle, visited)
                max_area = max(max_area, area)

    print(room_count)
    print(max_area)

if __name__ == "__main__":
    main()
