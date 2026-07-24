请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 多少人知道秘密

在第 1 天，有一个人发现了一个秘密。
给你一个整数 delay ，表示每个人会在发现秘密后的 第delay 天及以后，每天将秘密告诉给一个新人。同时给你一个整数 forget ，表示每个人在发现秘密的后的第 forget 天及之后会忘记这个秘密。一个人不能 在忘记秘密那一天及之后的日子里把秘密告诉别人。

给你一个整数 n ，请计算第 n 天结束时，知道秘密的人数。由于答案可能会很大，请你将结果对
1000000007取余后输出。

**输入**

一行，包括三个整数n,delay和forget ( 1 <= n <= 100)

**输出**

第 n 天结束时，知道秘密的人数对1000000007取余后的结果。

样例输入

```
#输入样例1
4 1 3
#输入样例2
90 3 9
```

样例输出

```
#输出样例1
6
#输出样例2
386701165
```

提示

对样例1的解释：
第 1 天：第一个知道秘密的人为 A 。（一个人知道秘密）
第 2 天：A 把秘密分享给 B 。（两个人知道秘密）
第 3 天：A 和 B 把秘密分享给 2 个新的人 C 和 D 。（四个人知道秘密）
第 4 天：A 忘记了秘密，B、C、D 分别分享给 3 个新的人。（六个人知道秘密）



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


for epoch in range(30):
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
    
    n = int(input_data[0])
    delay = int(input_data[1])
    forget = int(input_data[2])
    
    MOD = 1000000007
    
    # dp[i] 表示第 i 天新知道秘密的人数
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        # 能在第 i 天分享秘密的人，其得知秘密的日期 j 需满足：
        # i - forget < j <= i - delay
        start = max(1, i - forget + 1)
        end = i - delay
        
        current_shares = 0
        if start <= end:
            for j in range(start, end + 1):
                current_shares = (current_shares + dp[j]) % MOD
        dp[i] = current_shares
        
    # 计算在第 n 天结束时，还没忘记秘密的人数之和
    # 还没忘记秘密的人，其得知秘密的日期 j 需满足：
    # j + forget > n  =>  j >= n - forget + 1
    total_knowing = 0
    start = max(1, n - forget + 1)
    for j in range(start, n + 1):
        total_knowing = (total_knowing + dp[j]) % MOD
        
    print(total_knowing)

if __name__ == '__main__':
    solve()
```

