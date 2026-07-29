# External reference: http://cs101.openjudge.cn/practice/01068/statistics/
# Accepted submission: 51690523
# Source: http://cs101.openjudge.cn/practice/solution/51690523/
# License: not declared on the submission page; no license is inferred.

t = int(input())
for _ in range(t):
    n = int(input())
    P = [0]+[int(x) for x in input().split()]
    sequence = []
    for i in range(1, n+1):
        for _ in range(P[i]-P[i-1]):
            sequence.append('(')
        sequence.append(')')
    W = []
    for i in range(2*n):
        if sequence[i] == '(':
            continue
        num_r, num_l = 0, 0
        for j in range(i, -1, -1):
            if sequence[j] == '(':
                num_l += 1
                if num_l == num_r:
                    break
                continue
            num_r += 1
        W.append(num_r)
    print(*W)
