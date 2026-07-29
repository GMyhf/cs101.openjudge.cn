# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2049: Finding Nemo
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02049/
# License: not declared; no license is inferred.
import sys
from collections import deque

N = 210
Size = 999999
INF = 1<<20
mv = [(1,0),(0,-1),(0,1),(-1,0)]
mapp = [[[0]*2 for _ in range(N)] for _ in range(N)]
vis = [[0]*N for _ in range(N)]

def init():
    global result
    result = 0
    for i in range(N):
        for j in range(N):
            mapp[i][j] = [0, 0]
            vis[i][j] = 0

def BFS(x, y):
    global result
    q = deque()
    q.append((x, y, 0))
    vis[x][y] = 1
    result = INF
    while q:
        t = q.popleft()
        if t[0] == 0 or t[1] == 0 or t[0] > 198 or t[1] > 198:
            result = min(result, t[2])
            continue
        for i in range(4):
            f = [t[0] + mv[i][0], t[1] + mv[i][1]]
            if i == 0 and not vis[f[0]][f[1]] and mapp[t[0]][t[1]][1] != 3:
                f.append(t[2] + 1 if mapp[t[0]][t[1]][1] == 4 else t[2])
                vis[f[0]][f[1]] = 1
                q.append(tuple(f))
            elif i == 1 and not vis[f[0]][f[1]] and mapp[f[0]][f[1]][0] != 3:
                f.append(t[2] + 1 if mapp[f[0]][f[1]][0] == 4 else t[2])
                vis[f[0]][f[1]] = 1
                q.append(tuple(f))
            elif i == 2 and not vis[f[0]][f[1]] and mapp[t[0]][t[1]][0] != 3:
                f.append(t[2] + 1 if mapp[t[0]][t[1]][0] == 4 else t[2])
                vis[f[0]][f[1]] = 1
                q.append(tuple(f))
            elif i == 3 and not vis[f[0]][f[1]] and mapp[f[0]][f[1]][1] != 3:
                f.append(t[2] + 1 if mapp[f[0]][f[1]][1] == 4 else t[2])
                vis[f[0]][f[1]] = 1
                q.append(tuple(f))

while True:
    m, n = map(int, input().split())
    if m == -1 and n == -1:
        break
    init()
    for _ in range(m):
        x, y, d, t = map(int, input().split())
        if d:
            for num in range(t):
                mapp[x-1][y+num][1] = 3
        else:
            for num in range(t):
                mapp[x+num][y-1][0] = 3
    for _ in range(n):
        x, y, d = map(int, input().split())
        if d:
            mapp[x-1][y][1] = 4
        else:
            mapp[x][y-1][0] = 4
    Nemo_x, Nemo_y = map(float, input().split())
    xx, yy = int(Nemo_x + 0.0001), int(Nemo_y + 0.0001)
    if n == 0 and m == 0:
        print(0)
        continue
    if xx <= 0 or yy <= 0 or xx >= 199 or yy >= 199:
        print(0)
    else:
        BFS(xx, yy)
        print(result if result != INF else -1)
