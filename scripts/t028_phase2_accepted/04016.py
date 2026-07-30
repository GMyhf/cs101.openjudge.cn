# External reference: http://cs101.openjudge.cn/practice/04016/statistics/
# Accepted submission: 50765228
# Source: http://cs101.openjudge.cn/practice/solution/50765228/
# License: not declared on the submission page; no license is inferred.

N = int(input())
l = []
for i in range(N):
    num, grade = map(int, input().split())
    l.append((grade, i, num))
l.sort(key = lambda x: (-x[0], x[1]))
for i in l:
    print(i[2])
