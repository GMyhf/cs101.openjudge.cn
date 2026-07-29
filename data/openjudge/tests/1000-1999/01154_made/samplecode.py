# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1154: LETTERS
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01154/
# License: not declared; no license is inferred.
R,C=map(int,input().split())
grid=[]
for _ in range(R):
    grid.append(list(input()))
condition=[0]*26
def r(a):
    return ord(a)-65
def check(x,y):
    return 0<=x<=R-1 and 0<=y<=C-1
s=0
d=[[1,0],[-1,0],[0,1],[0,-1]]
def dfs(x,y,n):
    flag=True
    for i in range(4):
        x1=x+d[i][0]
        y1=y+d[i][1]
        if check(x1,y1):
            a=r(grid[x1][y1])
            if condition[a]==0:
                flag=False
                condition[a]=1
                dfs(x1,y1,n+1)
                condition[a]=0
    if flag:
        global s
        s=max(s,n)
        return
condition[r(grid[0][0])]=1
dfs(0,0,1)
print(s)
