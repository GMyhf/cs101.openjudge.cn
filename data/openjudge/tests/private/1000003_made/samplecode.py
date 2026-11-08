# 1000003 论文投稿前的关键路径：参考实现（仓库交接件，Claude 2026-11-08 编写，不套用外部许可）。
# Kahn 拓扑排序求最早开始时间，逆拓扑序求最迟开始时间；排不出全部任务说明有环。
import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    t = [0] + [int(x) for x in data[2:2 + n]]
    succ = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    pos = 2 + n
    for _ in range(m):
        u, v = int(data[pos]), int(data[pos + 1])
        pos += 2
        succ[u].append(v)
        indeg[v] += 1
    order = []
    queue = deque(i for i in range(1, n + 1) if indeg[i] == 0)
    es = [0] * (n + 1)
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in succ[u]:
            es[v] = max(es[v], es[u] + t[u])
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if len(order) < n:
        print(-1)
        return
    total = max(es[i] + t[i] for i in range(1, n + 1))
    lf = [total] * (n + 1)
    for u in reversed(order):
        for v in succ[u]:
            lf[u] = min(lf[u], lf[v] - t[v])  # 后继的最迟开始时间
    critical = [i for i in range(1, n + 1) if lf[i] - t[i] == es[i]]
    print(total)
    print(' '.join(map(str, critical)))


main()
