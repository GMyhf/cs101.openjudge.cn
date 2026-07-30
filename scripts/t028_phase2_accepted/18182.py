# External reference: http://cs101.openjudge.cn/practice/18182/statistics/
# Accepted submission: 52705451
# Source: http://cs101.openjudge.cn/practice/solution/52705451/
# License: not declared on the submission page; no license is inferred.

nCases = int(input())
for _ in range(nCases):
    n, m, b = map(int, input().split())
    ways = {}
    times = []
    for i in range(n):
        ti, xi = map(int, input().split())
        if ti not in ways:
            times.append(ti)
            ways[ti] = [xi]
        else:
            a = ways[ti]
            ways[ti] = a + [xi]
    times.sort()
    tot = 0
    jud = True
    for t in times:
        a1 = ways[t]
        a1.sort()
        tot += sum(a1[-m:])
        if tot >= b:
            print(t)
            jud = False
            break
    if jud == True:
        print('alive')
