import sys

def solve():
    # 读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # N: 精灵球数量, M: 初始体力, K: 野生小精灵数量
    N = int(input_data[0])
    M = int(input_data[1])
    K = int(input_data[2])
    
    # 初始化DP表，dp[i][j]表示用i个球和j点伤害能抓到的最多精灵
    # 体力必须大于0，所以伤害上限是 M-1
    dp = [[0] * (M) for _ in range(N + 1)]
    
    ptr = 3
    for _ in range(K):
        cost_ball = int(input_data[ptr])
        cost_health = int(input_data[ptr+1])
        ptr += 2
        
        # 二维0/1背包，逆序遍历
        for i in range(N, cost_ball - 1, -1):
            # 体力限制：总伤害不能超过 M-1
            for j in range(M - 1, cost_health - 1, -1):
                if dp[i - cost_ball][j - cost_health] + 1 > dp[i][j]:
                    dp[i][j] = dp[i - cost_ball][j - cost_health] + 1
    
    # 最大收服数量
    max_catch = dp[N][M-1]
    
    # 寻找达到最大收服数量时的最小伤害
    min_damage = M - 1
    for j in range(M):
        if dp[N][j] == max_catch:
            min_damage = j
            break
            
    # 剩余体力
    remaining_health = M - min_damage
    
    print(f"{max_catch} {remaining_health}")

if __name__ == "__main__":
    solve()
