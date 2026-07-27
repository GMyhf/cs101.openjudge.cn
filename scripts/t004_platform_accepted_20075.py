# External reference: cs101.openjudge.cn practice/20075 statistics, Accepted solution 51319354.
# Source: http://cs101.openjudge.cn/practice/solution/51319354/
# Statistics: http://cs101.openjudge.cn/practice/20075/statistics/
# License: not declared on submission page; no license inferred
from collections import deque
dire = [(-1, 0), (1, 0), (0, -1), (0, 1)]
def bfs(sx, sy):
    q = deque([(sx, sy, 0)])
    visited = [[0]*n for _ in range(m)]
    visited[sx][sy] = 1
    if matrix[sx][sy] == 2:
        return 'NO'
    while q:
        x, y, step = q.popleft()
        if matrix[x][y] == 1:
            return step
        for dx, dy in dire:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny]:
                if matrix[nx][ny] == 2:
                    visited[nx][ny] = 1
                    continue
                else:
                    q.append((nx, ny, step+1))
                    visited[nx][ny] = 1
    return 'NO'
m, n, p = map(int, input().split())
matrix = [[int(x) for x in input().split()] for _ in range(m)]
for _ in range(p):
    y, x = map(int, input().split())
    print(bfs(x-1, y-1))
