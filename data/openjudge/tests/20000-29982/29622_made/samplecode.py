# External reference: statistics page /practice/29622/
# Accepted submission: 52829508
# Source: http://cs101.openjudge.cn/practice/solution/52829508/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 读取所有输入数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    
    edges = []
    idx = 2
    for _ in range(M):
        if idx + 2 >= len(input_data):
            break
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        w = int(input_data[idx+2])
        edges.append((w, u, v))
        idx += 3
        
    # 按成本 w 从小到大排序
    edges.sort()
    
    # 并查集初始化
    parent = list(range(N + 1))
    
    def find(i):
        # 路径压缩的查找操作
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False

    mst_weight = 0
    edges_count = 0
    
    # Kruskal 算法核心步骤
    for w, u, v in edges:
        # 排除自环
        if u == v:
            continue
        if union(u, v):
            mst_weight += w
            edges_count += 1
            if edges_count == N - 1:
                break
                
    # 判断是否成功构建了包含 N-1 条边的生成树
    if edges_count == N - 1:
        print(mst_weight)
    else:
        print("orz")

if __name__ == '__main__':
    solve()