# External reference: cs101.openjudge.cn practice/07209 statistics, Accepted solution 51070119.
# Source: http://cs101.openjudge.cn/practice/solution/51070119/
# Statistics: http://cs101.openjudge.cn/practice/07209/statistics/
# License: not declared on submission page; no license inferred
from collections import deque
dire = [[-1, 0], [1, 0], [0, -1], [0, 1]]
def bfs(matrix, start, end, row, col):
    q = deque([start])
    visited = [[False]*col for _ in range(row)]
    visited[start[0]][start[1]] = True
    while q:
        x, y = q.popleft()
        if x == end[0] and y == end[1]:
            break
        for dx, dy in dire:
            nx, ny = x+dx, y+dy
            if 0 <= nx < row and 0 <= ny < col and matrix[nx][ny] != '1' and not visited[nx][ny]:
                q.append((nx, ny))
                visited[nx][ny] = (x, y)
    res = []
    pos = end
    while pos != start:
        res.append(pos)
        pos = visited[pos[0]][pos[1]]
    res.append(pos)
    res.reverse()
    return res
X, Y = map(int, input().split())
matrix = [[x for x in input()] for _ in range(X)]
for i in range(X):
    for j in range(Y):
        if matrix[i][j] == 'R':
            start = (i, j)
        elif matrix[i][j] == 'C':
            end = (i, j)
        elif matrix[i][j] == 'Y':
            key = (i, j)
res_1 = bfs(matrix, start, key, X, Y)
res_2 = bfs(matrix, key, end, X, Y)
for i, j in res_1+res_2[1:]:
    print(i+1, j+1)