# External reference: http://cs101.openjudge.cn/practice/02157/statistics/
# Accepted submission: 45991187
# Source: http://cs101.openjudge.cn/practice/solution/45991187/
# License: not declared on the submission page; no license is inferred.

def valid(i,j):
    if (0<=i)&(0<=j)&(i<h)&(j<w):
        return True
    else:
        return False
tile_free=['.','a','b','c','d','e']
def check(i,j):
    f=False
    if valid(i-1,j):
        if m[i-1][j] in tile_free:
            f=True
    if valid(i+1,j):
        if m[i+1][j] in tile_free:
            f=True
    if valid(i,j-1):
        if m[i][j-1] in tile_free:
            f=True
    if valid(i,j+1):
        if m[i][j+1] in tile_free:
            f=True
    return f
def door_check(i,j):
    f=False
    if valid(i-1,j):
        if m[i-1][j]=='@':
            f=True
    if valid(i+1,j):
        if m[i+1][j]=='@':
            f=True
    if valid(i,j-1):
        if m[i][j-1]=='@':
            f=True
    if valid(i,j+1):
        if m[i][j+1]=='@':
            f=True
    return f
def search(i,j):
    # global m
    if check(i,j)==False:
        return
    if valid(i-1,j):
        if m[i-1][j]=='.':
            m[i-1][j]='@'
            search(i-1,j)
        if m[i-1][j] in ['a','b','c','d','e']:
            key[['a','b','c','d','e'].index(m[i-1][j])]-=1
            m[i-1][j]='@'
            search(i-1,j)
    if valid(i+1,j):
        if m[i+1][j]=='.':
            m[i+1][j]='@'
            search(i+1,j)
        if m[i+1][j] in ['a','b','c','d','e']:
            key[['a','b','c','d','e'].index(m[i+1][j])]-=1
            m[i+1][j]='@'
            search(i+1,j)
    if valid(i,j-1):
        if m[i][j-1]=='.':
            m[i][j-1]='@'
            search(i,j-1)
        if m[i][j-1] in ['a','b','c','d','e']:
            key[['a','b','c','d','e'].index(m[i][j-1])]-=1
            m[i][j-1]='@'
            search(i,j-1)
    if valid(i,j+1):
        if m[i][j+1]=='.':
            m[i][j+1]='@'
            search(i,j+1)
        if m[i][j+1] in ['a','b','c','d','e']:
            key[['a','b','c','d','e'].index(m[i][j+1])]-=1
            m[i][j+1]='@'
            search(i,j+1)
while True:
    h,w=map(int,input().split())
    if h==0 & w==0:
        break
    m=[]
    door=[None,None,None,None,None]
    key=[0,0,0,0,0]
    for i in range(h):
        m.append(list(input()))
        for j in range(w):
            if m[i][j]=='S':
                i0=i
                j0=j
                m[i][j]='@'
            if m[i][j]=='G':
                i1=i
                j1=j
                m[i][j]='.'
            if m[i][j] in ['A','B','C','D','E']:
                door[['A','B','C','D','E'].index(m[i][j])]=(i,j)
            if m[i][j] in ['a','b','c','d','e']:
                key[['a','b','c','d','e'].index(m[i][j])]+=1
    search(i0,j0)
    key_p=[]
    while key_p!=key:
        key_p=key
        for _ in range(5):
            if (key[_]==0)&(door[_]!=None):
                if door_check(door[_][0],door[_][1])==True:
                    m[door[_][0]][door[_][1]]='@'
                    search(door[_][0],door[_][1])
    if m[i1][j1]=='@':
        print('YES')
    else:
        print('NO')
