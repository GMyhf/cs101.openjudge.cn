请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 力场叠加模拟 (在线版)

### 描述

在一个物理仿真系统中，一排 $N$ 个静止的粒子（索引从 1 到 $N$）初始受力均为 0。系统需要实时处理 $Q$ 次物理力场事件，并反馈指定区域的受力情况。

为了检验算法的实时性，本题**强制在线**。你需要维护一个变量 `lastans`（表示上一次 `Query` 操作输出的答案，初始时 `lastans = 0`）。

对于每一次操作，输入会给出解密前的区间端点 $l_{\text{raw}}$ 和 $r_{\text{raw}}$。真实的区间 $[l, r]$ 需要通过以下规则进行解密：

$$l = (l_{\text{raw}} \oplus |lastans|) \bmod N + 1$$
$$r = (r_{\text{raw}} \oplus |lastans|) \bmod N + 1$$

（其中 $\oplus$ 为异或运算，$|lastans|$ 为上一次查询答案的绝对值）。
如果计算出的 $l > r$，则需要交换 $l$ 和 $r$。

你需要实现以下两种操作：

1. `Add l_raw r_raw v`：解密后在区间 $[l, r]$ 内的每个粒子上叠加一个大小为 $v$ 的恒定力（$v$ 可正可负）。
2. `Query l_raw r_raw`：解密后查询当前区间 $[l, r]$ 内所有粒子受力的**最大值**。

### 输入

第一行包含两个整数 $N$ 和 $Q$。
接下来 $Q$ 行，每行描述一个操作：

* `Add l_raw r_raw v`：表示将解密后的区间 $[l, r]$ 增加力 $v$。
* `Query l_raw r_raw`：表示查询解密后的区间 $[l, r]$ 的受力最大值。

### 数据范围

* $1 \le N \le 10^9$
* $1 \le Q \le 10^5$
* $-10^9 \le v \le 10^9$
* $0 \le l_{\text{raw}}, r_{\text{raw}} < 2^{31}$

### 输出

对于每一个 `Query` 操作，输出一个整数，表示该区间的最大受力值。

### 样例输入

```text
5 4
Add 0 2 10
Query 11 13
Add 8 14 5
Query 11 9
```

### 样例输出

```text
10
15
```

### 



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

# 提升递归深度限制以应对深度可达 30 层的线段树
sys.setrecursionlimit(200000)

class DynamicSegmentTree:
    def __init__(self):
        # 0 号索引作为空节点存根，1 号索引为线段树的根节点
        # 使用扁平数组减少 Python 对象开销
        self.max_val = [0, 0]
        self.lazy = [0, 0]
        self.left_child = [0, 0]
        self.right_child = [0, 0]
        self.node_cnt = 1

    def _get_new_node(self):
        self.node_cnt += 1
        self.max_val.append(0)
        self.lazy.append(0)
        self.left_child.append(0)
        self.right_child.append(0)
        return self.node_cnt

    def _push_down(self, curr):
        if self.lazy[curr] == 0:
            return
        
        lazy_val = self.lazy[curr]
        
        # 延迟下传时若子节点不存在，则动态开点
        if self.left_child[curr] == 0:
            self.left_child[curr] = self._get_new_node()
        lc = self.left_child[curr]
        self.max_val[lc] += lazy_val
        self.lazy[lc] += lazy_val
        
        if self.right_child[curr] == 0:
            self.right_child[curr] = self._get_new_node()
        rc = self.right_child[curr]
        self.max_val[rc] += lazy_val
        self.lazy[rc] += lazy_val
        
        self.lazy[curr] = 0

    def update(self, curr, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self.max_val[curr] += val
            self.lazy[curr] += val
            return
        
        self._push_down(curr)
        mid = l + (r - l) // 2
        
        if ql <= mid:
            if self.left_child[curr] == 0:
                self.left_child[curr] = self._get_new_node()
            self.update(self.left_child[curr], l, mid, ql, qr, val)
        if qr > mid:
            if self.right_child[curr] == 0:
                self.right_child[curr] = self._get_new_node()
            self.update(self.right_child[curr], mid + 1, r, ql, qr, val)
        
        # 向上更新最大值
        lc = self.left_child[curr]
        rc = self.right_child[curr]
        lv = self.max_val[lc] if lc else 0
        rv = self.max_val[rc] if rc else 0
        self.tree_max_update(curr, lv, rv)

    def tree_max_update(self, curr, lv, rv):
        self.max_val[curr] = max(lv, rv)

    def query(self, curr, l, r, ql, qr):
        if curr == 0:
            return 0
        if ql <= l and r <= qr:
            return self.max_val[curr]
        
        self._push_down(curr)
        mid = l + (r - l) // 2
        
        ans = -float('inf')
        has_overlap = False
        
        if ql <= mid:
            ans = max(ans, self.query(self.left_child[curr], l, mid, ql, qr))
            has_overlap = True
        if qr > mid:
            ans = max(ans, self.query(self.right_child[curr], mid + 1, r, ql, qr))
            has_overlap = True
            
        return ans if has_overlap else 0

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    Q = int(input_data[1])
    
    st = DynamicSegmentTree()
    root = 1
    lastans = 0
    
    idx = 2
    results = []
    
    for _ in range(Q):
        op = input_data[idx]
        if op == "Add":
            l_raw = int(input_data[idx + 1])
            r_raw = int(input_data[idx + 2])
            v = int(input_data[idx + 3])
            
            # 在线解密
            l = (l_raw ^ abs(lastans)) % N + 1
            r = (r_raw ^ abs(lastans)) % N + 1
            if l > r:
                l, r = r, l
                
            st.update(root, 1, N, l, r, v)
            idx += 4
        elif op == "Query":
            l_raw = int(input_data[idx + 1])
            r_raw = int(input_data[idx + 2])
            
            # 在线解密
            l = (l_raw ^ abs(lastans)) % N + 1
            r = (r_raw ^ abs(lastans)) % N + 1
            if l > r:
                l, r = r, l
                
            lastans = st.query(root, 1, N, l, r)
            results.append(str(lastans))
            idx += 3
            
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    solve()
```

