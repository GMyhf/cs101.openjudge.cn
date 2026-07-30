# External reference: http://cs101.openjudge.cn/practice/27122/statistics/
# Accepted submission: 52535954
# Source: http://cs101.openjudge.cn/practice/solution/52535954/
# License: not declared on the submission page; no license is inferred.

import sys
I = iter(sys.stdin.read().split())
n = int(next(I))
m = int(next(I))
position = [int(next(I)) for _ in range(n)]
position.sort()
right = position[-1]-position[0] + 1
left = 0
def check(d):
    ans = 1
    i = 0
    j = 1
    while j < n:
        if position[j] - position[i] < d:
            j += 1
        else:
            i = j
            j += 1
            ans += 1
    return ans >= m
while left + 1<right:
    mid = (left+right)//2
    if check(mid):
        left = mid
    else:
        right = mid

print(left)
