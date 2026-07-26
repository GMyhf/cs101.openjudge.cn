# External reference: statistics page /practice/18071/
# Accepted submission: 52688789
# Source: http://cs101.openjudge.cn/practice/solution/52688789/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/18071 statistics, Accepted solution 52688789.
# Source: http://cs101.openjudge.cn/practice/solution/52688789/
# Statistics: http://cs101.openjudge.cn/practice/18071/statistics/
# License: not declared on submission page; no license inferred
import sys

data = sys.stdin.read().strip().splitlines()
M, N = map(int, data[0].strip().split())
matrix = []
for i in range(1, M + 1):
    line = list(map(int, data[i].split()))
    matrix.append(line)
graph = {(i, j): [] for i in range(M) for j in range(N)}

dire = [(0, 1), (0, -1), (1, 0), (-1, 0)]
for i in range(M):
    for j in range(N):
        if matrix[i][j] == 1:
            for dx, dy in dire:
                if 0 <= i + dx <= M - 1 and 0 <= j + dy <= N - 1:

                    if matrix[i + dx][j + dy] == 1:
                        graph[(i, j)].append((i + dx, j + dy))


def topological_sort_dfs(M, N, graph):
    visited = [[0] * N for _ in range(M)]

    def dfs(i, j, fi, fj):
        visited[i][j] = 1
        for v in graph[(i, j)]:
            if v[0] == fi and v[1] == fj:
                continue
            if visited[v[0]][v[1]] == 1:
                return False
            if visited[v[0]][v[1]] == 0:
                if not dfs(v[0], v[1], i, j):
                    return False
        visited[i][j] = 2
        return True

    for i in range(M):
        for j in range(N):
            if visited[i][j] == 0:
                if not dfs(i, j, -1, -1):
                    return None
    return 1


t = topological_sort_dfs(M, N, graph)
if not t:
    print("YES")
else:
    print("NO")
