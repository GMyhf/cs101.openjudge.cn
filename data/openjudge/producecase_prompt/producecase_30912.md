请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 累加树

> 给定一个二叉搜索树先序遍历序列，将其转换为一棵累加树，并输出累加树的按层次遍历序列。
>
> 累加树和原二叉树形态相同，设原树上结点v在累加树上对应的结点是u，则u的值是原树上所有大于等于v的结点的和。
>
> 样例数据如下图所示，原树结点的值在圈内，对应累加树结点的值在圈外
>
> <img src="https://raw.githubusercontent.com/GMyhf/img/main/img/1749112066.png" alt="img" style="zoom:33%;" />
>
> **输入**
>
> 第1行：一个整数n,表示二叉搜索树有n个结点( 1 <= n <= 100)。
> 第2行，n个整数，本行表示二叉搜索树的先序遍历序列。每个整数范围是 [0, 10000]
>
> **输出**
>
> 对应的累加树的按层次遍历序列
>
> 样例输入
>
> ```
> 9
> 4 1 0 2 3 6 5 7 8
> ```
>
> 样例输出
>
> ```
> 30 36 21 36 35 26 15 33 8
> ```





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
from collections import deque

# 定义二叉树节点
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

# 将节点插入到二叉搜索树中
def insert(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root

# 累加树转换辅助类
class GSTConverter:
    def __init__(self):
        self.running_sum = 0

    def convert(self, root):
        if not root:
            return
        # 反向中序遍历：先右子树，再当前节点，最后左子树
        self.convert(root.right)
        
        # 累加当前节点的值
        self.running_sum += root.val
        root.val = self.running_sum
        
        self.convert(root.left)

# 层次遍历二叉树
def level_order_traversal(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result

def main():
    # 读取标准输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    preorder = [int(x) for x in input_data[1:n+1]]
    
    if n == 0:
        return

    # 1. 重建二叉搜索树
    root = None
    for val in preorder:
        root = insert(root, val)
    
    # 2. 转换为累加树
    converter = GSTConverter()
    converter.convert(root)
    
    # 3. 层次遍历
    ans = level_order_traversal(root)
    
    # 输出结果
    print(*(ans))

if __name__ == '__main__':
    main()
```

