# External reference: http://cs101.openjudge.cn/practice/30178/statistics/
# Accepted submission: 52726449
# Source: http://cs101.openjudge.cn/practice/solution/52726449/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 使用快速读取
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    matrix = list(map(int, input_data[1:]))

    zero_row = 0
    sequence = []

    # 找到 0 的位置并提取非零序列
    for i in range(len(matrix)):
        val = matrix[i]
        if val == 0:
            zero_row = i // n
        else:
            sequence.append(val)

    # 计算逆序对奇偶性 (使用 O(N) 的环分解算法)
    # 逆序对奇偶性 = (元素个数 - 环的个数) % 2
    l = len(sequence)
    visited = [False] * l
    cycles = 0

    # 建立数值到索引的映射（如果数值不是 1~N-1，则需要离散化，这里题目说是 1 到 n^2-1）
    # 由于数值是 1 到 n^2-1，我们可以直接计算
    for i in range(l):
        if not visited[i]:
            cycles += 1
            curr = i
            while not visited[curr]:
                visited[curr] = True
                # sequence[curr] 是 1 到 n^2-1，映射回索引要减 1
                curr = sequence[curr] - 1

    inv_parity = (l - cycles) % 2

    # 判断逻辑
    if n % 2 != 0:
        # n 为奇数：逆序对必须为偶数
        if inv_parity == 0:
            print("yes")
        else:
            print("no")
    else:
        # n 为偶数：(逆序对 + 空格行号) 的奇偶性必须与 (0 + n-1) 一致
        if (inv_parity + zero_row) % 2 == (n - 1) % 2:
            print("yes")
        else:
            print("no")

if __name__ == "__main__":
    solve()
