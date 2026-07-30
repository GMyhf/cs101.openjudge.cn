# External reference: http://cs101.openjudge.cn/practice/12560/statistics/
# Accepted submission: 51204202
# Source: http://cs101.openjudge.cn/practice/solution/51204202/
# License: not declared on the submission page; no license is inferred.

import copy
def fun(n, m, matrix):
    dp = copy.deepcopy(matrix)
    for i in range(1, n+1):
        for j in range(1, m+1):
            num = matrix[i-1][j-1] + matrix[i-1][j] + matrix[i-1][j+1] + matrix[i][j-1] + matrix[i][j+1] + matrix[i+1][j-1] + matrix[i+1][j] + matrix[i+1][j+1]
            if dp[i][j] == 1:
                if num < 2 or num > 3:
                    dp[i][j] = 0
            elif dp[i][j] == 0:
                if num == 3:
                    dp[i][j] = 1
    return dp
n, m = map(int, input().split())
s = [[0]*(m+2)]
matrix = s + [[0]+[int(x) for x in input().split()]+[0] for _ in range(n)] + s
for i in fun(n, m, matrix)[1:n+1]:
    print(' '.join(map(str, i[1:m+1])))
