# External reference: http://cs101.openjudge.cn/practice/18224/statistics/
# Accepted submission: 52847431
# Source: http://cs101.openjudge.cn/practice/solution/52847431/
# License: not declared on the submission page; no license is inferred.

m=int(input())
l=map(int,input().split())
for i in l:
    for a in range(1,int(i**0.5)+1):
        f=0
        for b in range(1,int(i**0.5)+1):
            if a*a+b*b==i:
                print(bin(i),oct(i),hex(i))
                f=1
                break
        if f:
            break
