# External reference: http://cs101.openjudge.cn/practice/30163/statistics/
# Accepted submission: 50888034
# Source: http://cs101.openjudge.cn/practice/solution/50888034/
# License: not declared on the submission page; no license is inferred.

from collections import deque
for _ in range(int(input())):
    m,n = map(int,input().split())
    height = []
    visited = [[(0,-1)]*n for _ in range(m)]
    for _ in range(m):
        height.append(list(map(int,input().split())))
    x,y = map(int,input().split())
    q = deque()
    q.append((x-1,y-1,0))
    visited[x-1][y-1] = (1,0)
    dire = [(-1,0),(1,0),(0,1),(0,-1)]
    blocks = 0
    while q:
        blocks += 1
        x,y,depth = q.popleft()
        visited[x][y] = (1,depth)
        next_step = set()
        cq = deque()
        v = [[0]*n for _ in range(m)]
        cq.append((x,y,0,0))
        breakable = 0
        rounds = 0
        while cq and rounds < 6:
            rounds += 1
            for _ in range(len(cq)):
                x0,y0,fx,fy = cq.popleft()
                v[x0][y0] = 1
                if height[x0][y0] < height[x][y]:
                    breakable = 1
                    next_step.add((fx,fy))
                for dx,dy in dire:
                    x1,y1 = x0+dx,y0+dy
                    if 0<=x1<m and 0<=y1<n and v[x1][y1] == 0 and height[x1][y1]<=height[x0][y0]:
                        if rounds == 1:
                            fx,fy = dx,dy
                        cq.append((x1,y1,fx,fy))
            if breakable:
                break
        if breakable:
            next_move = next_step
        else:
            next_move = dire
        for dx,dy in next_move:
            x1,y1 = x+dx,y+dy
            if 0<=x1<m and 0<=y1<n:
                new = (depth+1)*(height[x1][y1] == height[x][y])
                if (visited[x1][y1][0] == 0 or new < visited[x1][y1][1]) and depth < 7 and height[x1][y1]<=height[x][y]:
                    blocks -= visited[x1][y1][0]
                    q.append((x1,y1,new))
                    visited[x1][y1] = (1,new)
    print(blocks)
