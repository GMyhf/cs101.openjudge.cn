# External reference: http://cs101.openjudge.cn/practice/30921/statistics/
# Accepted submission: 52721420
# Source: http://cs101.openjudge.cn/practice/solution/52721420/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 使用 sys.stdin.read 一次性读入所有数据，极大提升 Python 的 I/O 效率
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    q = int(next(iterator))
    s = int(next(iterator))

    # parent[i] 直接存储节点 i 所在堆的根节点（无需路径压缩，因为我们通过启发式合并保证了高度）
    parent = list(range(n + 1))

    # elements[i] 存储以 i 为根的堆中包含的所有积木编号
    elements = [[i] for i in range(n + 1)]
    elements[0] = []

    total_piles = n
    out = []

    # 本地化变量引用，加速 Python 的循环内查表速度
    parent_ref = parent
    elements_ref = elements

    for _ in range(q):
        x = int(next(iterator))
        y = int(next(iterator))

        u = parent_ref[x]
        v = parent_ref[y]

        if u != v:
            size_u = len(elements_ref[u])
            size_v = len(elements_ref[v])

            # 判断合并后是否会崩塌
            if size_u + size_v < s:
                # 启发式合并：保证 u 是较大的堆，v 是较小的堆
                if size_u < size_v:
                    u, v = v, u
                    size_u, size_v = size_v, size_u

                # 将较小堆 v 中的所有积木并入较大堆 u
                elements_v = elements_ref[v]
                for val in elements_v:
                    parent_ref[val] = u

                elements_ref[u].extend(elements_v)
                elements_ref[v] = [] # 释放内存
                total_piles -= 1
            else:
                # 触发崩塌：重置 u 和 v 堆中的所有积木为单人堆
                elements_u = elements_ref[u]
                elements_v = elements_ref[v]

                for val in elements_u:
                    parent_ref[val] = val
                    elements_ref[val] = [val]
                for val in elements_v:
                    parent_ref[val] = val
                    elements_ref[val] = [val]

                # 堆数变化：减少了 2 堆，增加了 size_u + size_v 堆
                total_piles += size_u + size_v - 2

        out.append(str(total_piles))

    # 批量输出结果
    print('\n'.join(out))

if __name__ == '__main__':
    solve()
