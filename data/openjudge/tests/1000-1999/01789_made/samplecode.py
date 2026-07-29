# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 1789: Truck History
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01789/
# License: not declared; no license is inferred.
import sys
import heapq

def truck_history():
    while True:
        n = int(input())
        if n == 0:
            break

        trucks = [input() for _ in range(n)]
        trucks.sort()

        graph = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                graph[i][j] = graph[j][i] = sum(a!=b for a, b in zip(trucks[i], trucks[j]))

        visited = [False]*n
        min_edge = [float('inf')]*n
        min_edge[0] = 0
        total_distance = 0

        min_heap = [(0, 0)]
        while min_heap:
            d, v = heapq.heappop(min_heap)
            if visited[v]:
                continue
            visited[v] = True
            total_distance += d
            for u in range(n):
                if not visited[u] and graph[v][u] < min_edge[u]:
                    min_edge[u] = graph[v][u]
                    heapq.heappush(min_heap, (graph[v][u], u))

        print(f"The highest possible quality is 1/{total_distance}.")

truck_history()
