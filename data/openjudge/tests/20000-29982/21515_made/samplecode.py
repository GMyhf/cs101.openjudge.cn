# Source: /home/ubuntu/hongfei/2024spring-cs201/2024spring_dsa_problems.md
import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it));
    p = int(next(it));
    k = int(next(it))

    graph = [[] for _ in range(n + 1)]
    max_edge = 0
    for _ in range(p):
        a = int(next(it));
        b = int(next(it));
        l = int(next(it))
        graph[a].append((b, l))
        graph[b].append((a, l))
        if l > max_edge:
            max_edge = l

    # 特殊情况：如果 1 和 n 不连通？0-1 BFS 会处理（dist[n] 保持 inf）

    def can(x):
        # dist[i] = 从 1 到 i 路径上 权重 > x 的边的最小数量
        INF = 10 ** 9
        dist = [INF] * (n + 1)
        dist[1] = 0
        dq = deque([1])

        while dq:
            u = dq.popleft()
            for v, w in graph[u]:
                # 如果 w <= x，这条边免费（不计入代价）；否则代价为1
                cost = 1 if w > x else 0
                new_cost = dist[u] + cost
                if new_cost < dist[v] and new_cost <= k:  # 剪枝：超过k没必要继续
                    dist[v] = new_cost
                    if cost == 0:
                        dq.appendleft(v)
                    else:
                        dq.append(v)
        return dist[n] <= k

    # 二分答案：最小的 x 使得 can(x) 为 True
    lo = 0
    hi = max_edge + 1  # 注意：答案可能为0，也可能需要比max_edge更大？但题目允许K>=0，所以max_edge足够

    # 但注意：有可能最优解是0（所有边<=0？但Li>=0），或甚至不需要任何边>lim
    # 另外，有可能即使 lim = max_edge 也不连通 → 输出 -1

    if not can(hi):
        print(-1)
        return

    ans = -1
    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid):
            ans = mid
            hi = mid
        else:
            lo = mid + 1

    print(ans)


if __name__ == "__main__":
    main()
