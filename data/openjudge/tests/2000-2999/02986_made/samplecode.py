# External reference: http://cs101.openjudge.cn/practice/02986/statistics/
# Accepted submission: 51426424
# Source: http://cs101.openjudge.cn/practice/solution/51426424/
# License: not declared on the submission page; no license is inferred.

import sys
for l in sys.stdin.read().splitlines():
    n, k=map(int,l.split())
    a = k.bit_length()
    for i in range(1, a + 1):
        if n // 2 ** i - (n - k) // 2 ** i:
            print(0)
            break
    else:
        print(1)
