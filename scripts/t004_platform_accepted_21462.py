# External reference: statistics page /practice/21462/
# Accepted submission: 52213098
# Source: http://cs101.openjudge.cn/practice/solution/52213098/
# License: not declared on the submission page; no license is inferred.

n=int(input())
matrix=[]
for i in range(n):
    matrix.append(list(map(int,input().split())))
directions=[(1,0),(0,1),(-1,0),(0,-1)]
x,y=0,0
ans=''
d=0
dx,dy=1,0
visited=set()
while matrix[x][y]!=0:
    ans+=chr(matrix[x][y])
    visited.add((x,y))
    nx,ny=x+dx,y+dy
    if (not 0<=nx<n) or (not 0<=ny<n) or (nx,ny) in visited:
        d=(d+1)%4
        dx,dy=directions[d]
        x,y=x+dx,y+dy
    else:
        x,y=nx,ny
print(ans)