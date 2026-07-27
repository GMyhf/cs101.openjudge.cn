# External reference: /practice/30022/statistics/
# Accepted submission: 52733303
# Source: http://cs101.openjudge.cn/practice/solution/52733303/
# License: not declared on the submission page; no license is inferred.

from collections import deque
import sys

def bfs(start, n, adj):
    dist = [-1] * n
    q = deque()
    q.append(start)
    dist[start] = 0
    while q:
        u = q.popleft()
        for v in range(n):
            if adj[u][v] == 1 and dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def main():
    n, k, s = map(int, sys.stdin.readline().split())
    adj = []
    for _ in range(n):
        row = list(map(int, sys.stdin.readline().split()))
        adj.append(row)
    
    d1 = bfs(k, n, adj)
    d2 = bfs(s, n, adj)
    
    min_len = float('inf')
    for u in range(n):
        if d1[u] == -1 or d2[u] == -1:
            continue
        if d1[u] == d2[u]:
            if d1[u] < min_len:
                min_len = d1[u]
    
    print(min_len if min_len != float('inf') else -1)

if __name__ == "__main__":
    main()