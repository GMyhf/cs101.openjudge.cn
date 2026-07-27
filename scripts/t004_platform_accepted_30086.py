# External reference: /practice/30086/statistics/
# Accepted submission: 52211740
# Source: http://cs101.openjudge.cn/practice/solution/52211740/
# License: not declared on the submission page; no license is inferred.

n,d=[int(i) for i in input().split()]
l=[int(i) for i in input().split()]
l.sort()
status="Yes"
for i in range(n):
    a=l[2*i]
    b=l[2*i+1]
    if abs(a-b)>d:
        status="No"
        break
print(status)