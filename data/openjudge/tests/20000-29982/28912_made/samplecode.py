# External reference: http://cs101.openjudge.cn/practice/28912/statistics/
# Accepted submission: 50926112
# Source: http://cs101.openjudge.cn/practice/solution/50926112/
# License: not declared on the submission page; no license is inferred.

import sys
import math
from functools import lru_cache
n,M=map(int,sys.stdin.readline().split())
data=sys.stdin.read().split()
ai=[int(data[i]) for i in range(0,3*n,3)]
bi=[int(data[i]) for i in range(1,3*n,3)]
ci=[int(data[i]) for i in range(2,3*n,3)]
@lru_cache(maxsize=None)
def f(x):
    return int(sum(ci[i]*abs(ai[i]*x+bi[i]) for i in range(n)))
min_fx,max_fx=min(f(0),f(M)),max(f(0),f(M))
points=[y for i in range(n) if ai[i]!=0 and M>=(y:=-bi[i]/ai[i])>=0]
m=len(points)
if m==0:
    print(max_fx,min_fx)
    exit()
points.sort()
min_fx=min(f(math.floor(points[0])),min_fx,f(math.ceil(points[-1])))
max_fx=max(f(math.floor(points[0])),max_fx,f(math.ceil(points[-1])))
for point in points:
    min_fx=min(min_fx,f(point))
    max_fx=max(max_fx,f(point))
print(max_fx,min_fx)
