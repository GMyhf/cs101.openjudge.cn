# External reference: statistics page /practice/21532/
# Accepted submission: 52201278
# Source: http://cs101.openjudge.cn/practice/solution/52201278/
# License: not declared on the submission page; no license is inferred.

n=int(input())
i=6
while n%i!=0:
    i+=1
print(n//i)