# External reference: http://cs101.openjudge.cn/practice/30868/statistics/
# Accepted submission: 52727511
# Source: http://cs101.openjudge.cn/practice/solution/52727511/
# License: not declared on the submission page; no license is inferred.

import heapq
import sys

def solve():
    # 使用 fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # 读取 a, b, c
    a = int(input_data[0])
    b = int(input_data[1])
    c = int(input_data[2])

    # 过滤掉 0 步长并去重
    steps = sorted(list(set(x for x in [a, b, c] if x > 0)))

    q_idx = 3
    q = int(input_data[q_idx])
    q_idx += 1

    # 特判：如果所有步长都是 0
    if not steps:
        results = []
        for i in range(q):
            h = int(input_data[q_idx + i])
            results.append("Yes" if h == 0 else "No")
        sys.stdout.write("\n".join(results) + "\n")
        return

    # 选择最小的步长作为模数
    m = steps[0]

    # 如果最小步长是 1，所有楼层都可达
    if m == 1:
        results = ["Yes"] * q
        sys.stdout.write("\n".join(results) + "\n")
        return

    # Dijkstra 算法初始化
    # dist[i] 存储余数为 i 的最小可达楼层高度
    dist = [float('inf')] * m
    dist[0] = 0

    pq = [(0, 0)] # (distance, remainder)

    # 其余步长用于转移
    other_steps = steps[1:]

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue

        for s in other_steps:
            v = (u + s) % m
            new_dist = d + s
            if dist[v] > new_dist:
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    # 处理询问
    ans = []
    for i in range(q):
        h = int(input_data[q_idx + i])
        if h >= dist[h % m]:
            ans.append("Yes")
        else:
            ans.append("No")

    sys.stdout.write("\n".join(ans) + "\n")

if __name__ == "__main__":
    solve()
