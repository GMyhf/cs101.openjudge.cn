# External reference: statistics page /practice/23744/
# Accepted submission: 52178544
# Source: http://cs101.openjudge.cn/practice/solution/52178544/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 参考解（审计时重写）：原 AC 提交 52178544 只用 min(a,b+c)/min(b,a+c)/min(c,a+b) 的闭式，
# 漏掉了「两步对角线 (1,1)+(1,-1) 合成一步 x」等组合，c 小于 a 或 b 时会偏大。
# 这里在位移网格上跑 Dijkstra 求任意两点间最小成本（成本只与位移有关），再枚举 6 种拾取顺序。
import heapq
from itertools import permutations
a, b, c = map(float, input().split())
parts = []
for _ in range(3):
    s, x, y = input().split()
    parts.append((s, int(x), int(y)))
R = 205  # 任意两点位移的分量绝对值不超过 199，最优路径可重排到不越出位移框外一格
W = 2 * R + 1
INF = float("inf")
dist = [INF] * (W * W)
start = R * W + R
dist[start] = 0.0
heap = [(0.0, start)]
moves = [(1, 0, a), (-1, 0, a), (0, 1, b), (0, -1, b), (1, 1, c), (1, -1, c), (-1, 1, c), (-1, -1, c)]
while heap:
    d, u = heapq.heappop(heap)
    if d > dist[u]:
        continue
    x, y = divmod(u, W)
    for dx, dy, w in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < W and 0 <= ny < W:
            v = nx * W + ny
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
def cost(p, q):
    return dist[(q[0] - p[0] + R) * W + (q[1] - p[1] + R)]
best = None
for order in permutations(range(3)):
    pts = [(0, 0)] + [(parts[i][1], parts[i][2]) for i in order] + [(100, 100)]
    total = sum(cost(pts[i], pts[i + 1]) for i in range(4))
    if best is None or total < best[0]:
        best = (total, order)
print(" ".join(parts[i][0] for i in best[1]))
print(f"{best[0]:.2f}")
