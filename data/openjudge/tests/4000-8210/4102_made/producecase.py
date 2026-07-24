import random
import time
import os

# 确保 data 目录存在
os.makedirs("data", exist_ok=True)

def solve(N, M, K, items):
    """
    模拟 ac.py 的逻辑计算结果
    N: 精灵球数量
    M: 皮卡丘初始体力
    K: 野生小精灵数量
    items: 一个列表，包含 (cost_ball, cost_health)
    """
    # 初始化DP表，dp[i][j]表示用i个球和j点伤害能抓到的最多精灵
    # 体力必须大于0，所以伤害上限是 M-1 (索引 0 到 M-1)
    dp = [[0] * (M) for _ in range(N + 1)]
    
    for cost_ball, cost_health in items:
        # 二维0/1背包，逆序遍历
        # 如果当前精灵需要的球大于拥有的球 N，或者伤害大于等于体力 M，则无法收服，直接跳过循环
        for i in range(N, cost_ball - 1, -1):
            # 体力限制：总伤害不能超过 M-1
            for j in range(M - 1, cost_health - 1, -1):
                if dp[i - cost_ball][j - cost_health] + 1 > dp[i][j]:
                    dp[i][j] = dp[i - cost_ball][j - cost_health] + 1
    
    # 最大收服数量
    max_catch = dp[N][M-1]
    
    # 寻找达到最大收服数量时的最小伤害
    min_damage = M - 1
    # 遍历伤害维度，找到第一个（最小伤害）达到 max_catch 的位置
    for j in range(M):
        if dp[N][j] == max_catch:
            min_damage = j
            break
            
    # 剩余体力 = 初始体力 - 最小伤害
    remaining_health = M - min_damage
    
    return f"{max_catch} {remaining_health}"

def generate_random_case(epoch):
    """
    根据轮次生成不同规模的数据
    题目限制: 0 < N < 1000, 0 < M < 500, 0 < K < 100
    """
    if epoch == 0:
        # 样例1
        N, M, K = 10, 100, 5
        items = [(7, 10), (2, 40), (2, 50), (1, 20), (4, 20)]
        return N, M, K, items
    
    if epoch == 1:
        # 样例2
        N, M, K = 10, 100, 5
        items = [(8, 110), (12, 10), (20, 10), (5, 200), (1, 110)]
        return N, M, K, items

    if epoch < 5:
        # 小规模随机数据
        N = random.randint(5, 50)
        M = random.randint(10, 100)
        K = random.randint(1, 10)
    elif epoch < 15:
        # 中大规模随机数据 (接近题目上限)
        N = random.randint(100, 999)
        M = random.randint(100, 499)
        K = random.randint(50, 99)
    else:
        # 边界/极限数据
        N = random.randint(900, 999)
        M = random.randint(450, 499)
        K = 99 # 最大K

    items = []
    for _ in range(K):
        # 为了保证有解和无解的情况混合：
        # 消耗球数：大部分在 1 到 N/2 之间，偶尔生成很大的无法捕捉的
        # 消耗体力：大部分在 0 到 M/2 之间
        
        # 90% 概率生成普通精灵，10% 概率生成很难/无法捕捉的精灵
        if random.random() < 0.9:
            ball_cost = random.randint(1, max(1, N // 2))
            dmg_cost = random.randint(0, max(1, M // 2))
        else:
            ball_cost = random.randint(N // 2, N + 10)
            dmg_cost = random.randint(M // 2, M + 10)
            
        items.append((ball_cost, dmg_cost))
        
    return N, M, K, items

def main():
    # 生成 20 组测试数据
    for epoch in range(20):
        # 1. 生成数据
        N, M, K, items = generate_random_case(epoch)
        
        # 2. 写入 .in 文件
        in_path = f"data/{epoch}.in"
        with open(in_path, "w") as f:
            f.write(f"{N} {M} {K}\n")
            for ball, dmg in items:
                f.write(f"{ball} {dmg}\n")
        
        # 3. 运行逻辑并计时
        start = time.time()
        result_str = solve(N, M, K, items)
        end = time.time() - start
        
        print(f"[{epoch}] {end:.4f}s | N={N}, M={M}, K={K}")
        
        # 4. 写入 .out 文件
        out_path = f"data/{epoch}.out"
        with open(out_path, "w") as f:
            f.write(result_str + "\n")

if __name__ == "__main__":
    main()
