# External reference: http://cs101.openjudge.cn/practice/30943/statistics/
# Accepted submission: 52727876
# Source: http://cs101.openjudge.cn/practice/solution/52727876/
# License: not declared on the submission page; no license is inferred.

n,m = map(int,input().split())
dis = [[float('inf')]*n for _ in range(n)]
for i in range(n):
    dis[i][i] = 0
for i in range(m):
    u,v,w = map(int,input().split())
    if w == 0:
        dis[u][v] = 1
    else:
        dis[v][u] = 1

for k in range(n):
    for i in range(n):
        for j in range(n):
            if dis[i][k] + dis[k][j] < dis[i][j]:
                dis[i][j] = dis[i][k] + dis[k][j]
ans = 0
for k in range(n):
    can_kown = True
    for i in range(n):
        if dis[i][k] < n+1 or dis[k][i] < n+1:
            continue
        else:
            can_kown = False
            break
    if can_kown:
        ans += 1
print(ans)
