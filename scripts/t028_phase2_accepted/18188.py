# External reference: http://cs101.openjudge.cn/practice/18188/statistics/
# Accepted submission: 51284215
# Source: http://cs101.openjudge.cn/practice/solution/51284215/
# License: not declared on the submission page; no license is inferred.

M, N = map(int, input().split())
image = []
for i in range(M):
    row = list(map(int, input().split()))
    image.append(row)
result = [[0] * N for _ in range(M)]
for i in range(M):
    for j in range(N):
        t = 0
        s = 0
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                ni = i + x
                nj = j + y
                if 0 <= ni < M and 0 <= nj < N:
                    t += image[ni][nj]
                    s += 1
        result[i][j] = t//s
for i in result:
    print(' '.join(map(str, i)))
