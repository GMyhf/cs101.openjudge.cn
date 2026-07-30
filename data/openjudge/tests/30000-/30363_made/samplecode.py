# External reference: http://cs101.openjudge.cn/practice/30363/statistics/
# Accepted submission: 52789476
# Source: http://cs101.openjudge.cn/practice/solution/52789476/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 优化输入读取，适合处理大数据量
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    Q = int(input_data[1])

    # 初始化并查集
    # parent[i] 表示节点 i 的父节点
    # size[i] 表示以 i 为根节点的连通分量的大小
    parent = list(range(N + 1))
    size = [1] * (N + 1)

    # 查找函数（带路径压缩）
    def find(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i

    # 合并函数
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            # 按大小合并，将小树合并到大树上
            if size[root_i] < size[root_j]:
                root_i, root_j = root_j, root_i
            parent[root_j] = root_i
            old_size_i = size[root_i]
            old_size_j = size[root_j]
            size[root_i] += size[root_j]
            return True, old_size_i, old_size_j
        return False, 0, 0

    current_ans = 0
    results = []

    idx = 2
    for _ in range(Q):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        idx += 2

        merged, sz_u, sz_v = union(u, v)
        if merged:
            # 减去原先两个连通分量的贡献
            current_ans -= sz_u * (sz_u - 1) // 2
            current_ans -= sz_v * (sz_v - 1) // 2
            # 加上合并后新连通分量的贡献
            new_sz = sz_u + sz_v
            current_ans += new_sz * (new_sz - 1) // 2

        results.append(str(current_ans))

    # 输出每一次操作后的结果
    print('\n'.join(results))

if __name__ == '__main__':
    solve()
