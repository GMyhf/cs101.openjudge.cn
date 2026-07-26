# External reference: cs101.openjudge.cn practice/19974 statistics, Accepted solution 28435155.
# Source: http://cs101.openjudge.cn/practice/solution/28435155/
# Statistics: http://cs101.openjudge.cn/practice/19974/statistics/
# License: not declared on submission page; no license inferred
t = int(input())
lis = []
for T in range(t):
    m,p,q = input().split()
    m = int(m)
    p = int(p)
    q = int(q)
    num = 0
    if m == 0:
        lis.append('0')
    elif m > 0:
        mat = [[0 for _ in range(q+1)]for _ in range(p+1)]
        for j in range(q+1):
            if j < m:
                mat[0][j] = 1
        for i in range(p+1):
            mat[i][0] = 1
        for j in range(1,q+1):
            for i in range(1,p+1):
                if j >= i+m:
                    mat[i][j] = 0
                else:
                    mat[i][j] = mat[i-1][j] + mat[i][j-1]
        lis.append(str(mat[p][q]))
    elif m < 0:
        m = -m
        mat = [[0 for _ in range(q+1)]for _ in range(p+1)]
        for i in range(p+1):
            if i < m:
                mat[i][0] = 1
        for j in range(q+1):
            mat[0][j] = 1
        for j in range(1,q+1):
            for i in range(1,p+1):
                if j <= i-m:
                    mat[i][j] = 0
                else:
                    mat[i][j] = mat[i-1][j] + mat[i][j-1]
        lis.append(str(mat[p][q]))
for _ in lis:
    print(_)
