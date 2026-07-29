# External reference: http://cs101.openjudge.cn/practice/03237/statistics/
# Accepted submission: 50653280
# Source: http://cs101.openjudge.cn/practice/solution/50653280/
# License: not declared on the submission page; no license is inferred.

n = int(input())
for _ in range(n):
    a = int(input())
    if a % 2 == 1:
        print(0, 0)
    else:
        print((a+2)//4, a//2)
