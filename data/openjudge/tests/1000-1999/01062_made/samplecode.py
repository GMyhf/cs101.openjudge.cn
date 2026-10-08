# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1062: 昂贵的聘礼
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01062/
# License: not declared; no license is inferred.
# 2300015881 赵凌哲 光华管理学院
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 参考解：原先引用的 2020fall 代码是沿路径的指数级 DFS，N=100 的稠密数据会超时；旧生成器每件物品都没有替代品（X=0），
# 答案恒为 P1，等于没测。这里改成：枚举包含酋长等级的等级窗口 [lo, lo+M]（lo 取现有等级），窗口内 Dijkstra。
import sys, heapq
d = list(map(int, sys.stdin.read().split()))
M, N = d[0], d[1]
p = 2
P = []; Lv = []; adj = [[] for _ in range(N)]
for i in range(N):
    pi, li, x = d[p], d[p + 1], d[p + 2]; p += 3
    P.append(pi); Lv.append(li)
    for _ in range(x):
        t, v = d[p], d[p + 1]; p += 2
        adj[t - 1].append((i, v))      # 拿到 t 之后，再付 v 换到 i
INF = float("inf")
best = INF
for lo in sorted(set(Lv)):
    if not (Lv[0] - M <= lo <= Lv[0]):
        continue
    hi = lo + M
    ok = [lo <= l <= hi for l in Lv]
    dist = [P[i] if ok[i] else INF for i in range(N)]
    pq = [(dist[i], i) for i in range(N) if ok[i]]
    heapq.heapify(pq)
    while pq:
        du, u = heapq.heappop(pq)
        if du > dist[u]:
            continue
        for w, v in adj[u]:
            if ok[w] and du + v < dist[w]:
                dist[w] = du + v
                heapq.heappush(pq, (dist[w], w))
    best = min(best, dist[0])
print(best)
