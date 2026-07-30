# External reference: http://cs101.openjudge.cn/practice/30889/statistics/
# Accepted submission: 52723166
# Source: http://cs101.openjudge.cn/practice/solution/52723166/
# License: not declared on the submission page; no license is inferred.

import sys
from sys import stdin
sys.setrecursionlimit(1 << 25)

def main():
    input = stdin.read().split()
    ptr = 0
    n = int(input[ptr])
    ptr += 1

    # 建树：每个节点保存左孩子、右孩子
    left = [0] * (n + 1)
    right = [0] * (n + 1)

    for i in range(1, n + 1):
        if i == 1:
            # 根节点固定 - -
            ptr += 2
            continue
        p = int(input[ptr])
        d = input[ptr + 1]
        ptr += 2
        if d == 'L':
            left[p] = i
        else:
            right[p] = i

    # 后序遍历递归计算寄存器数
    def dfs(u):
        l = left[u]
        r = right[u]
        # 叶子节点：无孩子
        if l == 0 and r == 0:
            return 1
        # 只有左孩子（一元操作）
        if r == 0:
            return dfs(l)
        # 只有右孩子（一元操作）
        if l == 0:
            return dfs(r)
        # 左右孩子都有（二元操作）
        a = dfs(l)
        b = dfs(r)
        if a == b:
            return a + 1
        else:
            return max(a, b)

    print(dfs(1))

if __name__ == "__main__":
    main()
