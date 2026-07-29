# External reference: http://cs101.openjudge.cn/practice/01269/statistics/
# Accepted submission: 51703457
# Source: http://cs101.openjudge.cn/practice/solution/51703457/
# License: not declared on the submission page; no license is inferred.

N = int(input())
print('INTERSECTING LINES OUTPUT')
for _ in range(N):
    x1, y1, x2, y2, x3, y3, x4, y4 = map(int, input().split())
    INF = float('inf')
    k1, k2 = INF, INF
    if x1 != x2:
        k1 = (y1-y2)/(x1-x2)
    if x3 != x4:
        k2 = (y3-y4)/(x3-x4)
    if k1 == k2:
        if k1 == INF:
            if x1 == x3:
                print('LINE')
            else:
                print('NONE')
        else:
            b1 = (x2*y1-x1*y2)/(x2-x1)
            b2 = (x4*y3-x3*y4)/(x4-x3)
            if b1 == b2:
                print('LINE')
            else:
                print('NONE')
    else:
        if k1 == INF:
            b2 = (x4*y3-x3*y4)/(x4-x3)
            y = k2*x1+b2
            print(f'POINT {x1:.2f} {y:.2f}')
        elif k2 == INF:
            b1 = (x2*y1-x1*y2)/(x2-x1)
            y = k1*x3+b1
            print(f'POINT {x3:.2f} {y:.2f}')
        else:
            b1 = (x2*y1-x1*y2)/(x2-x1)
            b2 = (x4*y3-x3*y4)/(x4-x3)
            x = (b2-b1)/(k1-k2)
            y = k1*x+b1
            print(f'POINT {x:.2f} {y:.2f}')
print('END OF OUTPUT')
