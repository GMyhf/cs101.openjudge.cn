# External reference: statistics page /practice/18252/
# Accepted submission: 41303512
# Source: http://cs101.openjudge.cn/practice/solution/41303512/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/18252 statistics, Accepted solution 41303512.
# Source: http://cs101.openjudge.cn/practice/solution/41303512/
# Statistics: http://cs101.openjudge.cn/practice/18252/statistics/
# License: not declared on submission page; no license inferred
def spfa(s):
    dis = [float('inf') for _ in range(n)]
    dis[s] = 0
    queue = [s]
    cnt = [0] * n
    while queue:
        u = queue.pop(0)
        for v, w in G[u]:
            if dis[v] > dis[u] + w:
                dis[v] = dis[u] + w
                queue.append(v)
                cnt[v] += 1
        if cnt[u] > n:
            return ['Error']
    return dis


for _ in range(int(input())):
    n, m, s = map(int, input().split())
    G = [[] for _ in range(n)]
    for _ in range(m):
        x, y, z = map(int, input().split())
        G[x - 1].append((y - 1, z))
    print(*(i if i != float('inf') else 'null' for i in spfa(s - 1)))
