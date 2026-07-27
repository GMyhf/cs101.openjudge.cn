# External reference: statistics page /practice/22548/
# Accepted submission: 52510538
# Source: http://cs101.openjudge.cn/practice/solution/52510538/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/22548/
# Accepted submission: 52510538
# Source: http://cs101.openjudge.cn/practice/solution/52510538/
# License: not declared on the submission page; no license is inferred.

price=[int(i) for i in input().split()]
upstack=[]
m=0
for p in price:
    while upstack and upstack[-1]>=p:
        upstack.pop()
    upstack.append(p)
    m=max(m,upstack[-1]-upstack[0])
print(m)