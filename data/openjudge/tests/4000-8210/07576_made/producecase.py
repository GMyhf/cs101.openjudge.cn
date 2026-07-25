"""7576 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 7576
SAMPLE_IN = '8 1\n10 9 20 6 16 12 90 17\n3 15\n'
SAMPLE_OUT = '6 12 9 17 10 20 16 90\n9 12 15 17 10 20 16 90\n'
REFERENCE_SOURCE = 'import sys\nfrom collections import deque\n\nclass Node:\n    # 使用 __slots__ 减少内存占用，加快属性访问\n    __slots__ = [\'val\', \'win\', \'left\', \'right\', \'parent\']\n    def __init__(self, v=0):\n        self.val = v      # 内部节点存储：败者 (Loser)\n        self.win = v      # 内部节点存储：该场胜者 (Winner)，用于向上传递\n        self.left = None\n        self.right = None\n        self.parent = None\n\ndef solve():\n    # 快速读取所有输入\n    input_data = sys.stdin.read().split()\n    if not input_data: return\n    n, m = int(input_data[0]), int(input_data[1])\n    vals = [int(x) for x in input_data[2:2+n]]\n    \n    # 1. 初始构建树：O(n)\n    # 将初始值包装为叶子节点\n    leaves = [Node(v) for v in vals]\n    queue = deque(leaves)\n    \n    # 两两分组模拟比赛，构建完全二叉树\n    while len(queue) > 1:\n        l = queue.popleft()\n        r = queue.popleft()\n        # 创建比赛节点：val存大值(败者)，win存小值(胜者)\n        match = Node()\n        match.val, match.win = max(l.win, r.win), min(l.win, r.win)\n        match.left, match.right = l, r\n        l.parent = r.parent = match\n        queue.append(match)\n    \n    # 创建顶层冠军节点 (只有一个左孩子)\n    battle_root = queue.popleft()\n    root = Node(battle_root.win)\n    root.left, battle_root.parent = battle_root, root\n\n    # 2. 预处理：确定内部节点的输出顺序\n    # 题目要求输出内部节点（从上到下，从左到右），且结构不变\n    internal_nodes = []\n    bfs_q = deque([root])\n    while bfs_q and len(internal_nodes) < n:\n        curr = bfs_q.popleft()\n        internal_nodes.append(curr)\n        if curr.left: bfs_q.append(curr.left)\n        if curr.right: bfs_q.append(curr.right)\n\n    # 辅助函数：按序输出当前树的所有内部节点值\n    def print_internal_nodes():\n        sys.stdout.write(" ".join(str(node.val) for node in internal_nodes) + "\\n")\n\n    # 输出初始状态\n    print_internal_nodes()\n\n    # 3. 处理修改：每次 O(log n + n)\n    ptr = 2 + n\n    for _ in range(m):\n        idx, new_val = int(input_data[ptr]), int(input_data[ptr+1])\n        ptr += 2\n        \n        # 向上更新路径\n        curr_leaf = leaves[idx]\n        curr_leaf.win = new_val\n        p = curr_leaf.parent\n        while p:\n            if p.right: # 普通比赛节点：有两个孩子\n                p.val = max(p.left.win, p.right.win)\n                p.win = min(p.left.win, p.right.win)\n            else:       # 顶层冠军节点：只有一个孩子\n                p.val = p.win = p.left.win\n            p = p.parent\n        \n        print_internal_nodes()\n\nif __name__ == "__main__":\n    solve()\n'

def g7576(r):
    n = r.randint(2, 30); m = r.randint(1, 8); values = [r.randint(1, 1000) for _ in range(n)]
    changes = [f"{r.randrange(n)} {r.randint(1, 1000)}" for _ in range(m)]
    return f"{n} {m}\n" + " ".join(map(str, values)) + "\n" + "\n".join(changes) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g7576(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
