# External reference: http://cs101.openjudge.cn/practice/30179/statistics/
# Accepted submission: 52006448
# Source: http://cs101.openjudge.cn/practice/solution/52006448/
# License: not declared on the submission page; no license is inferred.

t = int(input())
for _ in range(t):
    n = int(input())
    r = 0
    idx = -1
    matrix = []
    for i in range(n):
        row = list(map(int, input().split()))
        for j in range(n):
            if row[j] == 0:
                if not n%2:
                    r = i+1
                del row[j]
                break
        matrix.extend(row)
    cnt = n-1+r

    for k in range(n**2-1):
        if matrix[k] != 0:
            cnt += 1
            j = k
            while matrix[j] != 0:
                nxt = matrix[j]-1
                matrix[j] = 0
                j = nxt

    if cnt % 2:
        print('no')
    else:
        print('yes')
