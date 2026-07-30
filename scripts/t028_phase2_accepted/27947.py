# External reference: http://cs101.openjudge.cn/practice/27947/statistics/
# Accepted submission: 52662764
# Source: http://cs101.openjudge.cn/practice/solution/52662764/
# License: not declared on the submission page; no license is inferred.

import heapq

for _ in range(int(input())):
    l, r = [], []
    a = []
    for n in map(int, input().split()):
        if len(l) > len(r):
            if n < -l[0]:
                heapq.heappush(r, -heapq.heappop(l))
                heapq.heappush(l, -n)
            else:
                heapq.heappush(r, n)
        else:
            if r and n > r[0]:
                heapq.heappush(l, -heapq.heappop(r))
                heapq.heappush(r, n)
            else:
                heapq.heappush(l, -n)
            a.append(-l[0])
    print(len(a))
    print(' '.join(map(str, a)))
