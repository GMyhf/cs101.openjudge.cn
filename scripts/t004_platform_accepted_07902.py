# External reference: cs101.openjudge.cn practice/07902 statistics, Accepted solution 45388185.
# Source: http://cs101.openjudge.cn/practice/solution/45388185/
# Statistics: http://cs101.openjudge.cn/practice/07902/statistics/
# License: not declared on submission page; no license inferred
def max_peanuts(M, N, K, field):
    # 提取所有有花生的位置及其数量
    peanuts = []
    for i in range(M):
        for j in range(N):
            if field[i][j] > 0:
                peanuts.append((field[i][j], i, j))
    
    # 按照花生数量从大到小排序
    peanuts.sort(reverse=True, key=lambda x: x[0])
    
    # 初始化当前时间和采摘的花生总数
    current_time = 0
    total_peanuts = 0
    
    # 初始位置设为路边
    current_pos = (-1, 0)
    
    for peanut in peanuts:
        amount, x, y = peanut
        
        # 计算从当前位置到该位置的时间
        if current_pos[0] == -1:  # 从路边跳到第一行
            time_to_reach = x + 1 + abs(current_pos[1] - y)
        else:
            time_to_reach = abs(current_pos[0] - x) + abs(current_pos[1] - y)
        
        if current_pos == (-1, 0):  # 从路边跳到第一行的时间
            current_time += (x + 1)
        else:
            current_time += time_to_reach
        
        # 采摘花生需要1单位时间
        current_time += 1
        
        if current_time + x + 1 <= K:
            total_peanuts += amount
            current_pos = (x, y)
        else:
            break
    
    return total_peanuts

# 读取输入
M, N, K = map(int, input().split())
field = []
for _ in range(M):
    field.append(list(map(int, input().split())))

# 计算并输出结果
result = max_peanuts(M, N, K, field)
print(result)
