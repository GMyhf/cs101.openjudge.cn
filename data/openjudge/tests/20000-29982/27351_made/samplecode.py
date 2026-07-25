# Source: /home/ubuntu/hongfei/2024spring-cs201/2024spring_dsa_problems.md
from collections import deque

n, m = map(int, input().split())
graph1 = [set() for _ in range(n+1)]
for _ in range(m):
    a, b = map(int, input().split())
    graph1[a].add(b)
    graph1[b].add(a)

unvisited = set(range(1, n+1))
components = 0

while unvisited:
    start = unvisited.pop()
    components += 1
    queue = deque([start])
    while queue:
        u = queue.popleft()
        good = unvisited - graph1[u]  # 所有未访问且与 u 有 0-边的点
        for v in good:
            queue.append(v)
        unvisited -= good

print(components - 1)
