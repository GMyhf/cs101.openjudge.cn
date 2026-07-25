# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import sys

# 增加递归深度限制，防止处理大规模 $N$ 时溢出
sys.setrecursionlimit(200000)

class SegmentTree:
    def __init__(self, n):
        self.n = n
        # tree[i] 存储对应区间的最大值
        self.tree = [0] * (4 * n)
        # lazy[i] 存储懒标记（增加的力）
        self.lazy = [0] * (4 * n)

    def _push_up(self, node):
        """向上更新，父节点的值等于子节点的最大值"""
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def _push_down(self, node):
        """向下传播懒标记"""
        if self.lazy[node] != 0:
            add_val = self.lazy[node]
            
            # 更新左子节点
            self.tree[2 * node] += add_val
            self.lazy[2 * node] += add_val
            
            # 更新右子节点
            self.tree[2 * node + 1] += add_val
            self.lazy[2 * node + 1] += add_val
            
            # 清除当前节点的标记
            self.lazy[node] = 0

    def update(self, node, start, end, l, r, v):
        """区间更新：将 [l, r] 范围内的值加上 v"""
        if l <= start and end <= r:
            self.tree[node] += v
            self.lazy[node] += v
            return
        
        mid = (start + end) // 2
        self._push_down(node)
        
        if l <= mid:
            self.update(2 * node, start, mid, l, r, v)
        if r > mid:
            self.update(2 * node + 1, mid + 1, end, l, r, v)
            
        self._push_up(node)

    def query(self, node, start, end, l, r):
        """区间查询：获取 [l, r] 范围内的最大值"""
        if l <= start and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        self._push_down(node)
        
        res = -float('inf')
        if l <= mid:
            res = max(res, self.query(2 * node, start, mid, l, r))
        if r > mid:
            res = max(res, self.query(2 * node + 1, mid + 1, end, l, r))
        return res

def solve():
    # 使用快速读取
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    Q = int(input_data[1])
    
    st = SegmentTree(N)
    
    idx = 2
    results = []
    
    for _ in range(Q):
        op = input_data[idx]
        if op == "Add":
            l = int(input_data[idx + 1])
            r = int(input_data[idx + 2])
            v = int(input_data[idx + 3])
            st.update(1, 1, N, l, r, v)
            idx += 4
        elif op == "Query":
            l = int(input_data[idx + 1])
            r = int(input_data[idx + 2])
            results.append(str(st.query(1, 1, N, l, r)))
            idx += 3
            
    # 一次性输出所有查询结果
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    solve()
