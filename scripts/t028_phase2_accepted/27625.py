# External reference: http://cs101.openjudge.cn/practice/27625/statistics/
# Accepted submission: 52701621
# Source: http://cs101.openjudge.cn/practice/solution/52701621/
# License: not declared on the submission page; no license is inferred.

n=int(input())
a=1
b=2
if n==1:
    print(1)
elif n==2:
    print(2)
else:
    for i in range(n-2):
        a,b=b,a+b+1
    print(b)
