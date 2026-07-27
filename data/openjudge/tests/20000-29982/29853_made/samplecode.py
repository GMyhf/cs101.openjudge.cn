# External reference: /practice/29853/statistics/
# Accepted submission: 52288129
# Source: http://cs101.openjudge.cn/practice/solution/52288129/
# License: not declared on the submission page; no license is inferred.

n=int(input())
a=[int(i) for i in input().split()]
b=[int(i) for i in input().split()]
minb=min(b)
maxb=max(b)
calc=[max(abs(minb-i),abs(maxb-i)) for i in a]
print(min(calc))