# External reference: statistics page /practice/19493/
# Accepted submission: 43122575
# Source: http://cs101.openjudge.cn/practice/solution/43122575/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/19493 statistics, Accepted solution 43122575.
# Source: http://cs101.openjudge.cn/practice/solution/43122575/
# Statistics: http://cs101.openjudge.cn/practice/19493/statistics/
# License: not declared on submission page; no license inferred
m=int(input())
for _ in range(m):
    l=list(map(float,input().split()))
    t=str(l[0])
    if t[-2]=='.':
        flag=1
    else:
        flag=2
    ans=[]
    for i in range(len(l)-4):
        c=sum(l[i:i+5])/5
        ans.append(round(c,flag))
    print(*ans)
