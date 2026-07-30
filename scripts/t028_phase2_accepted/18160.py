# External reference: http://cs101.openjudge.cn/practice/18160/statistics/
# Accepted submission: 52706096
# Source: http://cs101.openjudge.cn/practice/solution/52706096/
# License: not declared on the submission page; no license is inferred.

from collections import deque

t=int(input())#有t组数据

def input_(n,m):
    grid=[]
    for i in range(n+1):
        thelist=list(input().strip())
        grid.append(thelist)
    return grid

def bfs(grid,n,m):
    directions=[(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
    r=0
    for i in range(n+1):
        for j in range(m+1):
            result = 0
            if grid[i][j]=="W":
                result+=1
                grid[i][j]="."
                queue = deque()
                queue.append((i, j))
                while queue:
                    point = queue.popleft()
                    for step in directions:
                        new_i=point[0]+step[0]
                        new_j=point[1]+step[1]
                        if 0<=new_i<n+1 and 0<=new_j<m+1 and grid[new_i][new_j]=="W":
                            queue.append((new_i,new_j))
                            grid[new_i][new_j]="."
                            result+=1
            r=max(r,result)
    return r

for i in range(t):
    n, m = map(int, input().split())  # 接下来有n行，每行有m个字符
    n-=1
    m-=1
    grid=input_(n,m)
    r=bfs(grid,n,m)
    print(r)
