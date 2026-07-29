# External reference: http://cs101.openjudge.cn/practice/02992/statistics/
# Accepted submission: 50604307
# Source: http://cs101.openjudge.cn/practice/solution/50604307/
# License: not declared on the submission page; no license is inferred.

n = int(input())
stu = 1
max_ = 0
for i in range(1, n+1):
    li = [int(x) for x in input().split()]
    num = li.count(3)
    if num > max_:
        max_ = num
        stu = i
print(stu)
