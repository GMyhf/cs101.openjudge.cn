import sys
from collections import deque

sys.setrecursionlimit(10**9)

move = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def tong(x, y, q, maze):
    """DFS标记第一个岛屿，并将边界点加入队列"""
    maze[x][y] = '2'
    q.append((x, y))
    for dx, dy in move:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and maze[nx][ny] == '1':
            tong(nx, ny, q, maze)

def bfs(q, maze):
    """BFS寻找第二个岛屿的最短距离"""
    s = 0
    while q:
        for _ in range(len(q)):
            x, y = q.popleft()
            for dx, dy in move:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n:
                    if maze[nx][ny] == '1':  # 找到第二个岛屿
                        return s
                    if maze[nx][ny] == '0':  # 水域，加入队列
                        maze[nx][ny] = '2'  # 标记为访问过
                        q.append((nx, ny))
        s += 1
    return s

# 主函数
n = int(input())
maze = [list(input()) for _ in range(n)]
q = deque()
found = False  # 标记是否找到第一个岛屿

for i in range(n):
    if found:
        break
    for j in range(n):
        if maze[i][j] == '1':  # 找到第一个岛屿
            tong(i, j, q, maze)
            print(bfs(q, maze))
            found = True
            break
