# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import heapq

def dijkstra(n, graph, allowed_edges):
    dist = [float('inf')] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]
    while pq:
        time, u = heapq.heappop(pq)
        if time > dist[u]:
            continue
        for v, t in allowed_edges[u]:
            if dist[v] > time + t:
                dist[v] = time + t
                heapq.heappush(pq, (dist[v], v))
    return dist[n]

def check(x, n, T, edges):
    graph = [[] for _ in range(n + 1)]
    special_edges = []

    for u, v, t, a in edges:
        if a <= x:
            graph[u].append((v, t))
            graph[v].append((u, t))
        else:
            special_edges.append((u, v, t))

    # 尝试不使用光学迷彩
    if dijkstra(n, edges, graph) <= T:
        return True

    # 尝试每一条特权边作为迷彩边
    for u, v, t in special_edges:
        # 暂时加上这条边
        graph[u].append((v, t))
        graph[v].append((u, t))
        if dijkstra(n, edges, graph) <= T:
            return True
        # 撤销
        graph[u].pop()
        graph[v].pop()

    return False

def min_armor(n, m, T, edge_list):
    left, right = 0, 100
    answer = 100
    while left <= right:
        mid = (left + right) // 2
        if check(mid, n, T, edge_list):
            answer = mid
            right = mid - 1
        else:
            left = mid + 1
    return answer

# 读入样例输入
n, m, T = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]

print(min_armor(n, m, T, edges))
