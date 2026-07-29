# External reference: http://cs101.openjudge.cn/practice/01922/statistics/
# Accepted submission: 52492593
# Source: http://cs101.openjudge.cn/practice/solution/52492593/
# License: not declared on the submission page; no license is inferred.

import math

def calc(line,val):
    k=line[0]
    b=line[1]
    x=(val-b)/k
    return math.ceil(x)

while True:
    n=int(input())
    if n==0:
        break
    students=[]
    for _ in range(n):
        students.append(tuple(int(i) for i in input().split()))
    line=[]
    for speed,setoff in students:
        if setoff<0:
            continue
        k=speed
        b=-k*setoff
        line.append((k,b))
    time=float('inf')
    for l in line:
        time=min(time,calc(l,16200))
    print(time)
