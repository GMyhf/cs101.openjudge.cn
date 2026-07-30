# External reference: http://cs101.openjudge.cn/practice/30550/statistics/
# Accepted submission: 52740200
# Source: http://cs101.openjudge.cn/practice/solution/52740200/
# License: not declared on the submission page; no license is inferred.

import math
import sys
N = int(input())
triples = []
for m in range(2,int(math.sqrt(N))+1):
    for n in range(1,m):
        if math.gcd(m,n) != 1 or (m % 2) == (n % 2):
            continue
        a0 = m*m - n*n
        b0 = 2*m*n
        c0 = m*m + n*n
        if a0 > b0:
            a0,b0 = b0,a0 # 确保a0<b0
        k = 1
        while k*c0 <= N:
            a,b,c = k*a0,k*b0,k*c0
            triples.append((a<<40)|(b<<20)|c)# 使用位运算，2**20>10**6
            k += 1
triples.sort()
res = []
mask = (1 << 20) - 1
for i,tri in enumerate(triples):
    if i == 0 or tri != triples[i-1]:# 去重
        sys.stdout.write(f"{tri>>40} {(tri>>20)&mask} {tri&mask} ")
