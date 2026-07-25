"""7161 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 7161
SAMPLE_IN = '2\nC 3 E 3 F 0 G 0 K 0 H 0 J 0\nD 2 X 0 I 0\n'
SAMPLE_OUT = 'K H J E F G C X I D\n'
REFERENCE_SOURCE = 'from collections import deque\n\nn = int(input())\nans = []\n\nclass TreeNode:\n    def __init__(self, x):\n        self.val = x\n        self.first_child = None\n        self.next_sibling = None\n    def __str__(self):\n        return str(self.val)\n\ndef postorder(x):\n    global ans\n    if x is None:\n        return\n    y = x.first_child\n    while y:\n        postorder(y)\n        y = y.next_sibling\n    ans.append(x.val)\n\ndef inorder(x):\n    global ans\n    if x:\n        inorder(x.first_child)\n        ans.append(x.val)\n        inorder(x.next_sibling)\n\n\nfor _ in range(n):\n    s = input().split()\n    root = TreeNode(s[0])\n    q = deque([[root, int(s[1])]])\n    i = 2\n    while q:\n        front = q.popleft()\n        cur = front[0]\n        for j in range(front[1]):\n            if j == 0:\n                cur.first_child = TreeNode(s[i])\n                cur = cur.first_child\n            else:\n                cur.next_sibling = TreeNode(s[i])\n                cur = cur.next_sibling\n            q.append((cur, int(s[i+1])))\n            i += 2\n    #postorder(root)\n    inorder(root)   #二叉树的中序遍历 = 原多叉树的后序遍历\nprint(*ans)\n'

def g7161(r):
    count = r.randint(1, 3); used = 0; lines = [str(count)]
    for tree in range(count):
        size = r.randint(2, min(8, 26 - used)); labels = [chr(65 + used + i) for i in range(size)]; used += size
        children = [[] for _ in range(size)]
        for i in range(1, size): children[r.randrange(i)].append(i)
        queue = [0]; encoded = []
        while queue:
            node = queue.pop(0); kids = children[node]
            encoded += [labels[node], str(len(kids))]
            queue.extend(kids)
        lines.append(" ".join(encoded))
    return "\n".join(lines) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g7161(random.Random(NUMBER + i + attempt * 1000))
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
