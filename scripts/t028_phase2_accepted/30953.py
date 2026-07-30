# External reference: http://cs101.openjudge.cn/practice/30953/statistics/
# Accepted submission: 52727269
# Source: http://cs101.openjudge.cn/practice/solution/52727269/
# License: not declared on the submission page; no license is inferred.

import sys

sys.setrecursionlimit(10**6)
def tarjan(graph):
    n = len(graph)
    dfn = [-1] * n
    low = [-1] * n
    mn_visit = list(range(n))
    on_stack = [False] * n
    stack = []
    timer = 0
    def dfs(u):
        nonlocal timer
        dfn[u] = low[u] = timer
        timer += 1
        on_stack[u] = True
        stack.append(u)
        for v in graph[u]:
            if dfn[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif on_stack[v]:
                low[u] = min(low[u], dfn[v])
            mn_visit[u] = min(mn_visit[u], mn_visit[v])
        if low[u] == dfn[u]:
            comp = []
            mn = mn_visit[u]
            while True:
                node = stack.pop()
                on_stack[node] = False
                comp.append(node)
                if mn > mn_visit[node]:
                    mn = mn_visit[node]
                if node == u:
                    break
            for node in comp:
                mn_visit[node] = mn

    for i in range(1, n):
        if dfn[i] == -1:
            dfs(i)

    return mn_visit

def main():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
    ans = tarjan(adj)
    print(*ans[1:])

if __name__ == '__main__':
    main()
