# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import heapq

def topological_sort(vertices, edges):
    # Initialize in-degree and connection matrix
    in_edges = [0] * (vertices + 1)
    connect = [[0] * (vertices + 1) for _ in range(vertices + 1)]

    # Populate the in-degree and connection matrix
    for u, v in edges:
        in_edges[v] += 1
        connect[u][v] += 1

    # Priority queue for vertices with in-degree of 0
    queue = []
    for i in range(1, vertices + 1):
        if in_edges[i] == 0:
            heapq.heappush(queue, i)

    # List to store the topological order
    order = []

    # Processing vertices
    while queue:
        u = heapq.heappop(queue)
        order.append(u)
        for v in range(1, vertices + 1):
            if connect[u][v] > 0:
                in_edges[v] -= connect[u][v]
                if in_edges[v] == 0:
                    heapq.heappush(queue, v)

    if len(order) == vertices:
        return order
    else:
        return None

# Read input
vertices, num_edges = map(int, input().split())
edges = []
for _ in range(num_edges):
    u, v = map(int, input().split())
    edges.append((u, v))

# Perform topological sort
order = topological_sort(vertices, edges)

# Output result
if order:
    for i, vertex in enumerate(order):
        if i < len(order) - 1:
            print(f"v{vertex}", end=" ")
        else:
            print(f"v{vertex}")
else:
    print("No topological order exists due to a cycle in the graph.")
