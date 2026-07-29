# External reference: http://cs101.openjudge.cn/practice/03259/statistics/
# Accepted submission: 50653360
# Source: http://cs101.openjudge.cn/practice/solution/50653360/
# License: not declared on the submission page; no license is inferred.

n = int(input())
res = []
if n == 4:
    for i in range(1000, 10000):
        s = str(i)
        l, r = s[:2], s[2:]
        if (int(l)+int(r))**2 == i:
            res.append(i)
else:
    for i in range(100000, 1000000):
        s = str(i)
        l, r = s[:3], s[3:]
        if (int(l)+int(r))**2 == i:
            res.append(i)
print(*res)
