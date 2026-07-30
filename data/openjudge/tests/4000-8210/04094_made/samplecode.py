# External reference: http://cs101.openjudge.cn/practice/04094/statistics/
# Accepted submission: 50952933
# Source: http://cs101.openjudge.cn/practice/solution/50952933/
# License: not declared on the submission page; no license is inferred.

n, s = map(int, input().split())
res = 0
for _ in range(n):
    t, v = map(int, input().split())
    T = t+s/v
    res = max(res, T)
print(int(res))
