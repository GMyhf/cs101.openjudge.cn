# External reference: http://cs101.openjudge.cn/practice/04019/statistics/
# Accepted submission: 51369926
# Source: http://cs101.openjudge.cn/practice/solution/51369926/
# License: not declared on the submission page; no license is inferred.

import sys

d = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30]

for l in sys.stdin.read().splitlines():
    m = []
    n = int(l) + 12
    for i in range(12):
        n += d[i]
        if n % 7 == 5:
            m += [i + 1]
    print(' '.join(map(str, m)))
