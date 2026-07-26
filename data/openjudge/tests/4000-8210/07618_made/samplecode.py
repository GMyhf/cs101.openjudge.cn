# External reference: statistics page /practice/07618/
# Accepted submission: 52517208
# Source: http://cs101.openjudge.cn/practice/solution/52517208/
# License: not declared on the submission page; no license is inferred.

n=int(input())
oldage=[]
teens=[]
for _ in range(n):
    name,age=input().split()
    age=int(age)
    if age>=60:
        oldage.append((name,age))
    else:
        teens.append((name,age))
oldage.sort(reverse=True,key=lambda x:x[1])
for name, age in oldage:
    print(name)
for name, age in teens:
    print(name)