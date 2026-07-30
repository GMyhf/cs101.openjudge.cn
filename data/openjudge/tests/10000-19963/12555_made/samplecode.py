# External reference: http://cs101.openjudge.cn/practice/12555/statistics/
# Accepted submission: 47939111
# Source: http://cs101.openjudge.cn/practice/solution/47939111/
# License: not declared on the submission page; no license is inferred.

import math
n=int(input())
lis=sorted(map(float,input().split()))
def f(n,i):
    a=(n-1)*i/4+1
    if int(a)==a:
        return lis[int(a)-1]
    h1=math.floor(a)
    h2=math.ceil(a)
    dh=a-h1
    dx=lis[h2-1]-lis[h1-1]
    return lis[h1-1]+dh*dx
for i in range(1,4):
    print(f'{f(n,i):.2f}')
