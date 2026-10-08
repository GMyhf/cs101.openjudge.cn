"""3720 文本二叉树 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

出处：build_001a（scripts/build_001a.py 批次 001a）。

题面约束（valid() 逐条核）：第一行树的数目 n；接下来 n 棵树，每棵以单独一行 '0' 结尾；
每个节点是一个字母且互不相同，每棵树不超过 100 个节点；按题面 1)~5) 规则，
层次连续、'*' 只出现在「没有左子而有右子」时的左子位置。

2026-10 审计修正：原生成器只有一个孩子时一律写成「'*' + 右子」，从没出现过
「只有左子」（直接一行子节点、不写 '*'）的形态；每棵树 2~12 个节点，没有单节点树、
没有长链。现在显式随机左右子：覆盖只有左子 / 只有右子 / 左链 / 右链 / 之字形 /
完全二叉树、单节点树；节点数到 26（大写）和 52（大小写字母混用，题面只说「字母」），
一组里树的数目到 100。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

NUMBER = 3720
SAMPLE_IN = '2\nA\n-B\n--*\n--C\n-D\n--E\n---*\n---F\n0\nA\n-B\n-C\n0\n'
SAMPLE_OUT = 'ABCDEF\nCBFEDA\nBCAEFD\n\nABC\nBCA\nBAC\n'
REFERENCE_SOURCE = 'class Node:\n    def __init__(self, x, depth):\n        self.x = x\n        self.depth = depth\n        self.lchild = None\n        self.rchild = None\n\n    def preorder_traversal(self):\n        nodes = [self.x]\n        if self.lchild and self.lchild.x != \'*\':\n            nodes += self.lchild.preorder_traversal()\n        if self.rchild and self.rchild.x != \'*\':\n            nodes += self.rchild.preorder_traversal()\n        return nodes\n\n    def inorder_traversal(self):\n        nodes = []\n        if self.lchild and self.lchild.x != \'*\':\n            nodes += self.lchild.inorder_traversal()\n        nodes.append(self.x)\n        if self.rchild and self.rchild.x != \'*\':\n            nodes += self.rchild.inorder_traversal()\n        return nodes\n\n    def postorder_traversal(self):\n        nodes = []\n        if self.lchild and self.lchild.x != \'*\':\n            nodes += self.lchild.postorder_traversal()\n        if self.rchild and self.rchild.x != \'*\':\n            nodes += self.rchild.postorder_traversal()\n        nodes.append(self.x)\n        return nodes\n\n\ndef build_tree():\n    n = int(input())\n    for _ in range(n):\n        tree = []\n        stack = []\n        while True:\n            s = input()\n            if s == \'0\':\n                break\n            depth = len(s) - 1\n            node = Node(s[-1], depth)\n            tree.append(node)\n\n            # Finding the parent for the current node\n            while stack and tree[stack[-1]].depth >= depth:\n                stack.pop()\n            if stack:  # There is a parent\n                parent = tree[stack[-1]]\n                if not parent.lchild:\n                    parent.lchild = node\n                else:\n                    parent.rchild = node\n            stack.append(len(tree) - 1)\n\n        # Now tree[0] is the root of the tree\n        yield tree[0]\n\n\n# Read each tree and perform traversals\nfor root in build_tree():\n    print("".join(root.preorder_traversal()))\n    print("".join(root.postorder_traversal()))\n    print("".join(root.inorder_traversal()))\n    print()\n\n'

LETTERS_UPPER = [chr(ord("A") + i) for i in range(26)]
LETTERS_ALL = LETTERS_UPPER + [chr(ord("a") + i) for i in range(26)]
LINE_RE = re.compile(r"(-*)([A-Za-z*])")


def valid(text):
    """按题面 1)~5) 解析每棵树，核：字母互不相同、每棵 <=100 个节点、层次连续、
    '*' 只出现在「无左子有右子」的位置且无子节点、每个节点至多两个子节点。"""
    if not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    count = int(lines[0])
    p = 1
    for _ in range(count):
        items = []
        while True:
            if p >= len(lines):
                return False
            s = lines[p]
            p += 1
            if s == "0":
                break
            m = LINE_RE.fullmatch(s)
            if not m:
                return False
            items.append((len(m.group(1)), m.group(2)))
        if not items or items[0] != (0, items[0][1]) or items[0][1] == "*":
            return False
        letters = [c for _, c in items if c != "*"]
        if len(letters) != len(set(letters)) or len(letters) > 100:
            return False
        children = [[] for _ in items]
        stack = []
        prev = -1
        for idx, (depth, c) in enumerate(items):
            if idx and (depth < 1 or depth > prev + 1):
                return False
            while stack and items[stack[-1]][0] >= depth:
                stack.pop()
            if idx:
                parent = stack[-1]
                if items[parent][1] == "*":
                    return False
                children[parent].append(idx)
            stack.append(idx)
            prev = depth
        for idx, ch in enumerate(children):
            kinds = [items[k][1] == "*" for k in ch]
            if len(ch) > 2:
                return False
            if kinds and kinds[-1]:       # '*' 不能是最后一个子（右子或唯一子）
                return False
    return p == len(lines)


def make_shape(r, size, style):
    """返回 (left, right) 两个字典：节点编号 -> 子节点编号。"""
    left, right = {}, {}
    for v in range(1, size):
        if style == "left":
            left[v - 1] = v
        elif style == "right":
            right[v - 1] = v
        elif style == "zigzag":
            (left if r.random() < .5 else right)[v - 1] = v
        elif style == "complete":
            parent = (v - 1) // 2
            (left if v % 2 else right)[parent] = v
        else:
            while True:
                parent = r.randrange(v)
                side = left if r.random() < .5 else right
                if parent not in side:
                    side[parent] = v
                    break
    return left, right


def serialize(node, left, right, label, depth, lines):
    lines.append("-" * depth + label[node])
    if node in left:
        serialize(left[node], left, right, label, depth + 1, lines)
    elif node in right:
        lines.append("-" * (depth + 1) + "*")
    if node in right:
        serialize(right[node], left, right, label, depth + 1, lines)


def one_tree(r, size, style, mixed):
    pool = LETTERS_ALL if mixed else LETTERS_UPPER
    label = r.sample(pool, size)
    left, right = make_shape(r, size, style)
    lines = []
    serialize(0, left, right, label, 0, lines)
    return lines


def g3720(r, tree_count=None, sizes=None, styles=None, mixed=None):
    tree_count = tree_count or r.randint(1, 6)
    lines = [str(tree_count)]
    for t in range(tree_count):
        mix = r.random() < .2 if mixed is None else mixed
        size = sizes[t] if sizes else r.choice([1, 2, 3, r.randint(2, 12), r.randint(10, 26)])
        if size > 26:
            mix = True
        style = styles[t] if styles else r.choice(["random"] * 5 + ["left", "right", "zigzag", "complete"])
        lines.extend(one_tree(r, size, style, mix))
        lines.append("0")
    return "\n".join(lines) + "\n"


def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        cases.append(g3720(random.Random(NUMBER + i)))
    fixed = [
        dict(tree_count=1, sizes=[1], styles=["random"]),
        dict(tree_count=3, sizes=[1, 2, 2], styles=["random", "left", "right"]),
        dict(tree_count=1, sizes=[26], styles=["left"]),
        dict(tree_count=1, sizes=[26], styles=["right"]),
        dict(tree_count=1, sizes=[52], styles=["left"], mixed=True),
        dict(tree_count=1, sizes=[52], styles=["right"], mixed=True),
        dict(tree_count=1, sizes=[52], styles=["zigzag"], mixed=True),
        dict(tree_count=2, sizes=[52, 52], styles=["random", "complete"], mixed=True),
        dict(tree_count=4, sizes=[26, 26, 26, 26], styles=["zigzag", "random", "complete", "random"]),
        dict(tree_count=50),
        dict(tree_count=100),
    ]
    for k, kw in enumerate(fixed):
        cases.append(g3720(random.Random(NUMBER * 100 + k), **kw))
    k = 0
    while len(cases) < 40:
        k += 1
        c = g3720(random.Random(NUMBER * 1000 + k))
        if c not in cases:
            cases.append(c)
    assert len(set(cases)) == len(cases)
    assert all(valid(c) for c in cases), [i for i, c in enumerate(cases) if not valid(c)]
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
