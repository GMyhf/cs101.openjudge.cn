# External reference: http://cs101.openjudge.cn/practice/02002/statistics/
# Accepted submission: 52726153
# Source: http://cs101.openjudge.cn/practice/solution/52726153/
# License: not declared on the submission page; no license is inferred.

while 1:
    n = int(input())
    if n == 0:
        break
    a = [tuple(map(int, input().split())) for _ in range(n)]
    pa = set(a)
    ans = 0
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = a[i]
            x2, y2 = a[j]
            x3, y3, x4, y4 = x1 - (y2 - y1), y1 + (x2 - x1), x2 - (y2 - y1), y2 + (x2 - x1)
            if (x3, y3) in pa and (x4, y4) in pa:
                ans += 1
            x3, y3, x4, y4 = x1 + (y2 - y1), y1 - (x2 - x1), x2 + (y2 - y1), y2 - (x2 - x1)
            if (x3, y3) in pa and (x4, y4) in pa:
                ans += 1
    print(ans // 4)
