# External reference: http://cs101.openjudge.cn/practice/04100/statistics/
# Accepted submission: 52530757
# Source: http://cs101.openjudge.cn/practice/solution/52530757/
# License: not declared on the submission page; no license is inferred.

t=int(input())
for _ in range(t):
    n=int(input())
    lis=[]
    for i in range(n):
        lis.append(list(map(int,input().split())))
    lis=sorted(lis,key=lambda x:x[1])
    las=-1
    ans=0
    for i in range(n):
        if lis[i][0]>las:
            ans+=1
            las=lis[i][1]
    print(ans)
