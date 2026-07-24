请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 30889:Register Allocation

XiaoP is building a minimal code generator for expression trees. For a given expression tree, he wants to know how many registers are needed at minimum.

An expression corresponds to a rooted binary tree with n nodes. The root is node 1.

- A leaf node represents reading a value from memory.
- An internal node with one child represents a unary operation.
- An internal node with two children represents a binary operation.

Evaluation is performed on a register machine. The only allowed instructions are:

- `LOAD`: load a leaf's value into any free register. The register becomes occupied.
- `UNARY`: read one register and overwrite it with the unary result. The register stays occupied.
- `BINARY`: read two registers and write the result into one of them. The other register is freed.

Evaluation ends when the root's result is in some register. The register cost of the tree is the minimum possible peak number of simultaneously occupied registers, over all legal evaluation orders.

Given the tree, output its register cost.

输入

The first line contains an integer n (1 ≤ n ≤ 2 × 105).

The next n lines describe nodes 1,...,n. The first of these lines is `- -`, the placeholder for the root. For each i ≥ 2, the i-th line contains an integer p and a character d, meaning that node i is a child of node p (1 ≤ p < i). If d is `L`, it is the left child; if d is `R`, it is the right child.

It is guaranteed that no node has more than one left child or more than one right child.

输出

Print a single integer: the register cost of the tree.

样例输入

```
10
- -
1 L
2 L
3 R
3 L
1 R
6 L
7 L
7 R
6 R
```

样例输出

```
3
```

提示

In the sample, the tree has root 1 with two main subtrees rooted at nodes 2 and 6. The minimum possible peak number of occupied registers is 3.



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
    # 使用 sys.stdin.read().split() 一次性读取所有输入，提高在大数据量下的性能
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    if n == 0:
        return

    # 初始化左孩子和右孩子数组，0 表示没有孩子
    left_child = [0] * (n + 1)
    right_child = [0] * (n + 1)

    # 跳过根节点的占位符（即输入中的 "- -"）
    # input_data[1] 和 input_data[2] 分别是根节点的占位信息
    
    # 从第 3 个元素开始，每两个一组表示 parent 和 direction
    idx = 3
    for i in range(2, n + 1):
        p = int(input_data[idx])
        direction = input_data[idx + 1]
        idx += 2
        
        if direction == 'L':
            left_child[p] = i
        else:
            right_child[p] = i

    # dp[u] 表示以 u 为根的子树的计算值
    dp = [0] * (n + 1)

    # 按照节点编号从大到小遍历。
    # 这种遍历方式的前提是：父节点的编号一定小于子节点的编号（题目输入逻辑通常满足此点）。
    # 如果不满足，则需要使用后序遍历（DFS）。
    for u in range(n, 0, -1):
        l = left_child[u]
        r = right_child[u]

        if l == 0 and r == 0:
            # 情况 1：叶子节点，初始值为 1
            dp[u] = 1
        elif l != 0 and r == 0:
            # 情况 2：只有左孩子，继承左孩子的值
            dp[u] = dp[l]
        elif l == 0 and r != 0:
            # 情况 3：只有右孩子，继承右孩子的值
            dp[u] = dp[r]
        else:
            # 情况 4：左右孩子都有
            x = dp[l]
            y = dp[r]
            if x == y:
                # 如果两个孩子值相等，当前节点值加 1
                dp[u] = x + 1
            else:
                # 如果不等，取较大的那个值
                dp[u] = max(x, y)

    # 输出根节点（1号节点）的计算结果
    print(dp[1])

if __name__ == "__main__":
    solve()
```

