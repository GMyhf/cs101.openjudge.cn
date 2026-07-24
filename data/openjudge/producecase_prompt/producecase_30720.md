请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 30720:败方树的构建与维护

**败方树（Loser Tree）** 是一种用于多路归并排序的完全二叉树结构。它通过维护每场“比赛”的失败者，使得获取当前所有元素中的最小值以及在修改元素后更新状态的效率达到最优。

**构建规则：**

1. **叶子结点（外部结点）**：数组中的 n 个元素作为败方树的叶子结点。
2. **内部结点**：败方树有 n 个内部结点（包含一个位于根部上方的“冠军结点”）。
   - 每个内部结点存储该场比赛的**败者**（数值较大者）。
   - 每场比赛的**胜者**（数值较小者）将继续向上晋级，与父结点中记录的上一轮败者进行比较。
   - **根部上方结点**：存储最终的全局胜者（冠军）。
3. **树形结构**：本题要求构建一棵基于数组位置的**完全二叉树**。对于 n=8 的情况，第一轮由数组相邻元素 `(0,1), (2,3), (4,5), (6,7)` 两两对决，胜者进入下一轮，直至选出冠军。

**任务：** 给定一个长度为 n 的整数数组，构建初始败方树。随后进行 m 次修改操作，每次修改数组中的一个元素，并同步更新败方树。要求输出初始状态及每次修改后，所有**内部结点（含冠军结点）**代表的数值。

**输入**

第一行：两个整数 n 和 m。n 代表数组元素个数，m 代表修改次数。（n 通常为 2 的幂次，以保证完全二叉树的对称性）。
第二行：n 个整数，代表数组的初始元素。
接下来 m 行：每行包含两个整数 idx 和 val，表示将数组下标为 idx 的元素修改为 val（下标从 0 开始）。

**输出**

输出共 m+1 行。
第一行：初始构建后，败方树内部结点的整数序列。
随后 m 行：每次修改后，败方树内部结点的整数序列。
注意：输出顺序为内部结点的层次遍历顺序（从上到下，从左到右，第一位是全局冠军）。

样例输入

```
8 1
10 9 20 6 16 12 90 17
3 15
```

样例输出

```
6 12 9 17 10 20 16 90
9 12 15 17 10 20 16 90

#解释第一行输出
第一轮对决 (叶子层)：
10 vs 9 -> 胜者 9, 败者 10；20 vs 6 -> 胜者 6, 败者 20；
16 vs 12 -> 胜者 12, 败者 16；90 vs 17 -> 胜者 17, 败者 90

第二轮对决 (半决赛)：
9 vs 6 -> 胜者 6, 败者 9；12 vs 17 -> 胜者 12, 败者 17

第三轮对决 (决赛)：
6 vs 12 -> 胜者 6, 败者 12

冠军节点： 6

层次遍历内部节点结果： 6 (冠军), 12 (决赛败者), 9 (半决赛败者L), 17 (半决赛败者R), 10, 20, 16, 90 (初始败者)
```

提示

数据范围：1 <= n <= 10^5，0 <= m <= 10^5，注意：保证 (n+1)×(m+1)≤2×10^6
数组元素为整数。



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

class Node:
    # 使用 __slots__ 减少内存占用，加快属性访问
    __slots__ = ['val', 'win', 'left', 'right', 'parent']
    def __init__(self, v=0):
        self.val = v      # 内部节点存储：败者 (Loser)
        self.win = v      # 内部节点存储：该场胜者 (Winner)，用于向上传递
        self.left = None
        self.right = None
        self.parent = None

def solve():
    # 快速读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data: return
    n, m = int(input_data[0]), int(input_data[1])
    vals = [int(x) for x in input_data[2:2+n]]
    
    # 1. 初始构建树：O(n)
    # 将初始值包装为叶子节点
    leaves = [Node(v) for v in vals]
    queue = deque(leaves)
    
    # 两两分组模拟比赛，构建完全二叉树
    while len(queue) > 1:
        l = queue.popleft()
        r = queue.popleft()
        # 创建比赛节点：val存大值(败者)，win存小值(胜者)
        match = Node()
        match.val, match.win = max(l.win, r.win), min(l.win, r.win)
        match.left, match.right = l, r
        l.parent = r.parent = match
        queue.append(match)
    
    # 创建顶层冠军节点 (只有一个左孩子)
    battle_root = queue.popleft()
    root = Node(battle_root.win)
    root.left, battle_root.parent = battle_root, root

    # 2. 预处理：确定内部节点的输出顺序
    # 题目要求输出内部节点（从上到下，从左到右），且结构不变
    internal_nodes = []
    bfs_q = deque([root])
    while bfs_q and len(internal_nodes) < n:
        curr = bfs_q.popleft()
        internal_nodes.append(curr)
        if curr.left: bfs_q.append(curr.left)
        if curr.right: bfs_q.append(curr.right)

    # 辅助函数：按序输出当前树的所有内部节点值
    def print_internal_nodes():
        sys.stdout.write(" ".join(str(node.val) for node in internal_nodes) + "\n")

    # 输出初始状态
    print_internal_nodes()

    # 3. 处理修改：每次 O(log n + n)
    ptr = 2 + n
    for _ in range(m):
        idx, new_val = int(input_data[ptr]), int(input_data[ptr+1])
        ptr += 2
        
        # 向上更新路径
        curr_leaf = leaves[idx]
        curr_leaf.win = new_val
        p = curr_leaf.parent
        while p:
            if p.right: # 普通比赛节点：有两个孩子
                p.val = max(p.left.win, p.right.win)
                p.win = min(p.left.win, p.right.win)
            else:       # 顶层冠军节点：只有一个孩子
                p.val = p.win = p.left.win
            p = p.parent
        
        print_internal_nodes()

if __name__ == "__main__":
    solve()
```

