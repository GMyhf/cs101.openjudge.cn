# External reference: http://cs101.openjudge.cn/practice/27103/statistics/
# Accepted submission: 51527453
# Source: http://cs101.openjudge.cn/practice/solution/51527453/
# License: not declared on the submission page; no license is inferred.

N, M = map(int, input().split())
l = [int(x) for x in input().split()]
res = 0
s = set()
for i in l:
    s.add(i)
    if len(s) == M:
        res += 1
        s.clear()
print(res+1)
