# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 1724: ROADS
# Fenced code block index: 8
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01724/
# License: not declared in source collection; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
# 原写法是带剪枝的 DFS 枚举路径，最坏指数级，且 min_lengths 表为 (N+1)*(K+1)，满规模组超时。
# 改为按路径长度做 Dijkstra，状态 (城市, 已花费)；同一城市后弹出者若花费不更低即被支配而丢弃，O(R*K*log) 上界，实际远小。
import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    k, n, r = int(data[0]), int(data[1]), int(data[2])
    city_map = [[] for _ in range(n + 1)]   # 邻接表：city_map[s] 中为 (d, L, t)
    p = 3
    for _ in range(r):
        s, d, L, t = int(data[p]), int(data[p + 1]), int(data[p + 2]), int(data[p + 3])
        p += 4
        if s != d and t <= k:
            city_map[s].append((d, L, t))

    # min_cost[i]：已弹出的到达 i 的状态中最小花费；按长度递增弹出，花费不更低的状态必然更差
    min_cost = [k + 1] * (n + 1)
    heap = [(0, 0, 1)]                       # (总长度, 总花费, 城市)
    while heap:
        length, cost, s = heapq.heappop(heap)
        if cost >= min_cost[s]:
            continue
        min_cost[s] = cost
        if s == n:
            print(length)
            return
        for d, L, t in city_map[s]:
            c = cost + t
            if c < min_cost[d]:
                heapq.heappush(heap, (length + L, c, d))
    print(-1)


main()
