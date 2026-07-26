# External reference: statistics page /practice/07832/
# Accepted submission: 51153551
# Source: http://cs101.openjudge.cn/practice/solution/51153551/
# License: not declared on the submission page; no license is inferred.

import math
N, A, B = map(int, input().split())
res = 0
ans = (0, 0)
for i in range(1, N+1):
    j = math.ceil(i*A/B-1)
    if j/i > res:
        res = j/i
        ans = (j, i)
print(*ans)