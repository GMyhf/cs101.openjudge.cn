# External reference: http://cs101.openjudge.cn/practice/18164/statistics/
# Accepted submission: 52625278
# Source: http://cs101.openjudge.cn/practice/solution/52625278/
# License: not declared on the submission page; no license is inferred.

import heapq
num = int(input())
heap = [int(x) for x in input().split()]
ans = 0
heapq.heapify(heap)
while len(heap) > 1:
    a = heapq.heappop(heap)
    b = heapq.heappop(heap)
    ans += a + b
    heapq.heappush(heap, a + b)
print(ans)
