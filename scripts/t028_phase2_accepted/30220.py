# External reference: http://cs101.openjudge.cn/practice/30220/statistics/
# Accepted submission: 52702594
# Source: http://cs101.openjudge.cn/practice/solution/52702594/
# License: not declared on the submission page; no license is inferred.

import sys
def dp(i,j,used,not_used,graph):
    if graph[i][j]>=0:
        cur=graph[i][j]
        not_used[i][j]=cur
        if i>0 and j>0:
            used[i][j]=cur+max(used[i-1][j],used[i][j-1])
            not_used[i][j]+=max(not_used[i-1][j],not_used[i][j-1])
        elif i>0:
            used[i][j]=cur+used[i-1][j]
            not_used[i][j]+=not_used[i-1][j]
        elif j>0:
            used[i][j]=cur+used[i][j-1]
            not_used[i][j]+=not_used[i][j-1]
    else:
        cur = graph[i][j]
        if i==0 and j==0:
            used[i][j]=-cur
            not_used[i][j]=cur
        elif j==0:
            used[i][j]=max(used[i-1][j]+cur,not_used[i-1][j]-cur)
            not_used[i][j]=cur+not_used[i-1][j]
        elif i==0:
            used[i][j]=max(used[i][j-1]+cur,not_used[i][j-1]-cur)
            not_used[i][j]=cur+not_used[i][j-1]
        else:
            used[i][j]=max(used[i-1][j]+cur,not_used[i-1][j]-cur,used[i][j-1]+cur,not_used[i][j-1]-cur)
            not_used[i][j]=cur+max(not_used[i-1][j],not_used[i][j-1])
def main():
    data=iter(sys.stdin.read().strip().split())
    N,M=int(next(data)),int(next(data))
    not_used=[[float('-inf')]*M for _ in range(N)]
    used=[[float('-inf')]*M for _ in range(N)]
    graph=[[int(next(data)) for _ in range(M)] for _ in range(N)]
    for i in range(N):
        for j in range(M):
            dp(i,j,used,not_used,graph)
    print(max(used[N-1][M-1],not_used[N-1][M-1]))
if __name__ == '__main__':
    main()
