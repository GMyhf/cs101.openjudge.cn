# External reference: http://cs101.openjudge.cn/practice/28912/statistics/
# Accepted submission: 52512477
# Source: http://cs101.openjudge.cn/practice/solution/52512477/
# License: not declared on the submission page; no license is inferred.

import math

n, M = map(int, input().split())
params = [list(map(int, input().split())) for _ in range(n)]

points = {0, M}
for a, b, c in params:
    if a != 0:
        x_f = -b / a
        for dx in [math.floor(x_f), math.ceil(x_f)]:
            if 0 <= dx <= M:
                points.add(dx)

results = []
for x in points:
    val = sum(c * abs(a * x + b) for a, b, c in params)
    results.append(val)

print(f"{max(results)} {min(results)}")
