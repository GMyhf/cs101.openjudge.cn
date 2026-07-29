# External reference: http://cs101.openjudge.cn/practice/01248/statistics/
# Accepted submission: 52718716
# Source: http://cs101.openjudge.cn/practice/solution/52718716/
# License: not declared on the submission page; no license is inferred.

lt = {}
for i in range(1, 27):
    lt[i] = chr(64 + i)

ch = []
a = 0

def find(visited, f):
    if len(visited) == 5:
        if a == f[0] - f[1]**2 + f[2]**3 - f[3]**4 + f[4]**5:
            print(''.join(map(lambda x: lt[x], f)))
            return True
        else:
            return False
    for i in ch:
        if i not in visited and find(visited | {i}, f + [i]):
            return True
    return False

while True:
    sa, l = input().split()
    a = int(sa)
    if a == 0:
        break
    ch = sorted(map(lambda x: ord(x) - 64, l), reverse = True)
    if not find(set(), []):
        print("no solution")
