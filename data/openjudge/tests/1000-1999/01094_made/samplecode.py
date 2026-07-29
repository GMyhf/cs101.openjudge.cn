# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 1094: Sorting It All Out
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01094/
# License: not declared in source collection; no license is inferred.
import sys
#23n2310307206胡景博
from collections import deque
def topo_sort(graph):
    in_degree = {u:0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1
    q = deque([u for u in in_degree if in_degree[u] == 0])
    topo_order = [];flag = True
    while q:
        if len(q) > 1:
            flag = False#topo_sort不唯一确定
        u = q.popleft()
        topo_order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.append(v)
    if len(topo_order) != len(graph): return 0
    return topo_order if flag else None
while True:
    n,m = map(int,input().split())
    if n == 0: break
    graph = {chr(x+65):[] for x in range(n)}
    edges = [tuple(input().split('<')) for _ in range(m)]
    for i in range(m):
        a,b = edges[i]
        graph[a].append(b)
        t = topo_sort(graph)
        if t:
            s = ''.join(t)
            print("Sorted sequence determined after {} relations: {}.".format(i+1,s))
            break
        elif t == 0:
            print("Inconsistency found after {} relations.".format(i+1))
            break
    else:
        print("Sorted sequence cannot be determined.")
