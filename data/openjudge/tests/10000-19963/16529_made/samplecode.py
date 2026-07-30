# External reference: http://cs101.openjudge.cn/practice/16529/statistics/
# Accepted submission: 52513767
# Source: http://cs101.openjudge.cn/practice/solution/52513767/
# License: not declared on the submission page; no license is inferred.

n=int(input())
p=list(map(float,input().split()))
minp=p[0]
maxpro=1
for i in range(n):
    pro=p[i]/minp
    maxpro=max(maxpro,pro)
    if p[i]<minp:
        minp=p[i]
ans=100*maxpro
print(f'{ans:.2f}')
