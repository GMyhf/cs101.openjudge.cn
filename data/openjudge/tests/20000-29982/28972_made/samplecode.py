# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys
from operator import itemgetter

def solve():
    # 使用生成器逐个读取输入，节省内存
    def get_tokens():
        for line in sys.stdin:
            for word in line.split():
                yield word
    
    tokens = get_tokens()
    
    try:
        n = int(next(tokens))
        m = int(next(tokens))
    except (StopIteration, ValueError):
        return
    
    size = n * m
    # 特判：如果只有一个区块，海拔差最大值为0
    if size <= 1:
        if size == 1:
            print(0)
        return

    # 读取所有海拔高度，存储在扁平化的1D列表中
    h = [0] * size
    for i in range(size):
        h[i] = int(next(tokens))
    
    # 构造所有的边 (权重, 点u, 点v)
    edges = []
    for r in range(n):
        offset = r * m
        for c in range(m):
            u = offset + c
            # 添加向右的边
            if c + 1 < m:
                v = u + 1
                diff = h[u] - h[v]
                edges.append((diff if diff >= 0 else -diff, u, v))
            # 添加向下的边
            if r + 1 < n:
                v = u + m
                diff = h[u] - h[v]
                edges.append((diff if diff >= 0 else -diff, u, v))
    
    # 释放海拔列表以节省内存
    h = None
    
    # 按权重从小到大排序
    edges.sort(key=itemgetter(0))
    
    # 并查集初始化
    parent = list(range(size))
    
    # 路径压缩的并查集查找函数
    def find(i):
        root = i
        while parent[root] != root:
            root = parent[root]
        curr = i
        while parent[curr] != root:
            # 路径压缩：直接指向根节点
            parent[curr], curr = root, parent[curr]
        return root

    start_node = 0
    end_node = size - 1
    
    # 依次加入边，直到起点和终点连通
    for diff, u, v in edges:
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            parent[root_u] = root_v
            # 检查起点(0,0)和终点(n-1,m-1)是否连通
            if find(start_node) == find(end_node):
                print(diff)
                return

if __name__ == "__main__":
    solve()
