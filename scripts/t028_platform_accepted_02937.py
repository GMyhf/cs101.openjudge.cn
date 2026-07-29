# External reference: http://cs101.openjudge.cn/practice/02937/statistics/
# Accepted submission: 50584040
# Source: http://cs101.openjudge.cn/practice/solution/50584040/
# License: not declared on the submission page; no license is inferred.

N = int(input())
mat = []
for _ in range(N):
    l = [int(x) for x in input().split()]
    mat.append(l)
res = 0
for i in range(1, N-1):
    for j in range(1, N-1):
        if mat[i][j] <= min(mat[i][j-1], mat[i][j+1], mat[i-1][j], mat[i+1][j])-50:
            res += 1
print(res)
