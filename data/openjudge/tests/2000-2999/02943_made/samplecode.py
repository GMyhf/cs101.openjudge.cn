# External reference: http://cs101.openjudge.cn/practice/02943/statistics/
# Accepted submission: 52332033
# Source: http://cs101.openjudge.cn/practice/solution/52332033/
# License: not declared on the submission page; no license is inferred.

n=int(input())
lis=[]
for i in range(n):
    x,y=input().split()
    x=int(x)
    lis.append([x,y])
lis.sort()
for i in range(n-1,-1,-1):
    print(lis[i][1])
