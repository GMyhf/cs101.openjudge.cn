import copy
n, m = map(int, input().split())
matrix = [[int(x) for x in input().split()] for _ in range(n)]
mat = copy.deepcopy(matrix)
for i in range(1, n-1):
    for j in range(1, m-1):
        mat[i][j] = round((matrix[i][j]+matrix[i][j-1]+matrix[i-1][j]+matrix[i+1][j]+matrix[i][j+1])/5)
for i in mat:
    print(*i)