# External reference: http://cs101.openjudge.cn/practice/18177/statistics/
# Accepted submission: 47978840
# Source: http://cs101.openjudge.cn/practice/solution/47978840/
# License: not declared on the submission page; no license is inferred.

import math

n,d=map(int,input().split())
f = [list(map(int,input().split())) for _ in range(n)]
def w(m,i,j):
    g = [f[i][s]-f[j][s] for s in range(m)]
    p = sum(g)/m
    q = math.sqrt(sum([(index-p)**2 for index in g])/m)
    s = f[i][m]-f[j][m]
    if s>p:
        N = (s-p)//q
        return N*(f[i][m]-f[i][m+1]+f[j][m+1]-f[j][m])
    else:
        N = (p-s)//q
        return -N * (f[i][m] - f[i][m + 1] + f[j][m + 1] - f[j][m])
total=[]
for i in range(n):
    for j in range(i+1,n):
        res=0
        for m in range(3,d-1):
            res+=w(m,i,j)
        total.append((i,j,res))
i,j,n=max(total,key=lambda x: (x[2],x[0],x[1]))
n = int(n)
print(*[i+1,j+1,n])
