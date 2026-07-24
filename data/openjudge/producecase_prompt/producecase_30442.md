请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。题面的heights[r][c]缺少范围，也请给出。



## Blackslex 赶时间

- [查看](http://cs101.openjudge.cn/2025fallcs101testing/M30442/)
- [提交](http://cs101.openjudge.cn/2025fallcs101testing/M30442/submit/)
- [统计](http://cs101.openjudge.cn/2025fallcs101testing/M30442/statistics/)
- [提问](http://cs101.openjudge.cn/2025fallcs101testing/clarify/M30442/)

- 总时间限制: 

  20000ms

- 单个测试点时间限制: 

  2000ms

- 内存限制: 

  256000kB

- 描述

  Blackslex 要迟到了！为了赶去上课，Blackslex 必须按特定顺序乘坐拥挤的电梯经过多个楼层。由于他是个黑客，他最多可以跳过其中一层楼而不被其他人发现。他所花的时间等于相邻楼层编号之差的绝对值之和。现在，请你找出在他最多跳过一层楼的前提下，所需的最短时间。更形式化地说，给定一个包含 n 个整数的数组 a = [a1, a_2, ..., a_n] ，你可以选择最多一个下标 k ∈‌ {1, 2, ..., n} 将其删除，使得删除后的数组 b = [a_1, ..., a_{k-1}, a_{k+1}, ..., a_n] 满足以下总和最小：![img](http://media.openjudge.cn/images/upload/3673/1766551195.png)请输出这个最小的总和。

- 输入

  第一行包含一个整数 t (1 ≤ t ≤ 10^4 )—— 测试用例的数量。  每个测试用例的第一行包含一个整数 n (3 ≤ n ≤ 2*10^5)—— 数组的大小。  第二行包含 n 个整数 ( a_1, a_2, ..., a_n) ( 1 ≤ a_i ≤ 100 )。  保证所有测试用例中 n 的总和不超过 (2*10^5)。

- 输出

  对每个测试用例，输出一个整数—— 所需的最短时间。

- 样例输入

  `3 5 4 15 1 7 9 3 2 4 8 6 11 13 17 19 23 29 `

- 样例输出

  `11 2 12 # 解释 例一，从数组 [4,15,1,7,9] 中删除第 2 个元素（即 15），得到 [4,1,7,9]， 所需时间为 |4-1| + |1-7| + |7-9| = 3 + 6 + 2 = 11。 例二，最优做法是删除第 3 个元素（即 8），得到 [2,4]，所需时间为 |2-4| = 2。`

- 提示

  greedy, implementation

- 来源

  2025fall, yan, https://codeforces.com/contest/2179/problem/B

  

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
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    tot = sum(abs(a[i]-a[i-1]) for i in range(1, n))

    ans = float('inf')
    cur = 0
    for i in range(n):
        if i == 0:
            cur = tot - abs(a[1] - a[0])
        elif i < n - 1:
            cur = tot - abs(a[i] - a[i-1]) - abs(a[i+1] - a[i]) + abs(a[i-1]-a[i+1])
        elif i == n - 1:
            cur = tot - abs(a[n-1] - a[n-2])

        ans = min(ans, cur)

    print(ans)

```

