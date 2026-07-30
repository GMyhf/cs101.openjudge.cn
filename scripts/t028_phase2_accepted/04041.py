# External reference: http://cs101.openjudge.cn/practice/04041/statistics/
# Accepted submission: 51370741
# Source: http://cs101.openjudge.cn/practice/solution/51370741/
# License: not declared on the submission page; no license is inferred.

m, k = map(int, input().split())
a = [list(map(int, input().split())) for i in range(m)]
k1, n = map(int, input().split())
b = [list(map(int, input().split())) for i in range(k)]

if k == k1:
    for j in range(n):
        print(''.join([f"{sum([a[i][l] * b[l][j] for l in range(k)]):5}" for i in range(m)]))
else:
    for j in range(k):
        print(''.join([f"{a[i][j]:5}" for i in range(m)]))
