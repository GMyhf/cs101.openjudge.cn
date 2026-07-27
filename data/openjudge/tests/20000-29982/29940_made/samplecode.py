# External reference: /practice/29940/statistics/
# Accepted submission: 52265911
# Source: http://cs101.openjudge.cn/practice/solution/52265911/
# License: not declared on the submission page; no license is inferred.

n=int(input())
l=[int(i) for i in input().split()]
result=0
min_result=0
for i in l:
    result+=i
    min_result=min(min_result,result)
if (min_result>=0):
    print(1)
else:
    print(1-min_result)