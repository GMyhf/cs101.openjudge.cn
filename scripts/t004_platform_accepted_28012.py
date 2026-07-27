# External reference: statistics page /practice/28012/
# Accepted submission: 52741406
# Source: http://cs101.openjudge.cn/practice/solution/52741406/
# License: not declared on the submission page; no license is inferred.

from collections import defaultdict, deque

def reachableNodes(n, edges, restricted):
    # 建图
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    restricted_set = set(restricted)

    # BFS 从节点 0 开始
    visited = set()
    queue = deque([0])
    visited.add(0)

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in visited and v not in restricted_set:
                visited.add(v)
                queue.append(v)

    return len(visited)


if __name__ == "__main__":
    # 读取输入
    n = int(input().strip())
    edges = []
    for _ in range(n - 1):
        a, b = map(int, input().split())
        edges.append([a, b])
    restricted = list(map(int, input().split()))

    # 计算结果并输出
    result = reachableNodes(n, edges, restricted)
    print(result)