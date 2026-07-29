# External reference: http://cs101.openjudge.cn/practice/02793/statistics/
# Accepted submission: 52507570
# Source: http://cs101.openjudge.cn/practice/solution/52507570/
# License: not declared on the submission page; no license is inferred.

from functools import reduce
from math import gcd

def lcm_base(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0

def lcm(*args):
    return reduce(lcm_base, args, 1)

while True:
    a = list(map(int,input().split()))[1:]
    if not a:
        exit()

    l = lcm(*a)

    def exgcd(a,b):
        if b==0:return a,1,0
        g,x,y=exgcd(b,a%b)
        return g,y,x-(a//b*y)

    b = [1]*len(a)
    pre_g = l//a[0]
    for i in range(1,len(a)):
        g,x,y = exgcd(pre_g, l//a[i])
        b[i]=y
        for j in range(0,i):
            b[j]*=x
            b[j]%=l
        pre_g = gcd(pre_g,g)
    for i in range(0,len(a)):
        b[i] *= l//a[i]
        b[i] %= l
    print(' '.join(map(str,b)))
