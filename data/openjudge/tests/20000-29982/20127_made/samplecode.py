# External reference: http://cs101.openjudge.cn/practice/20127/statistics/
# Accepted submission: 47975272
# Source: http://cs101.openjudge.cn/practice/solution/47975272/
# License: not declared on the submission page; no license is inferred.

def dfs(x,y,k):
    if mp[x][y]==1:
        return k
    tem=[float('inf')]
    for i,j in [(1,0),(-1,0),(0,1),(0,-1)]:
        if vd[x+i][y+j] and mp[x+i][y+j]!=2:
            vd[x+i][y+j]=False
            if mp[x+i][y+j]==3:
                tem.append(dfs(x+i,y+j,k))
            else:
                tem.append(dfs(x+i,y+j,k+1))
            vd[x+i][y+j]=True
    return min(tem)

m,n=map(int,input().split())
mp=[[2 for j in range(n+2)]for i in range(m+2)]
for i in range(1,m+1):
    tem=list(map(int,input().split()))
    for j in range(1,n+1):
        mp[i][j]=tem[j-1]
vd=[[True for j in range(n+2)]for i in range(m+2)]
ans=dfs(1,1,0)
if ans==float('inf'):
    print('NO')
else:
    print(dfs(1,1,0))
