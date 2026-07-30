# External reference: http://cs101.openjudge.cn/practice/19930/statistics/
# Accepted submission: 52588851
# Source: http://cs101.openjudge.cn/practice/solution/52588851/
# License: not declared on the submission page; no license is inferred.

from collections import deque

[n, m] = [int(x) for x in input().split()]
a = []
xd, yd = -1, -1
for i in range(n):
    a.append([int(x) for x in input().split()])
    for j in range(m):
        if a[i][j] == 1:
            xd, yd = i, j
hvBeen = [[False] * m for _ in range(n)]
d = [(-1, 0), (1, 0), (0, -1), (0, 1)]
q = deque()
q.append((0, 0, 0))
hvBeen[0][0] = True
ans = -1
while q:
    xt, yt, t = q.popleft()
    if xt == xd and yt == yd:
        ans = t
        break
    nt = t + 1
    for dx, dy in d:
        nx, ny = xt + dx, yt + dy
        if 0 <= nx < n and 0 <= ny < m and not hvBeen[nx][ny] and a[nx][ny] != 2:
            hvBeen[nx][ny] = True
            q.append((nx, ny, nt))
if ans == -1:
    print("NO")
else:
    print(ans)
