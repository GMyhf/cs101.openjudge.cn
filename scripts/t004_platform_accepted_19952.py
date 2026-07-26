# External reference: cs101.openjudge.cn practice/19952 statistics, Accepted solution 52328950.
# Source: http://cs101.openjudge.cn/practice/solution/52328950/
# Statistics: http://cs101.openjudge.cn/practice/19952/statistics/
# License: not declared on submission page; no license inferred
a=[0 for i in range(201)]
b=[0 for i in range(201)]
a[1]=2
b[1]=1
for k in range(2,201):
    a[k]=2*a[k-1]+2*b[k-1]
    b[k]=a[k-1]
t=int(input())
for i in range(t):
    n=int(input())
    print(a[n]+b[n])
