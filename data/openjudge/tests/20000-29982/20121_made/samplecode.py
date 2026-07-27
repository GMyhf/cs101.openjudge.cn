# External reference: statistics page /practice/20121/
# Accepted submission: 52495947
# Source: http://cs101.openjudge.cn/practice/solution/52495947/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/20121 statistics, Accepted solution 52495947.
# Source: http://cs101.openjudge.cn/practice/solution/52495947/
# Statistics: http://cs101.openjudge.cn/practice/20121/statistics/
# License: not declared on submission page; no license inferred
n=int(input())
lis=[]
for i in range(n):
    lis.append(input().split())
vis=[[False for _ in range(n)] for _ in range(n)]
ans=""
now=0
x=0
y=-1
dx=0
dy=1
for _ in range(n*n):
    if 0<=x+dx<=n-1 and 0<=y+dy<=n-1 and not vis[x+dx][y+dy]:
        vis[x+dx][y+dy]=True
        x=x+dx
        y=y+dy
        ans=ans+lis[x][y]
        continue
    else:
        dx,dy=dy,-dx
        vis[x+dx][y+dy]=True
        x=x+dx
        y=y+dy
        ans=ans+lis[x][y]
        continue
print(ans)
