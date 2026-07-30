# External reference: http://cs101.openjudge.cn/practice/12557/statistics/
# Accepted submission: 51376050
# Source: http://cs101.openjudge.cn/practice/solution/51376050/
# License: not declared on the submission page; no license is inferred.

v1=list(map(int,input().split('.')))
v2=list(map(int,input().split('.')))
if v2>v1:
    print('.'.join(str(x) for x in v2))
else:
    print('.'.join(str(x) for x in v1))
