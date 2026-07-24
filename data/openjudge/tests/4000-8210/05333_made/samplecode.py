# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import heapq

def minimum_cost(planks):
    heapq.heapify(planks)  # 将木板列表转换为最小堆
    total_cost = 0

    while len(planks) > 1:
        # 取出最短的两块木板
        shortest1 = heapq.heappop(planks)
        shortest2 = heapq.heappop(planks)

        # 计算切割的成本，并将切割后得到的木板长度加入堆
        cost = shortest1 + shortest2
        total_cost += cost
        heapq.heappush(planks, cost)

    return total_cost

# 读取输入
n = int(input())
planks = []
for _ in range(n):
    length = int(input())
    planks.append(length)

# 调用函数计算最小成本
result = minimum_cost(planks)

# 输出结果
print(result)
