# External reference: http://cs101.openjudge.cn/practice/01696/statistics/
# Accepted submission: 43692664
# Source: http://cs101.openjudge.cn/practice/solution/43692664/
# License: not declared on the submission page; no license is inferred.

from math import acos
def f(a,b):
    c,d=vector
    t=(a*c+b*d)/(((a**2+b**2)**0.5)*((c**2+d**2)**0.5))
    return acos(t)
for _ in range(int(input())):
    try:
        n=int(input())
    except:
        n=int(input())
    l=[tuple(map(int,input().split())) for i in range(n)]
    x,y=0,1e9
    for i in range(n):
        if l[i][2]<y:
            y=l[i][2]
    ans=[n]
    vector=(1,0)
    for i in range(n):
        l.sort(key=lambda p:f((p[1]-x),(p[2]-y)))
        ans.append(l[0][0])
        vector=(l[0][1]-x,l[0][2]-y)
        x,y=l[0][1],l[0][2]
        l=l[1:]
    print(*ans)
