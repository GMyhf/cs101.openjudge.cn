# External reference: http://cs101.openjudge.cn/practice/02994/statistics/
# Accepted submission: 50623996
# Source: http://cs101.openjudge.cn/practice/solution/50623996/
# License: not declared on the submission page; no license is inferred.

import heapq
N = int(input())
l = [int(x) for x in input().split()]
heapq.heapify(l)
if N == 1:
    print(heapq.heappop(l))
else:
    res = 0
    while True:
        a = heapq.heappop(l)
        b = heapq.heappop(l)
        c = a+b
        res += c
        if l:
            heapq.heappush(l, c)
        else:
            break
    print(res)
