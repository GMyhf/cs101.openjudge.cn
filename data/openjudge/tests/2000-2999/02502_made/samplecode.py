# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2502: Subway
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02502/
# License: not declared in source collection; no license is inferred.
import sys
import math
import heapq

# 计算两点之间的欧几里得距离
def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# 读取起点（家）和终点（学校）坐标
sx, sy, ex, ey = map(int, input().split())

# min_time: 记录从起点到每个地铁站/终点的最短时间（单位：小时）
min_time = {}

# rails: 记录所有地铁连接（双向）
rails = set()

# 读取所有地铁线路
while True:
    try:
        rail = list(map(int, input().split()))
        if rail == [-1, -1]:
            break
        # 解析当前地铁线路的所有站点
        stations = [(rail[2 * i], rail[2 * i + 1]) for i in range(len(rail) // 2 - 1)]

        for j, station in enumerate(stations):
            # 初始化所有地铁站点的最短时间为无穷大
            min_time[station] = float('inf')
            # 添加地铁线路中相邻站点的双向连接
            if j != len(stations) - 1:
                rails.add((station, stations[j + 1]))
                rails.add((stations[j + 1], station))
    except EOFError:
        break  # 输入结束

# 把起点和终点加入时间表中
min_time[(sx, sy)] = 0  # 起点时间为 0
min_time[(ex, ey)] = float('inf')  # 终点初始化为无穷大

# 使用小根堆实现 Dijkstra 算法，按时间升序处理节点
min_heap = [(0, sx, sy)]  # (当前耗时, 当前x, 当前y)

while min_heap:
    curr_time, x, y = heapq.heappop(min_heap)

    # 如果当前耗时不是最短路径中记录的值，说明已经被更新，跳过
    if curr_time > min_time[(x, y)]:
        continue

    # 如果已经到达终点，提前结束
    if (x, y) == (ex, ey):
        break

    # 遍历所有可达点（隐式图）
    for position in min_time.keys():
        if position == (x, y):
            continue  # 自己跳过
        nx, ny = position

        # 计算当前位置到下一个点的距离
        dis = get_distance(x, y, nx, ny)

        # 判断是否为地铁连接：地铁速度是步行的4倍
        rail_factor = 4 if ((position, (x, y)) in rails or ((x, y), position) in rails) else 1

        # 计算到该点的所需时间（单位：小时）
        new_time = curr_time + dis / (10000 * rail_factor)

        # 如果时间更短，则更新并加入堆中
        if new_time < min_time[position]:
            min_time[position] = new_time
            heapq.heappush(min_heap, (new_time, nx, ny))

# 输出从起点到终点的最短时间，转换为分钟并四舍五入
print(round(min_time[(ex, ey)] * 60))
