"""3720 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 3720
SAMPLE_IN = '2\nA\n-B\n--*\n--C\n-D\n--E\n---*\n---F\n0\nA\n-B\n-C\n0\n'
SAMPLE_OUT = 'ABCDEF\nCBFEDA\nBCAEFD\n\nABC\nBCA\nBAC\n'
REFERENCE_SOURCE = 'class Node:\n    def __init__(self, x, depth):\n        self.x = x\n        self.depth = depth\n        self.lchild = None\n        self.rchild = None\n\n    def preorder_traversal(self):\n        nodes = [self.x]\n        if self.lchild and self.lchild.x != \'*\':\n            nodes += self.lchild.preorder_traversal()\n        if self.rchild and self.rchild.x != \'*\':\n            nodes += self.rchild.preorder_traversal()\n        return nodes\n\n    def inorder_traversal(self):\n        nodes = []\n        if self.lchild and self.lchild.x != \'*\':\n            nodes += self.lchild.inorder_traversal()\n        nodes.append(self.x)\n        if self.rchild and self.rchild.x != \'*\':\n            nodes += self.rchild.inorder_traversal()\n        return nodes\n\n    def postorder_traversal(self):\n        nodes = []\n        if self.lchild and self.lchild.x != \'*\':\n            nodes += self.lchild.postorder_traversal()\n        if self.rchild and self.rchild.x != \'*\':\n            nodes += self.rchild.postorder_traversal()\n        nodes.append(self.x)\n        return nodes\n\n\ndef build_tree():\n    n = int(input())\n    for _ in range(n):\n        tree = []\n        stack = []\n        while True:\n            s = input()\n            if s == \'0\':\n                break\n            depth = len(s) - 1\n            node = Node(s[-1], depth)\n            tree.append(node)\n\n            # Finding the parent for the current node\n            while stack and tree[stack[-1]].depth >= depth:\n                stack.pop()\n            if stack:  # There is a parent\n                parent = tree[stack[-1]]\n                if not parent.lchild:\n                    parent.lchild = node\n                else:\n                    parent.rchild = node\n            stack.append(len(tree) - 1)\n\n        # Now tree[0] is the root of the tree\n        yield tree[0]\n\n\n# Read each tree and perform traversals\nfor root in build_tree():\n    print("".join(root.preorder_traversal()))\n    print("".join(root.postorder_traversal()))\n    print("".join(root.inorder_traversal()))\n    print()\n\n'

def g3720(r):
    def make_tree(labels):
        # 题面是二叉树:每个节点最多两个子节点
        children = {label: [] for label in labels}
        for label in labels[1:]:
            parents = [p for p in labels[:labels.index(label)] if len(children[p]) < 2]
            children[r.choice(parents)].append(label)
        return children

    def serialize(node, children, depth, lines):
        lines.append("-" * depth + node)
        kids = children[node]
        if len(kids) == 1:
            lines.append("-" * (depth + 1) + "*")
        for child in kids:
            serialize(child, children, depth + 1, lines)

    tree_count = r.randint(1, 3)
    lines = [str(tree_count)]
    next_label = 0
    for _ in range(tree_count):
        size = r.randint(2, 12)
        labels = [chr(ord("A") + (next_label + i) % 26) for i in range(size)]
        next_label += size
        children = make_tree(labels)
        tree_lines = []
        serialize(labels[0], children, 0, tree_lines)
        lines.extend(tree_lines)
        lines.append("0")
    return "\n".join(lines) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g3720(random.Random(NUMBER + i)) for i in range(1, 20)]

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
