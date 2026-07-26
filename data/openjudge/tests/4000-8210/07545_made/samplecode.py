# External reference: statistics page /practice/07545/
# Accepted submission: 51084173
# Source: http://cs101.openjudge.cn/practice/solution/51084173/
# License: not declared on the submission page; no license is inferred.

row, col = map(int, input().split())
matrix = [['#']*(col+2)] + [['#']+[int(x) for x in input().split()]+['#'] for _ in range(row)] + [['#']*(col+2)]
res = []
dire = [[0, 1], [1, 0], [0, -1], [-1, 0]]
idx = 0
num = 1
x, y = 1, 1
while num <= row*col:
    res.append(matrix[x][y])
    matrix[x][y] = '#'
    dx, dy = dire[idx][0], dire[idx][1]
    if matrix[x+dx][y+dy] == '#':
        idx = (idx+1)%4
        dx, dy = dire[idx][0], dire[idx][1]
    x += dx
    y += dy
    num += 1
print(*res, sep='\n')