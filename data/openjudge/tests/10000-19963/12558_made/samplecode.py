# External reference: http://cs101.openjudge.cn/practice/12558/statistics/
# Accepted submission: 52467858
# Source: http://cs101.openjudge.cn/practice/solution/52467858/
# License: not declared on the submission page; no license is inferred.

n,m=[int(i) for i in input().split()]
matrix=[[int(i) for i in input().split()] for _ in range(n)]
visited=[[False]*m for _ in range(n)]
start=None
for i in range(n):
    for j in range(m):
        if matrix[i][j]==1:
            start=(i,j)
            break
    if not(start is None):
        break
stack=[]
stack.append(start)
visited[start[0]][start[1]]=True
directions=[(0,1),(0,-1),(1,0),(-1,0)]
ans=0
while stack:
    x=stack.pop()
    to_add=4
    for dx,dy in directions:
        nx=x[0]+dx
        ny=x[1]+dy
        if 0<=nx<n and 0<=ny<m:
            if matrix[nx][ny]==1:
                to_add-=1
            if not visited[nx][ny] and matrix[nx][ny]==1:
                visited[nx][ny]=True
                stack.append((nx,ny))
    ans+=to_add
print(ans)
