# External reference: http://cs101.openjudge.cn/practice/30669/statistics/
# Accepted submission: 52735186
# Source: http://cs101.openjudge.cn/practice/solution/52735186/
# License: not declared on the submission page; no license is inferred.

from collections import deque
import math
n, t = [*map(int, input().split())]
nbr = [[] for _ in range(n+1)]
for _ in range(n-1):
    x1, x2 = [*map(int, input().split())]
    nbr[x1].append(x2)
    nbr[x2].append(x1)
flag = [0] * (n + 1)
deep = [0] * (n + 1)
q = deque()
q.append((t, 0))
flag[t] = 1
parent = [0 for _ in range(n+1)]
while q:
    now, cur_deep = q.popleft()
    deep[now] = cur_deep
    for i in nbr[now]:
        if flag[i] == 0:
            flag[i] = 1
            q.append((i, cur_deep+1))
            parent[i] = now
p, q, v1, v2 = [*map(int, input().split())]
now, ekis = p, [p]
while now != t:
    now = parent[now]
    ekis.append(now)
now = q
while now not in ekis:
    now = parent[now]
d1, d2 = deep[p] - deep[now], deep[q] - deep[now]
time = (d1 + d2) // (v1 + v2)
x1, x2 = time * v1, time * v2
ans = 0
if x1 < d1:
    ans = deep[p] - x1
else:
    ans = deep[q] - x2
print(time, ans)
