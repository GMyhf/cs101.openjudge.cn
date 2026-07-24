请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 30888:Phigros Rating

You are given N songs. Song i has difficulty di, a positive integer, and accuracy acci, an integer between 0 and 100.

The score contribution of a song is defined as follows:

| Condition      | Score contribution        |
| :------------- | :------------------------ |
| acci = 100     | di × 1.0                  |
| 95 ≤ acci ≤ 99 | di × (0.5 + acci / 200)   |
| 70 ≤ acci ≤ 94 | di × (acci / 150 - 1 / 6) |
| acci ≤ 69      | 0                         |

The player's rating is the average score contribution of the top B songs, that is, the songs with the highest score contributions. If there are fewer than B songs, all songs are used.

Output the rating with exactly 6 digits after the decimal point.

输入

The first line contains two integers N and B (1 ≤ N ≤ 105, 1 ≤ B ≤ 105).

The next N lines each contain two integers di and acci (1 ≤ di ≤ 100, 0 ≤ acci ≤ 100).

输出

Print a single real number: the rating with exactly 6 digits after the decimal point.

样例输入

```
#1
3 2
10 100
8 95
5 80

#2
5 3
15 100
12 98
10 72
8 65
20 85
```

样例输出

```
#1
8.900000

#2
11.626667
```

提示

In sample #1, the score contributions are 10.000000, 7.800000, and approximately 1.833333. The top 2 songs are the first two, so the answer is (10.0 + 7.8) / 2 = 8.900000.

In sample #2, the top 3 score contributions are 15.000000, 11.880000, and 8.000000. Their sum is 34.88, so the rating is 11.626667.



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
    # 使用 sys.stdin.read().split() 一次性读取所有数据，处理速度最快
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # N 是总条目数，B 是计算平均分时考虑的最大条目数
    n = int(input_data[0])
    b = int(input_data[1])
    
    scores = []
    current_idx = 2
    
    for _ in range(n):
        d = int(input_data[current_idx])
        acc = int(input_data[current_idx + 1])
        current_idx += 2
        
        # 根据题目给出的公式计算单项贡献分
        contribution = 0.0
        
        if acc == 100:
            contribution = float(d)
        elif acc >= 95:
            # 公式 1: d * (0.5 + acc / 200)
            contribution = d * (0.5 + acc / 200.0)
        elif acc >= 70:
            # 公式 2: d * (acc / 150 - 1/6)
            contribution = d * (acc / 150.0 - 1.0 / 6.0)
        else:
            # 低于 70 分不计分
            contribution = 0.0
            
        scores.append(contribution)
    
    # 贪心策略：将计算出的贡献分从大到小排序
    scores.sort(reverse=True)
    
    # 取前 B 个得分（如果总数不足 B，则取全部 N 个）
    k = min(n, b)
    
    if k == 0:
        print(f"{0.0:.6f}")
        return
    
    # 计算前 k 项的和
    top_sum = sum(scores[:k])
    
    # 计算平均分并保留 6 位小数
    result = top_sum / k
    print(f"{result:.6f}")

if __name__ == "__main__":
    solve()
```

