请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py



## K柱汉诺塔



汉诺塔（Hanoi Tower），又称河内塔。

传说大梵天创造世界的时候做了三根金刚石柱子，按左、中、右排序。大梵天在左侧的柱子上，从下往上按照大小顺序摞着64片黄金圆盘，越靠下的圆盘越大。大梵天命令婆罗门把圆盘从下面开始按大小顺序重新摆放到右侧的柱子上。并且规定，任何时候，较小的圆盘都不能被较大的圆盘压着，且一个步骤只能移动一个圆盘。

小明复刻了这个故事为一套游戏道具，但他发现以他有生之年是移不完这些圆盘的——实际上，原始的故事下，需要 2^64-1 = 18446744073709551615（约 1.8 * 10^19）个步骤才能移动完毕。

基于此，他将柱子的数量改为k个，再将圆盘的数量改为n个。

请你帮助小明计算，修改后的游戏需要多少个步骤能操作完毕。

**输入**

输入为两个正整数k和n，以空格隔开，分别代表修改后的游戏有k根柱子和n个圆盘。

所有k, n, s为正整数
所有k满足3<=k<=100
所有n满足1<=n<=100
所有s满足1<=s<=2^31-1

提供三个输入样例。

**输出**

输出为一个正整数s，代表需要的最少步骤数。

提供三个输出样例。

**样例输入：**

```
3 3
===
4 5
===
6 2
```

**样例输出：**

```
7
===
13
===
3
```

#### 提示信息

所有k, n, s为正整数
所有k满足3<=k<=100
所有n满足1<=n<=100
所有s满足1<=s<=2^31-1





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
def solve():
    """
    计算 k 根柱子移动 n 个圆盘所需的最少步骤数
    """
    import sys
    
    # 从标准输入读取数据
    # 输入格式为一行：k n
    try:
        input_line = sys.stdin.readline().split()
        if not input_line:
            return
        k = int(input_line[0])
        n = int(input_line[1])
    except ValueError:
        return

    # dp[i][j] 表示：有 j 根柱子时，移动 i 个圆盘所需的最少步骤数
    # 初始化数组，大小为 (n+1) x (k+1)，初始值为无穷大
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]

    # === 初始化边界条件 ===

    # 1. 0 个圆盘需要 0 步
    for j in range(3, k + 1):
        dp[0][j] = 0

    # 2. 3 根柱子的情况（经典汉诺塔）
    # 公式为：2^i - 1
    for i in range(1, n + 1):
        dp[i][3] = 2**i - 1
        
    # 3. 任何柱子数量下，移动 1 个圆盘只需要 1 步
    for j in range(3, k + 1):
        dp[1][j] = 1

    # === 动态规划计算 ===
    
    # 外层循环：柱子数量 j 从 4 增加到 k
    for j in range(4, k + 1):
        # 内层循环：圆盘数量 i 从 2 增加到 n
        for i in range(2, n + 1):
            min_steps = float('inf')
            
            # 核心状态转移：
            # 尝试将 i 个盘子分割为两部分：
            # 上面 x 个盘子（使用 j 根柱子移动到缓冲区）
            # 下面 i-x 个盘子（使用 j-1 根柱子移动到目标区，因为有一根柱子被 x 占用了）
            # 最后再把 x 个盘子移回目标区（使用 j 根柱子）
            # 总步数 = 2 * dp[x][j] + dp[i-x][j-1]
            
            for x in range(1, i):
                current_steps = 2 * dp[x][j] + dp[i - x][j - 1]
                if current_steps < min_steps:
                    min_steps = current_steps
            
            dp[i][j] = min_steps

    # 输出结果
    print(dp[n][k])

if __name__ == "__main__":
    solve()
```

