# External reference: http://cs101.openjudge.cn/practice/01307/statistics/
# Accepted submission: 43699892
# Source: http://cs101.openjudge.cn/practice/solution/43699892/
# License: not declared on the submission page; no license is inferred.

h=1
while 1:
    while 1:
        k=input()
        if k:break
    r,c,a,b,e,f=map(int,k.split())
    if r==0:
        break
    print('Maze %d'%h);h+=1;print()
    while 1:
        k=input()
        if k:break
    wall=[list(map(int,k.split()))]+[list(map(int,input().split())) for _ in range(r-1)]
    input()
    l=[[0]*c for _ in range(r)]
    l[a-1][b-1]=1
    cur=(a,b)
    while 1:
        if cur==(e,f):
            break
        ff=0
        for direction in [(0,-1),(-1,0),(0,1),(1,0),]:
            x,y=direction
            if not (1<=cur[0]+x<=r and 1<=cur[1]+y<=c):
                continue
            if (x,y)==(-1,0) and wall[cur[0]-2][cur[1]-1] in {2,3}:
                continue
            if (x,y)==(0,1) and wall[cur[0]-1][cur[1]-1] in {1,3}:
                continue
            if (x,y)==(1,0) and wall[cur[0]-1][cur[1]-1] in {2,3}:
                continue
            if (x,y)==(0,-1) and wall[cur[0]-1][cur[1]-2] in {1,3}:
                continue
            if l[cur[0]+x-1][cur[1]+y-1]!=-1:
                if l[cur[0]+x-1][cur[1]+y-1]==0:
                    ff=1
                    l[cur[0]+x-1][cur[1]+y-1]=l[cur[0]-1][cur[1]-1]+1
                    cur=(cur[0]+x,cur[1]+y)
                    break
        if ff==0:
            for direction in [(-1,0),(0,1),(1,0),(0,-1)]:
                x,y=direction
                if not (1<=cur[0]+x<=r and 1<=cur[1]+y<=c):
                    continue
                if (x,y)==(-1,0) and wall[cur[0]-2][cur[1]-1] in {2,3}:
                    continue
                if (x,y)==(0,1) and wall[cur[0]-1][cur[1]-1] in {1,3}:
                    continue
                if (x,y)==(1,0) and wall[cur[0]-1][cur[1]-1] in {2,3}:
                    continue
                if (x,y)==(0,-1) and wall[cur[0]-1][cur[1]-2] in {1,3}:
                    continue
                t=l[cur[0]+x-1][cur[1]+y-1]
                if t!=-1 and t==l[cur[0]-1][cur[1]-1]-1:
                    l[cur[0]-1][cur[1]-1]=-1
                    cur=(cur[0]+x,cur[1]+y)
                    break
    res=['']*(2*r+1)
    res[0]='+---'*c+'+'
    res[-1]=res[0]
    for i in range(r):
        t=2*i+1
        res[t]='|'
        for j in range(c):
            if l[i][j]==-1:res[t]+='???'
            elif l[i][j]==0:res[t]+=' '*3
            else:res[t]+=' '*(3-len(str(l[i][j])))+str(l[i][j])
            if wall[i][j] in {1,3} or j==c-1:res[t]+='|'
            else:res[t]+=' '
    for i in range(1,r):
        t=2*i
        res[t]='+'
        for j in range(c):
            if wall[i-1][j] in {2,3}:
                res[t]+='---'
            else:
                res[t]+='   '
            res[t]+='+'
    for u in res:
        print(u)
    print('\n')
