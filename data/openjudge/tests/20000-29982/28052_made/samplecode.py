# External reference: http://cs101.openjudge.cn/practice/28052/statistics/
# Accepted submission: 44675005
# Source: http://cs101.openjudge.cn/practice/solution/44675005/
# License: not declared on the submission page; no license is inferred.

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:51:47 2024

@author: Lenovo
"""

from collections import deque
def bfs(color):
    move=[(0,-1),(1,0),(1,1),(0,1),(-1,0),(-1,-1)]
    q=deque()
    if color==1:
        for i in range(n):
            if matrix[0][i]==0:
                d[0][i]=1
            elif matrix[0][i]==1:
                d[0][i]=0
            q.append((d[0][i],0,i))
    else:
        for i in range(n):
            if matrix[i][0]==0:
                d[i][0]=1
            elif matrix[i][0]==2:
                d[i][0]=0
            q.append((d[i][0],i,0))
    while q:
        step,x,y=q.popleft()
        for i in range(6):
            dx,dy=x+move[i][0],y+move[i][1]
            if dx<0 or dx>=n or dy<0 or dy>=n:
                continue
            if matrix[dx][dy]!=color and matrix[dx][dy]!=0:
                continue
            if d[dx][dy]>d[x][y]+int(matrix[dx][dy]!=color):
                d[dx][dy]=d[x][y]+int(matrix[dx][dy]!=color)
                q.append((d[dx][dy],dx,dy))
    if color==2:
        ans=float("inf")
        for i in range(n):
            ans=min(ans,d[i][-1])
    else:
        ans=min(d[-1])
    return ans if ans!=float("inf") else -1

n=int(input())
matrix=[list(map(int,input().split())) for i in range(n)]
d=[[float("inf") for i in range(n)] for i in range(n)]
count1=count2=0
for i in range(n):
    for j in range(n):
        count1+=int(matrix[i][j]==1)
        count2+=int(matrix[i][j]==2)
if count1<=count2:
    ans=bfs(1)
else:
    ans=bfs(2)
print(ans)
