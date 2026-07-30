# External reference: http://cs101.openjudge.cn/practice/18106/statistics/
# Accepted submission: 52526886
# Source: http://cs101.openjudge.cn/practice/solution/52526886/
# License: not declared on the submission page; no license is inferred.

n=int(input())
matrix=[[0]*n for i in range(n)]
ptr=(0,0)
directions=[(0,1),(1,0),(0,-1),(-1,0)]
p=0
for i in range(1,n**2+1):
    matrix[ptr[0]][ptr[1]]=i
    nptr=(ptr[0]+directions[p][0],ptr[1]+directions[p][1])
    if nptr[0]>=n or nptr[0]<0 or nptr[1]>=n or nptr[1]<0:
        p=(p+1)%4
        nptr=(ptr[0]+directions[p][0],ptr[1]+directions[p][1])
    elif matrix[nptr[0]][nptr[1]]!=0:
        p=(p+1)%4
        nptr=(ptr[0]+directions[p][0],ptr[1]+directions[p][1])
    ptr=nptr
for i in matrix:
    print(*i)
