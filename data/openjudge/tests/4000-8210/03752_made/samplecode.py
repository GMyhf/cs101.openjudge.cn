# T-004-r3 reference implementation
import sys
from collections import deque
a=sys.stdin.read().split(); r,c=map(int,a[:2]); g=a[2:]; d=[[-1]*c for _ in range(r)]
q=deque([(0,0)]); d[0][0]=1
while q:
    x,y=q.popleft()
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        u,v=x+dx,y+dy
        if 0<=u<r and 0<=v<c and g[u][v]=="." and d[u][v]<0:
            d[u][v]=d[x][y]+1; q.append((u,v))
print(d[-1][-1])