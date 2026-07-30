# External reference: http://cs101.openjudge.cn/practice/26976/statistics/
# Accepted submission: 52499256
# Source: http://cs101.openjudge.cn/practice/solution/52499256/
# License: not declared on the submission page; no license is inferred.

import sys
I = iter(sys.stdin.read().split())
n = int(next(I))
nums = [int(next(I)) for _ in range(n)]
up = 1
down = 1
for i in range(1,n):
    if nums[i] < nums[i-1]:
        down = up +1
    elif nums[i] > nums[i-1]:
        up = down +1

print(max(up,down))
