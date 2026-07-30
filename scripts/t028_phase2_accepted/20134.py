# External reference: http://cs101.openjudge.cn/practice/20134/statistics/
# Accepted submission: 52789455
# Source: http://cs101.openjudge.cn/practice/solution/52789455/
# License: not declared on the submission page; no license is inferred.

import heapq

d1, c, d2, m, n = map(float, input().split())
n = int(n)
heap = [(m, 0)]
d0 = 0
tot = 0
sta = sorted(map(lambda x: tuple(map(float, x.split())), [input() for i in range(n)])) + [(d1, float("inf"))]
for d, p in sta:
    while heap and heap[0][1] + c*d2 < d:
        if heap[0][1] + c*d2 > d0:
            tot += (heap[0][1] + c*d2 - d0)/d2*heap[0][0]
            d0 = heap[0][1] + c*d2
        heapq.heappop(heap)
    if not heap:
        print("No Solution")
        exit()
    tot += (d - d0)/d2*heap[0][0]
    heapq.heappush(heap, (p, d))
    d0 = d
print(f"{tot:.2f}")
