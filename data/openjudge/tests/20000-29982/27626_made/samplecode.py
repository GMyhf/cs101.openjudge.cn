# External reference: http://cs101.openjudge.cn/practice/27626/statistics/
# Accepted submission: 52701690
# Source: http://cs101.openjudge.cn/practice/solution/52701690/
# License: not declared on the submission page; no license is inferred.

n=int(input())
ans=0
if n==1:
    print(1)
elif n==2:
    print(2)
else:
    a=1
    b=2
    h=2
    while True:
        a,b=b,a+b+1
        if b>n:
            print(h)
            break
        h+=1
