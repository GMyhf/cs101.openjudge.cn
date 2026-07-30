# External reference: http://cs101.openjudge.cn/practice/29947/statistics/
# Accepted submission: 52610953
# Source: http://cs101.openjudge.cn/practice/solution/52610953/
# License: not declared on the submission page; no license is inferred.

import sys
L,M=map(int,input().split())
res=[]
for _ in range(M):
    cut=list(map(int,input().split()))
    res.append(cut)
res.sort()
st=-sys.maxsize
ed=-sys.maxsize
ans=0
for i in res:
    if i[0]==st:
        ed=i[1]
    elif i[0]<=ed:
        ed=max(i[1],ed)
        ans-=1
    else:
        ans+=ed-st
        st=i[0]
        ed=i[1]
ans+=ed-st
print(L+1-ans-M)
