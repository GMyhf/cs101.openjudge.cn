# External reference: statistics page /practice/28405/
# Accepted submission: 52736793
# Source: http://cs101.openjudge.cn/practice/solution/52736793/
# License: not declared on the submission page; no license is inferred.

n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
d = int(input())
if len(a) <= d:
    print(0)
else:
    l, r = 1, sum(a)
    while l < r:
        m = (l + r) // 2
        cur_tol = 0
        maxn = 0
        day = 0
        for i in range(n):
            maxn = max(maxn, a[i])
            if cur_tol - maxn + a[i] > m:
                maxn = -1
                cur_tol = 0
                day += 1
            cur_tol += a[i]
        if cur_tol > 0:
            day += 1
        if day <= d: # m可行 可继续缩小
            r = m
        else:
            l = m + 1
    print(l)