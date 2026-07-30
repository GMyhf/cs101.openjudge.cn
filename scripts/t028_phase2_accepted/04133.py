# External reference: http://cs101.openjudge.cn/practice/04133/statistics/
# Accepted submission: 52456037
# Source: http://cs101.openjudge.cn/practice/solution/52456037/
# License: not declared on the submission page; no license is inferred.

d=int(input())
n=int(input())
matrix=[[0 for __ in range(1025)] for _ in range(1025)]
for _ in range(n):
    x,y,val=[int(i) for i in input().split()]
    for i in range(max(0,x-d),min(1025,x+d+1)):
        for j in range(max(0,y-d),min(1025,y+d+1)):
            matrix[i][j]+=val

num=0
cmax=0
for i in range(1025):
    for j in range(1025):
        if matrix[i][j]>cmax:
            cmax=matrix[i][j]
            num=1
        elif matrix[i][j]==cmax:
            num+=1
print(num,cmax)
