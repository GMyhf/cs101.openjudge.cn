# External reference: http://cs101.openjudge.cn/practice/02790/statistics/
# Accepted submission: 51486638
# Source: http://cs101.openjudge.cn/practice/solution/51486638/
# License: not declared on the submission page; no license is inferred.

import sys

sys.setrecursionlimit(1 << 30)

k = int(input())
for _ in range(k):
    n = int(input())
    a = []
    for i in range(n):
        a.append(input())
    ha, la, hb, lb = map(int, input().split())
    if a[ha][la] == "#" or a[hb][lb] == "#":
        print("NO")
        continue

    vis = [[False] * n for __ in range(n)]

    def dfs(x, y):
        vis[x][y] = True
        if x == hb and y == lb:
            return True
        d = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dx, dy in d:
            if 0 <= x + dx < n and 0 <= y + dy < n:
                if a[x + dx][y + dy] == "." and not vis[x + dx][y + dy]:
                    if dfs(x + dx, y + dy):
                        return True

    print("YES" if dfs(ha, la) else "NO")
