# External reference: http://cs101.openjudge.cn/practice/25572/statistics/
# Accepted submission: 51542096
# Source: http://cs101.openjudge.cn/practice/solution/51542096/
# License: not declared on the submission page; no license is inferred.

n=int(input())
grid=[]
start=[]
target=[]
for i in range(n):
    lst=list(map(int,input().split()))
    for j in range(n):
        if lst[j]==5:
            if not start:
                lst[j]=2
            start.append((i,j))
        elif lst[j]==9:
            target.append((i,j))
    grid.append(lst)
from _collections import deque
queue=deque()
queue.append(start)
def valid_location(i_1,j_1,i_2,j_2,grid):
    n=len(grid)
    res=[]
    for x_1,y_1,x_2,y_2 in [(i_1+1,j_1,i_2+1,j_2),(i_1,j_1+1,i_2,j_2+1),(i_1-1,j_1,i_2-1,j_2),(i_1,j_1-1,i_2,j_2-1)]:
        if 0<=x_1<n and 0<=y_1<n and 0<=x_2<n and 0<=y_2<n:
            if grid[x_1][y_1]!=1 and grid[x_2][y_2]!=1:
                if grid[x_1][y_1]!=2:
                    res.append([(x_1,y_1),(x_2,y_2)])
    return res
check=False
while queue:
    location_1,location_2=queue.popleft()
    i_1,j_1=location_1
    i_2,j_2=location_2
    if (i_1,j_1)==target[0] or (i_2,j_2)==target[0]:
        check=True
        break
    for (x_1,y_1),(x_2,y_2) in valid_location(i_1,j_1,i_2,j_2,grid):
        queue.append([(x_1,y_1),(x_2,y_2)])
        grid[x_1][y_1]=2
if check:
    print("yes")
else:
    print("no")
