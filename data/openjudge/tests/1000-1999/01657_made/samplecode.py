# External reference: http://cs101.openjudge.cn/practice/01657/statistics/
# Accepted submission: 52486260
# Source: http://cs101.openjudge.cn/practice/solution/52486260/
# License: not declared on the submission page; no license is inferred.

def King(x, y):
    steps = max(x, y)
    return steps

def Queen(x, y):
    if x == y or x == 0 or y == 0:
        steps = 1
    else:
        steps = 2
    return steps

def Rook(x, y):
    if x == 0 or y == 0:
        return 1
    else:
        return 2

def Bishop(x, y):
    if (x + y) % 2 != 0:
        return "Inf"
    elif x == y:
        return 1
    else:
        return 2


t = int(input())

for _ in range(t):
    start, end = input().split()
    x_1 = start[0]
    y_1 = int(start[1])
    x_2 = end[0]
    y_2 = int(end[1])
    dx = abs(ord(x_2) - ord(x_1))
    dy = abs(y_2 - y_1)
    if dx == 0 and dy == 0:
        print('0 0 0 0')
    else:
        print(King(dx, dy), Queen(dx, dy), Rook(dx, dy), Bishop(dx, dy))
