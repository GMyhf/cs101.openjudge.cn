# External reference: cs101.openjudge.cn practice/07735 statistics, Accepted solution 52721315.
# Source: http://cs101.openjudge.cn/practice/solution/52721315/
# Statistics: http://cs101.openjudge.cn/practice/07735/statistics/
# License: not declared on submission page; no license inferred
import heapq

k = int(input())
n = int(input())
road = [set() for i in range(n + 1)]
for i in range(int(input())):
    s, d, l, t = map(int, input().split())
    road[s].add((d, l, t))

dis = [{} for i in range(n + 1)]
dis[1][0] = 0
h = [(0, 1, 0)]

while h:
    d, u, c = heapq.heappop(h)
    if u == n:
        print(d)
        break
    for v, l, t in road[u]:
        if c + t > k:
            continue
        if c + t not in dis[v] or d + l < dis[v][c + t]:
            dis[v][c + t] = d + l
            heapq.heappush(h, (d + l, v, c + t))
else:
    print(-1)