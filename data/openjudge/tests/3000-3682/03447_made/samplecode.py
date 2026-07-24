# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# 肖添天
from collections import defaultdict, deque

n = int(input())
graph = defaultdict(set)
to_earth = set()
price = {}
for i in range(n):
    a, b, c = input().split()
    b = float(b)
    price[a] = b if a not in price else max(price[a], b)
    for x in c:
        if x == "*":
            to_earth.add(a)
        else:
            graph[a].add(x)
            graph[x].add(a)

def bfs(start):
    Q = deque([start])
    visited = set()
    visited.add(start)
    cnt = 0
    while Q:
        l = len(Q)
        for _ in range(l):
            f = Q.popleft()
            if f in to_earth:
                return price[start] * (0.95 ** cnt)
            for x in graph[f]:
                if x not in visited:
                    Q.append(x)
                    visited.add(x)
        cnt += 1
    return 0


ans = []
for planet in price.keys():
    ans.append((bfs(planet), planet))

ans.sort(key=lambda x: [-x[0], x[1]])
print(ans[0][1])
