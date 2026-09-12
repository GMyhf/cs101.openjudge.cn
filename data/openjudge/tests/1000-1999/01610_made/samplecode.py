# External reference: http://cs101.openjudge.cn/practice/01610/statistics/
# Accepted submission: 44188104
# Source: http://cs101.openjudge.cn/practice/solution/44188104/
# License: not declared on the submission page; no license is inferred.
#
# 算法部分（TreeNode / build / get / int(ans, 2) → hex）逐字取自上面那份平台
# Accepted 提交。**只有读输入这一段是仓库改写的**，原提交用的是
#     matrix = [list(map(int, input().split())) for _ in range(n)]
# 2026-09-12 之前，生成器把矩阵写成了无分隔的 `10010111`（题面明写「每两个 0 和 1
# 之间至少有一个空格」），这个读法于是把一整行读成单个整数 10010111，21 组 `.out`
# 全是乱码 —— 而参考实现重跑照样复现同一份乱码，闸门全绿。数据已按题面补上空格；
# 读法也改成按 token 流读、多字符 token 逐字符展开，两种写法都能读，
# 免得同一个坑再踩一次。详见 CHANGELOG。

import sys


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []

def build(n, matrix):
    check = sum(sum(row) for row in matrix)
    if check == 0:
        return TreeNode('00')
    elif check == n**2:
        return TreeNode('01')
    else:
        a = [matrix[i][:n//2] for i in range(n//2)]
        b = [matrix[i][n//2:] for i in range(n//2)]
        c = [matrix[i][:n//2] for i in range(n//2, n)]
        d = [matrix[i][n//2:] for i in range(n//2, n)]
        root = TreeNode('1')
        for p in [a, b, c, d]:
            root.children.append(build(n//2, p))
        return root

def get(root):
    result = ''
    queue = [root]
    while queue:
        node = queue.pop(0)
        result += node.val
        queue += node.children
    return result

def read_row(tokens, n):
    """读一行 n 个格子：`0 1 0 1` 与 `0101` 都接受。"""
    cells = []
    while len(cells) < n:
        cells.extend(int(character) for character in next(tokens))
    if len(cells) != n:
        raise ValueError(f"row has {len(cells)} cells, expected {n}")
    return cells

def main():
    tokens = iter(sys.stdin.read().split())
    sys.setrecursionlimit(10000)
    out = []
    for _ in range(int(next(tokens))):
        n = int(next(tokens))
        matrix = [read_row(tokens, n) for _ in range(n)]
        ans = get(build(n, matrix))
        p = int(ans, 2)
        out.append(hex(p)[2:].upper())
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
