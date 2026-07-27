# External reference: /practice/29662/statistics/
# Accepted submission: 52727805
# Source: http://cs101.openjudge.cn/practice/solution/52727805/
# License: not declared on the submission page; no license is inferred.

n,m=map(int,input().split())
graph=[[1]*(m+2)]
for i in range(n):
    graph.append([1]+list(map(int,input().split()))+[1])
graph.append([1]*(m+2))
dire=[(0,1),(0,-1),(1,0),(-1,0)]
ans=[[0]*(m+2) for i in range(n+2)]
def dfs(x,y):
    ans[x][y]=1
    for dx,dy in dire:
        nx,ny=x+dx,y+dy
        if 0<=nx<n+1 and 0<=ny<m+1 and ans[nx][ny]==0 and graph[nx][ny]==1:
            dfs(nx,ny)
for i in range(m+2):
    if ans[0][i]==0:
        dfs(0,i)
for i in range(1,n+1):
    if ans[i][0]==0:
        dfs(i,0)
    if ans[i][m+1]==0:
        dfs(i,m+1)
for i in range(m+2):
    if ans[n+1][i]==0:
        dfs(n+1,i)
for k in range(1,n+1):
    print(" ".join(str(i) for i in ans[k][1:m+1]))