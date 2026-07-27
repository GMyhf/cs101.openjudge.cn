# External reference: statistics page /practice/28327/
# Accepted submission: 52825181
# Source: http://cs101.openjudge.cn/practice/solution/52825181/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 快速读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    adj = [[] for _ in range(N + 1)]
    idx = 1
    for _ in range(N - 1):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        adj[u].append(v)
        adj[v].append(u)
        idx += 2
        
    Q = int(input_data[idx])
    idx += 1
    
    # 预处理倍增数组
    # 2^11 = 2048 > 2000，因此最大倍增步数设为 12 足够
    K = 12  
    depth = [0] * (N + 1)
    up = [[0] * K for _ in range(N + 1)]
    
    # 使用 BFS 初始化深度和直接父节点，避免递归栈溢出
    queue = [1]
    depth[1] = 1
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        for v in adj[u]:
            if depth[v] == 0:
                depth[v] = depth[u] + 1
                up[v][0] = u
                queue.append(v)
                
    # 填充倍增表
    for j in range(1, K):
        for i in range(1, N + 1):
            parent = up[i][j-1]
            up[i][j] = up[parent][j-1] if parent != 0 else 0

    # 查询 LCA
    def get_lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        for j in range(K):
            if (diff >> j) & 1:
                u = up[u][j]
        if u == v:
            return u
        for j in range(K - 1, -1, -1):
            if up[u][j] != up[v][j]:
                u = up[u][j]
                v = up[v][j]
        return up[u][0]

    # 查询节点的第 k 个祖先
    def get_kth_ancestor(node, k):
        for j in range(K):
            if (k >> j) & 1:
                node = up[node][j]
                if node == 0:
                    break
        return node

    out = []
    for _ in range(Q):
        c = int(input_data[idx])
        d = int(input_data[idx+1])
        idx += 2
        
        g = get_lca(c, d)
        dist_c_g = depth[c] - depth[g]
        dist_d_g = depth[d] - depth[g]
        total_dist = dist_c_g + dist_d_g
        
        if total_dist % 2 == 0:
            # 偶数长度，相遇于城市
            steps = total_dist // 2
            if steps <= dist_c_g:
                ans = get_kth_ancestor(c, steps)
            else:
                ans = get_kth_ancestor(d, total_dist - steps)
            out.append(f"City {ans}")
        else:
            # 奇数长度，相遇于道路
            steps1 = total_dist // 2
            steps2 = steps1 + 1
            
            if steps1 <= dist_c_g:
                u = get_kth_ancestor(c, steps1)
            else:
                u = get_kth_ancestor(d, total_dist - steps1)
                
            if steps2 <= dist_c_g:
                v = get_kth_ancestor(c, steps2)
            else:
                v = get_kth_ancestor(d, total_dist - steps2)
                
            # 道路输出要求节点编号升序
            if u > v:
                u, v = v, u
            out.append(f"Road {u} {v}")
            
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    solve()