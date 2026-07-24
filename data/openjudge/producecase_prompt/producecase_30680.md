请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## M30680:森林局部排序遍历

给定一个**森林**（由一棵或多棵树组成）。对于森林中的每一棵树，遍历规则如下：
1. **局部排序规则**：遍历到每个节点时，将**该节点本身**与其**所有直接子节点**的值放在一起，按从小到大的顺序进行遍历。
2. **递归规则**：
   - 如果遇到的是子节点，则递归进入该子节点进行深度遍历。
   - 如果遇到的是当前节点本身，则输出该节点的值。
3. **森林规则**：如果森林中存在多棵树，首先找到所有树的根节点，按照**根节点的值从小到大**的顺序依次对每棵树进行上述遍历。

每个节点的值为互不相同的正整数。

#### 输入
第一行：节点总个数 $n$ ($n < 1000$)。
接下来的 $n$ 行：每行代表一个节点的结构。第一个数是此节点的值，之后的数表示它的所有直接子节点的值。如果没有子节点，该行只有一个数。

#### 输出
输出遍历结果，每行一个节点的值。

**输入样例：**
```text
4
15 2
2
8 20
20
```

**输出样例：**

```text
8
20
2
15
# 解释：
1. 该输入构成了两棵树（一个森林）：
   - 第一棵树：根为 15，子节点为 2。
   - 第二棵树：根为 8，子节点为 20。
2. 根节点集合为 {8, 15}。按规则，先处理较小的根 8。
3. 局部排序遍历根 8
4. 局部排序遍历根 15
```



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

# 增加递归深度限制，防止深层树结构导致溢出
sys.setrecursionlimit(2000)

def solve():
    # 读取所有输入并按行处理
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    # 第一行是节点个数 n
    try:
        n = int(input_data[0].strip())
    except (ValueError, IndexError):
        return

    adj = {}
    all_nodes = set()
    all_children = set()
    
    # 处理接下来的 n 行输入
    line_count = 0
    for i in range(1, len(input_data)):
        if line_count >= n:
            break
        
        line = input_data[i].strip()
        if not line:
            continue
        
        parts = list(map(int, line.split()))
        parent = parts[0]
        children = parts[1:]
        
        adj[parent] = children
        all_nodes.add(parent)
        for child in children:
            all_children.add(child)
            
        line_count += 1
    
    # 根节点是所有节点中没有出现在子节点集合里的那个
    # 注意：即便某些叶子节点在输入中只有一行且没有子节点，它们也会被加入 all_nodes
    roots = list(all_nodes - all_children)
    
    # 如果没有找到根节点（理论上树结构必然有根），直接退出
    if not roots:
        return
    
    # 虽然题目暗示是一棵树，但如果是森林，我们按根节点大小排序后依次遍历
    roots.sort()

    def dfs(u):
        # 获取当前节点的子节点
        children_list = adj.get(u, [])
        
        # 核心规则：将父节点和所有子节点的值放在一起排序
        items = [u] + children_list
        items.sort()
        
        # 按照排序后的顺序进行遍历
        for item in items:
            if item == u:
                # 如果当前值是父节点，输出它
                print(item)
            else:
                # 如果当前值是子节点，递归进入该子节点
                dfs(item)

    # 从根节点开始执行
    for r in roots:
        dfs(r)

if __name__ == "__main__":
    solve()
```

