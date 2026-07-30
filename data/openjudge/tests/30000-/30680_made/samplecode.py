# External reference: http://cs101.openjudge.cn/practice/30680/statistics/
# Accepted submission: 52783959
# Source: http://cs101.openjudge.cn/practice/solution/52783959/
# License: not declared on the submission page; no license is inferred.

from collections import defaultdict

n = int(input())

children = defaultdict(list)
indegree = defaultdict(int)

nodes = set()

for _ in range(n):
    arr = list(map(int, input().split()))

    u = arr[0]
    nodes.add(u)

    for v in arr[1:]:
        children[u].append(v)
        indegree[v] += 1
        nodes.add(v)

# 找根节点
roots = []

for x in nodes:
    if indegree[x] == 0:
        roots.append(x)

roots.sort()

ans = []

def dfs(u):

    cur = [(u, 0)]

    for v in children[u]:
        cur.append((v, 1))

    cur.sort(key=lambda x: x[0])

    for x, typ in cur:

        if typ == 0:
            ans.append(x)

        else:
            dfs(x)

for r in roots:
    dfs(r)

print(*ans, sep="\n")
