# External reference: http://cs101.openjudge.cn/practice/02796/statistics/
# Accepted submission: 50581104
# Source: http://cs101.openjudge.cn/practice/solution/50581104/
# License: not declared on the submission page; no license is inferred.

l = [int(x) for x in input().split()]
res = 0
for i in l[1:]:
    if i < l[0]:
        res += i
print(res)
