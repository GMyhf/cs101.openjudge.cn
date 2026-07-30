# External reference: http://cs101.openjudge.cn/practice/18108/statistics/
# Accepted submission: 52510585
# Source: http://cs101.openjudge.cn/practice/solution/52510585/
# License: not declared on the submission page; no license is inferred.

t=int(input())
directions=[(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
for _ in range(t):
    n,m=[int(i) for i in input().split()]
    matrix=[input() for i in range(n)]
    visited=[[False]*m for i in range(n)]
    cnt=0
    for i in range(n):
        for j in range(m):
            if visited[i][j]==False and matrix[i][j]=="W":
                cnt+=1
                visited[i][j]=True
                stack=[(i,j)]
                while stack:
                    x,y=stack.pop()
                    for dx,dy in directions:
                        nx=x+dx
                        ny=y+dy
                        if 0<=nx<n and 0<=ny<m and visited[nx][ny]==False and matrix[nx][ny]=="W":
                            visited[nx][ny]=True
                            stack.append((nx,ny))
    print(cnt)
