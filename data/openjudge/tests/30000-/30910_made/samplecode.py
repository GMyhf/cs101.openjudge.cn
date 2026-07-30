# External reference: http://cs101.openjudge.cn/practice/30910/statistics/
# Accepted submission: 52724251
# Source: http://cs101.openjudge.cn/practice/solution/52724251/
# License: not declared on the submission page; no license is inferred.

import heapq
from collections import defaultdict

def dijkstra(n, adj, start):
    dist = [10 ** 9] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist

n, m = map(int, input().split())
adj1 = defaultdict(list)
adj2 = defaultdict(list)

for _ in range(m):
    st, ed, w1 = map(int, input().split())
    adj1[st].append((ed, w1))
    adj2[ed].append((st, w1))

dist1 = dijkstra(n, adj1, 1)
dist2 = dijkstra(n, adj2, 1)
print(sum(dist1[1:] + dist2[1:]))
