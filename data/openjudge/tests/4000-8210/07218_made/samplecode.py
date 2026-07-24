# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
from collections import deque

def solve_maze():
    T = int(input())
    for _ in range(T):
        R, C = map(int, input().split())
        maze = [list(input().strip()) for _ in range(R)]

        # 找起点 S
        for i in range(R):
            for j in range(C):
                if maze[i][j] == 'S':
                    start = (i, j)
                if maze[i][j] == 'E':
                    end = (i, j)

        # BFS
        queue = deque()
        visited = [[False] * C for _ in range(R)]
        queue.append((start[0], start[1], 0))  # (row, col, distance)
        visited[start[0]][start[1]] = True

        found = False

        while queue:
            x, y, dist = queue.popleft()
            if (x, y) == end:
                print(dist)
                found = True
                break

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < R and 0 <= ny < C:
                    if not visited[nx][ny] and maze[nx][ny] != '#':
                        visited[nx][ny] = True
                        queue.append((nx, ny, dist + 1))

        if not found:
            print("oop!")

# 调用主函数
solve_maze()
