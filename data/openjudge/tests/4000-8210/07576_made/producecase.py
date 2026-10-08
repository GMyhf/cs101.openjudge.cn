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

def valid(text):
    """题面契约：首行 n m；第二行 n 个整数；随后 m 行，每行“标号 新值”两个整数，标号从 0 起、落在数组内
    （样例 3 15 改的是第 4 个元素）。题面未给 n、m 与取值范围，只核格式与标号合法。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    def ints(line, cnt):
        t = line.split(' ')
        if len(t) != cnt:
            return None
        try:
            v = [int(x) for x in t]
        except ValueError:
            return None
        return v if all(str(x) == y for x, y in zip(v, t)) else None
    h = ints(lines[0], 2)
    if h is None or h[0] < 1 or h[1] < 0:
        return False
    n, m = h
    if len(lines) != 2 + m or ints(lines[1], n) is None:
        return False
    for line in lines[2:]:
        v = ints(line, 2)
        if v is None or not 0 <= v[0] < n:
            return False
    return True


def g7576(r, i=0):
    # 只用 2 的幂作 n：题面“相邻两两比较”在 n 非 2 的幂时树形不唯一（见 notes），2 的幂时各种建法一致
    if i <= 6:
        n = [2, 4, 2, 8, 4, 16, 8][i]; m = r.randint(1, 8); lo, hi = 1, 1000
    elif i <= 10:
        n = r.choice([16, 32, 64]); m = r.randint(5, 30); lo, hi = 1, 5   # 大量相等值
    elif i <= 15:
        n = r.choice([64, 128, 256]); m = r.randint(20, 100); lo, hi = -10**6, 10**6
    else:
        n = 1024; m = 200; lo, hi = 1, 10**6
    values = [r.randint(lo, hi) for _ in range(n)]
    init = list(values)
    changes = []
    for _ in range(m):
        k = r.random()
        if k < 0.2:
            idx = values.index(min(values)); v = r.randint(lo, hi)        # 改掉当前冠军
        elif k < 0.3:
            idx = r.randrange(n); v = lo - r.randint(0, 3)              # 新冠军
        elif k < 0.35:
            idx = r.randrange(n); v = values[idx]                        # 改成原值
        else:
            idx = r.randrange(n); v = r.randint(lo, hi)
        values[idx] = v
        changes.append(f"{idx} {v}")
    return f"{n} {m}\n" + " ".join(map(str, init)) + "\n" + "\n".join(changes) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g7576(random.Random(NUMBER + i + attempt * 1000), i)
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
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
