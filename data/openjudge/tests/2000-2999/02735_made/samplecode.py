# External reference: http://cs101.openjudge.cn/practice/02735/statistics/
# Accepted submission: 51866473
# Source: http://cs101.openjudge.cn/practice/solution/51866473/
# License: not declared on the submission page; no license is inferred.

a=list(map(int,list(input())))
x=0
s=0
while a:
    s+=a.pop()*8**x
    x+=1
print(s)
