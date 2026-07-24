请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 成绩排序



> 数据结构与算法考试结束之后，小明同学按捺不住心中的急迫，不停地向助教询问自己的考试成绩与排名。但是，助教不被允许向学生提前透露关于成绩的具体信息。因此，小明调整了策略，向助教发出了一系列如下形式的提问：“A 同学的成绩是否比 B 同学高？” 助教回答了小明的所有问题，然后意识到，小明可能已经根据这些信息推断出了部分甚至全部同学的排名！虽然为时已晚，但助教们现在希望至少计算一下，根据已经提供的信息，可以确认多少个同学的具体排名。
>
> 假定所有同学的成绩各不相同，助教提供的信息不会产生矛盾，也不包含重复的信息。
>
> 输入
>
> 第一行包含两个整数 n，m，（2 <= n <= 50, 1 <= m <= 100）分别表示参与考试的学生人数，和小明做出提问数量。 [0, n) 内的每个整数表示一名同学。
>
> 接下来 m 行，每行包含 3 个数字 x, y, z，（0 <= x < y < n）表示对于 “x 同学的成绩是否比 y 同学高” 这个问题，助教给出的回答为 z。z 为0或1，1代表是，0代表否。
>
> 输出
>
> 一个整数，表示依据上述信息，可以确认多少同学在班级中的精确排名。
>
> 样例输入
>
> ```
> 5 4
> 0 2 0
> 1 2 0
> 2 3 0
> 2 4 0
> ```
>
> 样例输出
>
> ```
> 1
> ```
>
> 提示
>
> 提示1：给出的样例中，可以确定 2 号同学比 0，1 号同学成绩高，比 3，4 号同学成绩低。因此可以确认 2 号同学为第三名，其余同学的名次均无法确定，因此答案为 1。
>
> 提示2：小明确定某个同学排名的方法是，推断出恰好有 a 个同学的分数高于他，有 b 个同学的分数低于他，且 a+b=n-1。

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
    # 读取所有输入数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])

    # adj[i][j] 为 True 表示 i 的成绩高于 j
    adj = [[False] * n for _ in range(n)]

    # 读取 m 条关系
    idx = 2
    for _ in range(m):
        x = int(input_data[idx])
        y = int(input_data[idx + 1])
        z = int(input_data[idx + 2])
        idx += 3

        if z == 1:
            adj[x][y] = True
        else:
            adj[y][x] = True

    # 使用 Floyd-Warshall 算法求传递闭包
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if adj[i][k] and adj[k][j]:
                    adj[i][j] = True

    # 统计有多少个同学的排名可以被唯一确定
    confirmed_students = 0
    for i in range(n):
        count_worse = 0
        count_better = 0
        for j in range(n):
            if i != j:
                if adj[i][j]:  # j 的成绩比 i 低
                    count_worse += 1
                if adj[j][i]:  # j 的成绩比 i 高
                    count_better += 1

        if count_worse + count_better == n - 1:
            confirmed_students += 1

    print(confirmed_students)


if __name__ == "__main__":
    solve()
```

