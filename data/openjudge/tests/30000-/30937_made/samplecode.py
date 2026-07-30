# External reference: http://cs101.openjudge.cn/practice/30937/statistics/
# Accepted submission: 52716427
# Source: http://cs101.openjudge.cn/practice/solution/52716427/
# License: not declared on the submission page; no license is inferred.

from collections import deque

n, m = map(int, input().split())
graph = [set() for _ in range(n+1)]
for _ in range(m):
    a, b = map(int, input().split())
    graph[a].add(b)
    graph[b].add(a)

res = set(range(1, n+1))
cnt = 0
while res:
    t = res.pop()
    cnt += 1
    q = deque([t])
    rem = set()
    while q:
        v = q.popleft()
        rem = res-graph[v]
        for u in rem:
            q.append(u)
            res.remove(u)
print(cnt-1)
