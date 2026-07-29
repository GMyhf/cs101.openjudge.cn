# External reference: http://cs101.openjudge.cn/routine/02795/statistics/
# Accepted submission: 47766167
# Source: http://cs101.openjudge.cn/routine/solution/47766167/
# License: not declared on the submission page; no license is inferred.

k=int(input())
for _ in range(k):
    w=int(input())
    s=int(input())
    l=list(map(int,input().split()))
    lis=[]
    i=0
    for _ in range(s):
        a=l[i]
        b=l[i+1]
        c=b/a
        lis.append((c,a,b))
        i+=2
    lis.sort()
    li=lis[::-1]
    e=0
    ans=0
    for k in li:
        if e+k[1]<=w:
            ans+=k[2]
            e+=k[1]
        else:
            d=w-e
            ans+=k[0]*d
            break
    print(f'{ans:.2f}')
