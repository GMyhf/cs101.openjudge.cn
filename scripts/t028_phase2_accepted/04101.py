# External reference: http://cs101.openjudge.cn/practice/04101/statistics/
# Accepted submission: 51446154
# Source: http://cs101.openjudge.cn/practice/solution/51446154/
# License: not declared on the submission page; no license is inferred.

import sys
k = int(sys.stdin.readline().strip())
dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
out = []
while k:
    n = int(sys.stdin.readline().strip())
    Map = []
    for _ in range(n):
        Map.append(sys.stdin.readline().strip())
    visited = [[False]*n for _ in range(n)]
    cnt_r = 0; cnt_b = 0
    for i in range(n):
        for j in range(n):
            if visited[i][j]:
                continue
            if Map[i][j] != "r" and Map[i][j] != "b":
                continue
            visited[i][j] = True
            t = Map[i][j]
            if t == "r":
                cnt_r += 1
                #print(i, j, t)
            elif t == "b":
                cnt_b += 1
            else:
                continue
            queue = [(i, j)]
            while queue:
                x, y = queue.pop()
                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n and visited[nx][ny] == False and Map[nx][ny] == t:
                        visited[nx][ny] = True
                        queue.append((nx, ny))
    out.append(f"{cnt_r} {cnt_b}")
    k -= 1
print("\n".join(out))
