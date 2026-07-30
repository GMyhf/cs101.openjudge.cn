# External reference: http://cs101.openjudge.cn/practice/30909/statistics/
# Accepted submission: 52723655
# Source: http://cs101.openjudge.cn/practice/solution/52723655/
# License: not declared on the submission page; no license is inferred.

from collections import deque
def check(h):
    global m, n
    q = deque()
    q.append((0, 0))
    hvBeen = [[False] * m for _ in range(n)]
    hvBeen[0][0] = True
    while q:
        x, y = q.popleft()
        if x == n - 1 and y == m - 1:
            break
        for dx, dy in d:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and not hvBeen[nx][ny] and abs(a[nx][ny] - a[x][y]) <= h:
                q.append((nx, ny))
                hvBeen[nx][ny] = True
    if hvBeen[n - 1][m - 1]:
        return True
    else:
        return False

d = [(-1, 0), (1, 0), (0, -1), (0, 1)]
[n, m] = [int(x) for x in input().split()]
a = []
for _ in range(n):
    a.append([int(x) for x in input().split()])
l, r = 0, 10 ** 4
while l < r:
    mid = (l + r) // 2
    if check(mid):
        r = mid
    else:
        l = mid + 1
print(l)
