# External reference: cs101.openjudge.cn practice/20135 statistics, Accepted solution 52789538.
# Source: http://cs101.openjudge.cn/practice/solution/52789538/
# Statistics: http://cs101.openjudge.cn/practice/20135/statistics/
# License: not declared on submission page; no license inferred
move = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

m, n = map(int, input().split())
s = [input() for i in range(m)]
name = input()

def find(x, y, d, i):
    if i == len(name):
        print(x + 1, y + 1)
        print(move[d][0], move[d][1])
        return True
    return name[i] == s[x + i*move[d][0]][y + i*move[d][1]] and find(x, y, d, i + 1)


for x in range(m):
    for y in range(n):
        if s[x][y] == name[0]:
            for d in range(8):
                if 0 <= x + move[d][0]*(len(name) - 1) < m and 0 <= y + move[d][1]*(len(name) - 1) < n:
                    if find(x, y, d, 0):
                        exit()
