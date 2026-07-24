# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import sys
from collections import deque

class Node:
    # 使用 __slots__ 减少内存占用，加快属性访问
    __slots__ = ['val', 'win', 'left', 'right', 'parent']
    def __init__(self, v=0):
        self.val = v      # 内部节点存储：败者 (Loser)
        self.win = v      # 内部节点存储：该场胜者 (Winner)，用于向上传递
        self.left = None
        self.right = None
        self.parent = None

def solve():
    # 快速读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data: return
    n, m = int(input_data[0]), int(input_data[1])
    vals = [int(x) for x in input_data[2:2+n]]
    
    # 1. 初始构建树：O(n)
    # 将初始值包装为叶子节点
    leaves = [Node(v) for v in vals]
    queue = deque(leaves)
    
    # 两两分组模拟比赛，构建完全二叉树
    while len(queue) > 1:
        l = queue.popleft()
        r = queue.popleft()
        # 创建比赛节点：val存大值(败者)，win存小值(胜者)
        match = Node()
        match.val, match.win = max(l.win, r.win), min(l.win, r.win)
        match.left, match.right = l, r
        l.parent = r.parent = match
        queue.append(match)
    
    # 创建顶层冠军节点 (只有一个左孩子)
    battle_root = queue.popleft()
    root = Node(battle_root.win)
    root.left, battle_root.parent = battle_root, root

    # 2. 预处理：确定内部节点的输出顺序
    # 题目要求输出内部节点（从上到下，从左到右），且结构不变
    internal_nodes = []
    bfs_q = deque([root])
    while bfs_q and len(internal_nodes) < n:
        curr = bfs_q.popleft()
        internal_nodes.append(curr)
        if curr.left: bfs_q.append(curr.left)
        if curr.right: bfs_q.append(curr.right)

    # 辅助函数：按序输出当前树的所有内部节点值
    def print_internal_nodes():
        sys.stdout.write(" ".join(str(node.val) for node in internal_nodes) + "\n")

    # 输出初始状态
    print_internal_nodes()

    # 3. 处理修改：每次 O(log n + n)
    ptr = 2 + n
    for _ in range(m):
        idx, new_val = int(input_data[ptr]), int(input_data[ptr+1])
        ptr += 2
        
        # 向上更新路径
        curr_leaf = leaves[idx]
        curr_leaf.win = new_val
        p = curr_leaf.parent
        while p:
            if p.right: # 普通比赛节点：有两个孩子
                p.val = max(p.left.win, p.right.win)
                p.win = min(p.left.win, p.right.win)
            else:       # 顶层冠军节点：只有一个孩子
                p.val = p.win = p.left.win
            p = p.parent
        
        print_internal_nodes()

if __name__ == "__main__":
    solve()
