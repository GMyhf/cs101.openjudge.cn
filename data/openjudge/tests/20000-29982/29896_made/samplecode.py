# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    X = int(data[0])
    N = int(data[1])
    coins = list(map(int, data[2:2+N]))
    
    # 去除大于 X 的硬币（无用）
    coins = [c for c in coins if c <= X]
    if not coins:
        if X == 0:
            return 0
        else:
            return -1
    
    # 排序
    coins.sort()
    
    # 必须要有 1，否则无法覆盖 1
    if coins[0] > 1:
        return -1
    
    max_reach = 0  # 当前能覆盖 [1, max_reach]
    count = 0      # 使用的硬币数量
    
    while max_reach < X:
        # 选择满足 coin <= max_reach + 1 的最大面值硬币
        candidate = -1
        for coin in coins:
            if coin <= max_reach + 1:
                candidate = coin
            else:
                break  # 因为已排序，后面的更大
        
        if candidate == -1:
            return -1  # 无法扩展
        
        max_reach += candidate
        count += 1
        
        if max_reach >= X:
            break
    
    return count

# 主程序
print(solve())
