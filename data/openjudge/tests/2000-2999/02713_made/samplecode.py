# External reference: http://cs101.openjudge.cn/practice/02713/statistics/
# Accepted submission: 52515343
# Source: http://cs101.openjudge.cn/practice/solution/52515343/
# License: not declared on the submission page; no license is inferred.

n = int(input())

pic = [list(map(int, input().split())) for _ in range(n)]
found = False
cnt = 0
line = 0
for i in range(n):
    num = pic[i].count(0)
    if num > 0 and not found:
        line = num
        found = True
    if num == 2 and found:
        cnt += 1

s = (line - 2) * cnt
print(s)
