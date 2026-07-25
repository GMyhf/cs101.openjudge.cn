# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import sys


def solve():
    # 使用 sys.stdin.read 快速读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    k = int(input_data[0])
    n = int(input_data[1])

    num_nodes = 1 << k
    sz = [0] * num_nodes

    # 预计算每个节点的子树大小
    for i in range(1, num_nodes):
        depth = i.bit_length()  # i 的二进制长度即为其所在的深度
        h = k - depth + 1
        sz[i] = (1 << h) - 1

    sum_tree = [0] * num_nodes
    lazy = [0] * num_nodes

    idx = 2
    out = []

    for _ in range(n):
        op = int(input_data[idx])
        if op == 1:
            x = int(input_data[idx + 1])
            y = int(input_data[idx + 2])
            idx += 3

            # 1. 更新操作
            lazy[x] += y
            add_val = sz[x] * y
            p = x
            # 向上更新所有祖先节点的 subtree sum
            while p > 0:
                sum_tree[p] += add_val
                p >>= 1
        else:
            x = int(input_data[idx + 1])
            idx += 2

            # 2. 查询操作
            lazy_sum = 0
            p = x >> 1
            # 向上累加所有严格祖先节点的 lazy 标记
            while p > 0:
                lazy_sum += lazy[p]
                p >>= 1
            res = sum_tree[x] + sz[x] * lazy_sum
            out.append(str(res))

    # 批量输出结果
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    solve()
