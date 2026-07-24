请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py



## 宠物小精灵之收服

- 总时间限制: 

  1000ms

- 内存限制: 

  65536kB

- 描述

  宠物小精灵是一部讲述小智和他的搭档皮卡丘一起冒险的故事。![img](http://media.openjudge.cn/images/upload/1340073461.jpg) 一天，小智和皮卡丘来到了小精灵狩猎场，里面有很多珍贵的野生宠物小精灵。小智也想收服其中的一些小精灵。然而，野生的小精灵并不那么容易被收服。对于每一个野生小精灵而言，小智可能需要使用很多个精灵球才能收服它，而在收服过程中，野生小精灵也会对皮卡丘造成一定的伤害（从而减少皮卡丘的体力）。当皮卡丘的体力小于等于0时，小智就必须结束狩猎（因为他需要给皮卡丘疗伤），而使得皮卡丘体力小于等于0的野生小精灵也不会被小智收服。当小智的精灵球用完时，狩猎也宣告结束。我们假设小智遇到野生小精灵时有两个选择：收服它，或者离开它。如果小智选择了收服，那么一定会扔出能够收服该小精灵的精灵球，而皮卡丘也一定会受到相应的伤害；如果选择离开它，那么小智不会损失精灵球，皮卡丘也不会损失体力。小智的目标有两个：主要目标是收服尽可能多的野生小精灵；如果可以收服的小精灵数量一样，小智希望皮卡丘受到的伤害越小（剩余体力越大），因为他们还要继续冒险。现在已知小智的精灵球数量和皮卡丘的初始体力，已知每一个小精灵需要的用于收服的精灵球数目和它在被收服过程中会对皮卡丘造成的伤害数目。请问，小智该如何选择收服哪些小精灵以达到他的目标呢？

- 输入

  输入数据的第一行包含三个整数：N(0 < N < 1000)，M(0 < M < 500)，K(0 < K < 100)，分别代表小智的精灵球数量、皮卡丘初始的体力值、野生小精灵的数量。 之后的K行，每一行代表一个野生小精灵，包括两个整数：收服该小精灵需要的精灵球的数量，以及收服过程中对皮卡丘造成的伤害。

- 输出

  输出为一行，包含两个整数：C，R，分别表示最多收服C个小精灵，以及收服C个小精灵时皮卡丘的剩余体力值最多为R。

- 样例输入

  `样例输入1： 10 100 5 7 10 2 40 2 50 1 20 4 20 样例输入2： 10 100 5 8 110 12 10 20 10 5 200 1 110 `

- 样例输出

  `样例输出1： 3 30 样例输出2： 0 100`

- 提示

  对于样例输入1：小智选择：(7,10) (2,40) (1,20) 这样小智一共收服了3个小精灵，皮卡丘受到了70点伤害，剩余100-70=30点体力。所以输出3 30 对于样例输入2：小智一个小精灵都没法收服，皮卡丘也不会收到任何伤害，所以输出0 100



producecase_template.py

```python
import random
import time
import os

# 确保 data 目录存在
os.makedirs("data", exist_ok=True)

def solve(m, n, k):
    """等价类划分问题逻辑 (ac.py 同款)"""
    groups = {}
    for num in range(m + 1, n):
        s = sum(map(int, str(num)))
        if s % k == 0:
            groups.setdefault(s, []).append(num)

    result_lines = []
    for s in sorted(groups):
        result_lines.append(','.join(map(str, sorted(groups[s]))))
    return result_lines


for epoch in range(20):
    # 随机生成 m, n, k
    m = random.randint(1, 9000)
    n = random.randint(m + 2, min(m + 2000, 10000))  # 保证范围合理
    k = random.randint(1, 9)

    # 写入输入文件
    with open(f"data/{epoch}.in", "w") as f:
        f.write(f"{m},{n},{k}\n")

    start = time.time()

    # 调用逻辑
    result = solve(m, n, k)

    end = time.time() - start
    print(f"[{epoch}] {end:.3f}s | m={m}, n={n}, k={k}")

    # 写入输出文件
    with open(f"data/{epoch}.out", "w") as f:
        if result:
            f.write("\n".join(result) + "\n")
        else:
            f.write("\n")  # 没有满足条件的情况


```



ac.py

```python
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
```

