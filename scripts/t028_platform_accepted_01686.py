# External reference: http://cs101.openjudge.cn/practice/01686/statistics/
# Accepted submission: 48613173
# Source: http://cs101.openjudge.cn/practice/solution/48613173/
# License: not declared on the submission page; no license is inferred.

from random import random
def check(s1,s2):
    for _ in range(10):
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random(), random()
        if abs(eval(s1)-eval(s2))>0.000001:
            return False
    return True
n=int(input())
for _ in range(n):
    s1=input()
    s2=input()
    print("YES" if check(s1,s2) else "NO")
