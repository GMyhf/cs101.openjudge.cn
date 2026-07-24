请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py

## 安全的密码

在一个遥远的王国中，国王想要为他的秘密宝库创建一个密码，这个密码不仅要足够复杂以避免被猜到，还要简短易记。为了找到这样的密码，国王的手下首先收集了所有已知的被他人知晓的密码，并将他们压缩成了一个单一的、长字符串，他们认为这个字符串的子序列都是不安全的。因此，他们希望找到最短的、不是这个字符串子序列的新密码，作为国王秘密宝库的密码。

由于时间紧迫，手下们找到你——王国中首屈一指的计算大手子，请你告诉他们安全密码的最短长度。

注意，一个字符串的子序列是指原字符串删除任意个字符得到的字符串，包括原串本身和空串。



**输入**

一行一个只包含小写字符的字符串 S，(1 ≤ |S| ≤ 10^5）。

**输出**

一行输出一个正整数，表示最短密码的长度。

样例输入

```
abcdefghijklmnopqrstuvwxyz
```

样例输出

```
2
```

提示

greedy





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
    # 读取输入字符串
    s = sys.stdin.read().strip()
    
    # 如果字符串为空，最短不存在的子序列长度是 1 (任意一个小写字母)
    if not s:
        print(1)
        return

    ans = 1      # 初始最短长度为 1
    seen = set() # 用于记录当前块内出现的字母
    
    for char in s:
        seen.add(char)
        # 一旦凑齐了 26 个字母
        if len(seen) == 26:
            ans += 1    # 说明长度为 ans 的所有子序列都能凑齐了，目标长度加 1
            seen.clear() # 开始寻找下一个完整的“字母表块”
            
    # 输出结果
    print(ans)

if __name__ == "__main__":
    solve()
```

