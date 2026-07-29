# External reference: http://cs101.openjudge.cn/practice/01702/statistics/
# Accepted submission: 51708993
# Source: http://cs101.openjudge.cn/practice/solution/51708993/
# License: not declared on the submission page; no license is inferred.

def trans(x):
    res = []
    while x >= 3:
        res.append(x%3)
        x //= 3
    res.append(x)
    return res
T = int(input())
for _ in range(T):
    x = int(input())
    expr = trans(x)+[0]
    left, right = [], []
    for i in range(len(expr)):
        if expr[i] == 0:
            continue
        if expr[i] == 1:
            right.append(3**i)
        elif expr[i] == 2:
            left.append(3**i)
            expr[i+1] += 1
        else:
            expr[i+1] += 1
    if not left:
        print('empty', end = ' ')
    else:
        print(','.join(map(str, left)), end = ' ')
    print(','.join(map(str, right)))
