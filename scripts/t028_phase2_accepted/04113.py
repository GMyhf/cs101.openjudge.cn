# External reference: http://cs101.openjudge.cn/practice/04113/statistics/
# Accepted submission: 52833036
# Source: http://cs101.openjudge.cn/practice/solution/52833036/
# License: not declared on the submission page; no license is inferred.

import sys
import math
from collections import defaultdict

def solve():
    # 使用生成器读取所有输入，这比逐行解析更能包容各种换行与空格排版
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)

    try:
        cases = int(next(iterator))
    except StopIteration:
        return

    for case_num in range(1, cases + 1):
        L = int(next(iterator))
        D = int(next(iterator))

        adj = defaultdict(list)

        # 1. 读入并解析 L 条地铁线路，并构图
        for _ in range(L):
            M = int(next(iterator))
            stations = []
            distances = []

            # 读取首站
            stations.append(next(iterator))
            # 依次读取 距离 和 车站
            for _ in range(M - 1):
                distances.append(int(next(iterator)))
                stations.append(next(iterator))

            # 将相邻车站建边
            for i in range(M - 1):
                u = stations[i]
                v = stations[i+1]
                w = distances[i]
                adj[u].append((v, w))
                adj[v].append((u, w))

        print(f"Case {case_num}:")

        # 2. 响应 D 次查询
        for _ in range(D):
            start = next(iterator)
            end = next(iterator)

            # 使用 DFS 查找起终点之间的唯一路径长度
            visited = set()
            def dfs(curr, target, dist):
                if curr == target:
                    return dist
                visited.add(curr)
                for neighbor, weight in adj[curr]:
                    if neighbor not in visited:
                        res = dfs(neighbor, target, dist + weight)
                        if res is not None:
                            return res
                return None

            distance = dfs(start, end, 0)

            # 3. 根据距离计算票价
            if distance <= 6000:
                fare = 3
            elif distance <= 12000:
                fare = 4
            elif distance <= 22000:
                fare = 5
            elif distance <= 32000:
                fare = 6
            else:
                # 32公里以上部分，每增加 20000 米（含不足）加 1 元
                fare = 6 + math.ceil((distance - 32000) / 20000)

            print(fare)

if __name__ == '__main__':
    solve()
