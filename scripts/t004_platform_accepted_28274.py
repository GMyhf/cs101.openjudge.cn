# External reference: statistics page /practice/28274/
# Accepted submission: 52504766
# Source: http://cs101.openjudge.cn/practice/solution/52504766/
# License: not declared on the submission page; no license is inferred.

from collections import deque

n, m = map(int, input().split())
mat = [list(input()) for _ in range(n)]

cnt = 0
dirs = [(0,1), (0,-1), (-1,0), (1,0)]

for i in range(n):
    for j in range(m):
        if mat[i][j] != '0':
            cnt += 1
            q = deque()
            q.append((i, j))
            mat[i][j] = '0'

            while q:
                x, y = q.popleft()
                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < m:
                        if mat[nx][ny] != '0':
                            mat[nx][ny] = '0'
                            q.append((nx, ny))

print(cnt)