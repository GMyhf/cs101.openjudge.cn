# External reference: cs101.openjudge.cn practice/08167 statistics, Accepted solution 51154035.
# Source: http://cs101.openjudge.cn/practice/solution/51154035/
# Statistics: http://cs101.openjudge.cn/practice/08167/statistics/
# License: not declared on submission page; no license inferred
import copy
n, m = map(int, input().split())
matrix = [[int(x) for x in input().split()] for _ in range(n)]
mat = copy.deepcopy(matrix)
for i in range(1, n-1):
    for j in range(1, m-1):
        mat[i][j] = round((matrix[i][j]+matrix[i][j-1]+matrix[i-1][j]+matrix[i+1][j]+matrix[i][j+1])/5)
for i in mat:
    print(*i)