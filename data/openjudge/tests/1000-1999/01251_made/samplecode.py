# External reference: http://cs101.openjudge.cn/practice/01251/statistics/
# Accepted submission: 51699516
# Source: http://cs101.openjudge.cn/practice/solution/51699516/
# License: not declared on the submission page; no license is inferred.

while True:
    n = int(input())
    if n == 0:
        break
    INF = float('inf')
    matrix = [[INF]*n for _ in range(n)]
    for _ in range(n-1):
        inp = input().split()
        village = inp[0]
        v1 = ord(village)-ord('A')
        num = int(inp[1])
        for i in range(1, num+1):
            neighbor, cost = inp[2*i], int(inp[2*i+1])
            v2 = ord(neighbor)-ord('A')
            matrix[v1][v2] = cost
            matrix[v2][v1] = cost
    total_cost = 0
    visited = [False]*n
    min_edge = [INF]*n
    min_edge[0] = 0
    for _ in range(n):
        u = -1
        for v in range(n):
            if not visited[v] and (u == -1 or min_edge[v] < min_edge[u]):
                u = v
        visited[u] = True
        total_cost += min_edge[u]
        for v in range(n):
            if matrix[u][v] < INF and not visited[v]:
                if matrix[u][v] < min_edge[v]:
                    min_edge[v] = matrix[u][v]
    print(total_cost)
