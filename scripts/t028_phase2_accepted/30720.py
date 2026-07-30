# External reference: http://cs101.openjudge.cn/practice/30720/statistics/
# Accepted submission: 52740206
# Source: http://cs101.openjudge.cn/practice/solution/52740206/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque


class TreeNode:
    # 使用 __slots__ 优化内存
    __slots__ = ['value', 'min_win', 'left', 'right', 'parent']

    # 构造函数支持四个参数及默认值
    def __init__(self, value=0, min_win=0, left=None, right=None):
        self.value = value
        self.min_win = min_win
        self.left = left
        self.right = right
        self.parent = None  # parent 通常在节点关联后设置


def solve():
    # 1. 快速读取
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    it = iter(input_data)
    n = int(next(it))
    m = int(next(it))

    # 2. 构建初始树
    # 初始化叶子：value为0(无意义)，min_win存初始值
    leaves = [TreeNode(0, int(next(it))) for _ in range(n)]
    queue = deque(leaves)

    while len(queue) > 1:
        l = queue.popleft()
        r = queue.popleft()

        # 利用四个参数的构造函数直接创建比赛节点
        # value 存败者(max), min_win 存胜者(min)
        match_node = TreeNode(
            max(l.min_win, r.min_win),
            min(l.min_win, r.min_win),
            l,
            r
        )
        l.parent = r.parent = match_node
        queue.append(match_node)

    # 创建冠军节点 (唯一只有左孩子的内部节点)
    battle_root = queue.popleft()
    root = TreeNode(battle_root.min_win, battle_root.min_win, battle_root)
    battle_root.parent = root

    # 3. 预处理内部节点顺序
    # 核心：必须通过 if node.left 过滤掉可能出现在浅层级的叶子节点
    internal_nodes = []
    bfs_q = deque([root])
    while bfs_q and len(internal_nodes) < n:
        curr = bfs_q.popleft()
        if curr.left:  # 有孩子即为内部节点
            internal_nodes.append(curr)
            bfs_q.append(curr.left)
            if curr.right:  # 只有比赛节点有右孩子，冠军节点没有
                bfs_q.append(curr.right)

    def print_internal_nodes():
        sys.stdout.write(" ".join(str(node.value) for node in internal_nodes) + "\n")

    # 输出初始
    print_internal_nodes()

    # 4. 修改与增量更新 O(log n)
    for _ in range(m):
        try:
            idx = int(next(it))
            new_val = int(next(it))
        except StopIteration:
            break

        curr = leaves[idx]
        curr.min_win = new_val

        p = curr.parent
        while p:
            if p.right:  # 普通比赛节点更新
                p.value = max(p.left.min_win, p.right.min_win)
                p.min_win = min(p.left.min_win, p.right.min_win)
            else:  # 顶层冠军节点更新
                p.value = p.min_win = p.left.min_win
            p = p.parent

        print_internal_nodes()


if __name__ == "__main__":
    solve()
