# External reference: http://cs101.openjudge.cn/practice/02313/statistics/
# Accepted submission: 43897847
# Source: http://cs101.openjudge.cn/practice/solution/43897847/
# License: not declared on the submission page; no license is inferred.

n=int(input())
a=[int(input()) for _ in range(n)]
b=[0]*n
b[0]=a[0];b[-1]=a[-1]
for i in range(1,n-1):
    inf = max(a[i],b[i-1])
    sup=min(a[i],b[i-1])
    if a[i+1]>inf:b[i]=inf
    elif a[i+1]<sup:b[i]=sup
    else:b[i]=a[i+1]
ans=0
for i in range(n-1):
    ans+=abs(a[i]-b[i])+abs(b[i+1]-b[i])
print(ans)
