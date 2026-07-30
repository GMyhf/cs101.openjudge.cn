# External reference: http://cs101.openjudge.cn/practice/30339/statistics/
# Accepted submission: 52680979
# Source: http://cs101.openjudge.cn/practice/solution/52680979/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

n,m=map(int,sys.stdin.readline().split())
grid=[]
island_idx=[[False] * m for _ in range(n)]
for i in range(n):
    grid.append(sys.stdin.readline().strip())

dirs=[(1,0),(-1,0),(0,1),(0,-1)]

def find_island(x,y,t):
    inq=set()
    bfs=deque()
    inq.add((x,y))
    bfs.append((x,y))
    island_idx[x][y]=t
    while bfs:
        a,b=bfs.popleft()
        for dx,dy in dirs:
            ra,rb=a+dx,b+dy
            if 0<=ra<n and 0<=rb<m and (ra,rb) not in inq and grid[ra][rb]=='X':
                inq.add((ra,rb))
                bfs.append((ra,rb))
                island_idx[ra][rb]=t
    return inq
count=1
islands=[None for _ in range(3)]
for i in range(n):
    for j in range(m):
        if grid[i][j]=='X' and not island_idx[i][j]:
            islands[count-1]=find_island(i,j,count)
            count+=1
INF=10**9

dist=[]
for k in range(3):
    d=[[INF]*m for _ in range(n)]
    q=deque()

    for x,y in islands[k]:
        d[x][y]=0
        q.appendleft((x,y))

    while q:
        x,y=q.popleft()
        cur=d[x][y]
        for dx,dy in dirs:
            rx,ry=x+dx,y+dy
            if 0<=rx<n and 0<=ry<m and d[rx][ry]==INF:
                if grid[rx][ry]=='.':
                    d[rx][ry]=cur+1
                    q.append((rx,ry))
                else:
                    d[rx][ry]=cur
                    q.appendleft((rx,ry))

    dist.append(d)

ans=INF
for i in range(n):
    for j in range(m):
        d0=dist[0][i][j]
        d1=dist[1][i][j]
        d2=dist[2][i][j]
        if d0==INF or d1==INF or d2==INF:
            continue
        total=d0+d1+d2
        if grid[i][j]=='.':
            total-=2
        ans=min(ans,total)

print(ans)
