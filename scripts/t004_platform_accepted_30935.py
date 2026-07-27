# External reference: /practice/30935/statistics/
# Accepted submission: 52760559
# Source: http://cs101.openjudge.cn/practice/solution/52760559/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    orders = []
    index = 1
    for i in range(n):
        d = int(input_data[index])
        p = int(input_data[index + 1])
        index += 2
        orders.append((d, p))
    
    # 1. 按照收益 P 从大到小排序
    orders.sort(key=lambda x: x[1], reverse=True)
    
    # 找到最大的截止时间，作为时间槽的上限
    max_deadline = max(d for d, p in orders)
    
    # 2. 初始化时间槽，False 表示该分钟空闲
    # 索引从 1 开始，所以大小为 max_deadline + 1
    time_slots = [False] * (max_deadline + 1)
    
    total_profit = 0
    
    # 3. 遍历每个订单，尝试安排
    for deadline, profit in orders:
        # 从截止时间往前找，寻找第一个空闲的分钟
        # 注意：最晚只能安排到第 1 分钟
        start_time = min(deadline, max_deadline)
        for t in range(start_time, 0, -1):
            if not time_slots[t]:
                time_slots[t] = True
                total_profit += profit
                break  # 安排成功，跳出循环处理下一个订单
                
    print(total_profit)

if __name__ == "__main__":
    solve()