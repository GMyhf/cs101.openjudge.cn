# External reference: http://cs101.openjudge.cn/practice/30281/statistics/
# Accepted submission: 51424826
# Source: http://cs101.openjudge.cn/practice/solution/51424826/
# License: not declared on the submission page; no license is inferred.

def min_cost(dx, dy):
    min_delta = min(dx, dy)
    rem_delta = abs(dx-dy)
    cost = min_delta * c
    if dx > dy:
        cost += rem_delta * a
    else:
        cost += rem_delta * b
    return cost
a, b, c = map(float, input().split())
a, b, c = min(a, b+c), min(b, a+c), min(c, a+b)
pos = []
name = []
for _ in range(3):
    s, x, y = input().split()
    pos.append((int(x), int(y)))
    name.append(s)
matrix = [[0]*5 for _ in range(5)]
matrix[0][1] = matrix[1][0] = min_cost(abs(pos[0][0]), abs(pos[0][1]))
matrix[0][2] = matrix[2][0] = min_cost(abs(pos[1][0]), abs(pos[1][1]))
matrix[0][3] = matrix[3][0] = min_cost(abs(pos[2][0]), abs(pos[2][1]))
matrix[1][2] = matrix[2][1] = min_cost(abs(pos[0][0]-pos[1][0]), abs(pos[0][1]-pos[1][1]))
matrix[1][3] = matrix[3][1] = min_cost(abs(pos[0][0]-pos[2][0]), abs(pos[0][1]-pos[2][1]))
matrix[3][2] = matrix[2][3] = min_cost(abs(pos[1][0]-pos[2][0]), abs(pos[1][1]-pos[2][1]))
matrix[4][1] = matrix[1][4] = min_cost(100-pos[0][0], 100-pos[0][1])
matrix[4][2] = matrix[2][4] = min_cost(100-pos[1][0], 100-pos[1][1])
matrix[4][3] = matrix[3][4] = min_cost(100-pos[2][0], 100-pos[2][1])
route = [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
d = {}
for i, j, k in route:
    d[(i, j, k)] = matrix[0][i]+matrix[i][j]+matrix[j][k]+matrix[k][4]
cost = min(d.values())
for key in d:
    if d[key] == cost:
        print(name[key[0]-1], name[key[1]-1], name[key[2]-1])
        break
print(f'{cost:.2f}')
