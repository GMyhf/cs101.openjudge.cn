# External reference: http://cs101.openjudge.cn/practice/27638/statistics/
# Accepted submission: 52829461
# Source: http://cs101.openjudge.cn/practice/solution/52829461/
# License: not declared on the submission page; no license is inferred.

n=int(input())
l=[-1]*n
r=[-1]*n
fa=[-1]*n
for i in range(n):
    a,b=map(int,input().split())
    l[i]=a
    r[i]=b
    if a!=-1:
        fa[a]=i
    if b!=-1:
        fa[b]=i
rt=0
for i in range(n):
    if fa[i]==-1:
        rt=i
h=0
cnt=0
def dfs(u,d):
    global h,cnt
    if l[u]==-1 and r[u]==-1:
        cnt+=1
        if d>h:
            h=d
        return
    if l[u]!=-1:
        dfs(l[u],d+1)
    if r[u]!=-1:
        dfs(r[u],d+1)
dfs(rt,0)
print(h,cnt)
