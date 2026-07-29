# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 1178: Camelot
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01178/
# License: not declared; no license is inferred.
import sys
import sys

inf = float('infinity')
kmove = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
knmove = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
kmap = [[inf]*64 for _ in range(64)]
knmap = [[inf]*64 for _ in range(64)]

def ok(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def getxy(p):
    return p % 8, p // 8

def getPosition(x, y):
    return x + y * 8

def init():
    for i in range(64):
        kmap[i][i] = 0
        knmap[i][i] = 0
        x, y = getxy(i)
        for j in range(8):
            tx, ty = kmove[j][0] + x, kmove[j][1] + y
            if ok(tx, ty):
                next = getPosition(tx, ty)
                kmap[i][next] = 1
            tx, ty = knmove[j][0] + x, knmove[j][1] + y
            if ok(tx, ty):
                next = getPosition(tx, ty)
                knmap[i][next] = 1

def floyd():
    for k in range(64):
        for i in range(64):
            for j in range(64):
                kmap[i][j] = min(kmap[i][j], kmap[i][k] + kmap[k][j])
                knmap[i][j] = min(knmap[i][j], knmap[i][k] + knmap[k][j])

init()
floyd()

s = input().strip()
size = len(s)
num = 0
position = [0]*64

for i in range(0, size, 2):
    position[num] = ord(s[i]) - ord('A') + (ord(s[i+1]) - ord('1')) * 8
    num += 1

minmove = inf
total = 0  # Renamed 'sum' to 'total'
for ds in range(64):
    for m in range(64):
        for k in range(1, num):
            total = sum(knmap[position[i]][ds] for i in range(1, num))
            total += kmap[position[0]][m]
            total += knmap[position[k]][m] + knmap[m][ds]
            total -= knmap[position[k]][ds]
            minmove = min(minmove, total)

print(minmove)
