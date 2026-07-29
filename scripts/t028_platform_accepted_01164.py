# External reference: http://cs101.openjudge.cn/practice/01164/statistics/
# Accepted submission: 51696044
# Source: http://cs101.openjudge.cn/practice/solution/51696044/
# License: not declared on the submission page; no license is inferred.

dire = [(0, -1), (-1, 0), (0, 1), (1, 0)]
def dfs(visited, x, y):
    global num
    visited[x][y] = True
    for i in range(4):
        if cond[x][y] >> i & 1:
            continue
        nx, ny = x+dire[i][0], y+dire[i][1]
        if not visited[nx][ny]:
            num += 1
            dfs(visited, nx, ny)
    return num
m = int(input())
n = int(input())
cond = [[int(x) for x in input().split()] for _ in range(m)]
visited = [[False]*n for _ in range(m)]
res, cnt = 0, 0
for i in range(m):
    for j in range(n):
        if not visited[i][j]:
            cnt += 1
            num = 1
            space = dfs(visited, i, j)
            res = max(res, space)
print(cnt)
print(res)
