# External reference: cs101.openjudge.cn practice/07544 statistics, Accepted solution 51070584.
# Source: http://cs101.openjudge.cn/practice/solution/51070584/
# Statistics: http://cs101.openjudge.cn/practice/07544/statistics/
# License: not declared on submission page; no license inferred
n, m, k = map(int, input().split())
A = [[int(x) for x in input().split()] for _ in range(n)]
B = [[int(x) for x in input().split()] for _ in range(m)]
C = [[0]*k for _ in range(n)]
for i in range(n):
    for j in range(k):
        C[i][j] = sum(A[i][t]*B[t][j] for t in range(m))
for i in range(n):
    print(*C[i])