# External reference: http://cs101.openjudge.cn/practice/01129/statistics/
# Accepted submission: 52288382
# Source: http://cs101.openjudge.cn/practice/solution/52288382/
# License: not declared on the submission page; no license is inferred.

def is_possible(g, n, colors):
    for u in range(n):
        for v in g[u]:
            if colors[u] == colors[v]:
                return False
    return True
def backtrack(g, u, n, max_color, colors):
    if u == n:
        return is_possible(g, n, colors)
    for c in range(max_color):
        colors[u] = c
        if backtrack(g, u + 1, n, max_color, colors):
            return True
        colors[u] = -1
    return False
def min_color(g, n):
    if n == 0:
        return 0
    for k in range(1, 5):
        colors = [-1] * n
        if backtrack(g, 0, n, k, colors):
            return k
    return 4
while True:
    n = int(input())
    if n == 0:
        break
    g = [[] for _ in range(n)]
    for i in range(n):
        s = input().strip()
        adj = s.split(':')[1]
        for ch in adj:
            j = ord(ch) - ord('A')
            g[i].append(j)
    res = min_color(g, n)
    if res == 1:
        print(f"{res} channel needed.")
    else:
        print(f"{res} channels needed.")
