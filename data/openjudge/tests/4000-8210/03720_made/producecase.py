import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '2\nA\n-B\n--*\n--C\n-D\n--E\n---*\n---F\n0\nA\n-B\n-C\n0\n'
SAMPLE_OUT = 'ABCDEF\nCBFEDA\nBCAEFD\n\nABC\nBCA\nBAC\n'
CASES = ['2\nA\n-B\n--*\n--C\n-D\n--E\n---*\n---F\n0\nA\n-B\n-C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n', '1\nA\n-B\n--*\n--C\n0\n']
REFERENCE_SOURCE = 'class Node:\n    def __init__(self, x, depth):\n        self.x = x\n        self.depth = depth\n        self.lchild = None\n        self.rchild = None\n\n    def preorder_traversal(self):\n        nodes = [self.x]\n        if self.lchild and self.lchild.x != \'*\':\n            nodes += self.lchild.preorder_traversal()\n        if self.rchild and self.rchild.x != \'*\':\n            nodes += self.rchild.preorder_traversal()\n        return nodes\n\n    def inorder_traversal(self):\n        nodes = []\n        if self.lchild and self.lchild.x != \'*\':\n            nodes += self.lchild.inorder_traversal()\n        nodes.append(self.x)\n        if self.rchild and self.rchild.x != \'*\':\n            nodes += self.rchild.inorder_traversal()\n        return nodes\n\n    def postorder_traversal(self):\n        nodes = []\n        if self.lchild and self.lchild.x != \'*\':\n            nodes += self.lchild.postorder_traversal()\n        if self.rchild and self.rchild.x != \'*\':\n            nodes += self.rchild.postorder_traversal()\n        nodes.append(self.x)\n        return nodes\n\n\ndef build_tree():\n    n = int(input())\n    for _ in range(n):\n        tree = []\n        stack = []\n        while True:\n            s = input()\n            if s == \'0\':\n                break\n            depth = len(s) - 1\n            node = Node(s[-1], depth)\n            tree.append(node)\n\n            # Finding the parent for the current node\n            while stack and tree[stack[-1]].depth >= depth:\n                stack.pop()\n            if stack:  # There is a parent\n                parent = tree[stack[-1]]\n                if not parent.lchild:\n                    parent.lchild = node\n                else:\n                    parent.rchild = node\n            stack.append(len(tree) - 1)\n\n        # Now tree[0] is the root of the tree\n        yield tree[0]\n\n\n# Read each tree and perform traversals\nfor root in build_tree():\n    print("".join(root.preorder_traversal()))\n    print("".join(root.postorder_traversal()))\n    print("".join(root.inorder_traversal()))\n    print()\n\n'
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(3720)
assert CASES[0] == SAMPLE_IN
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
def generate_case(index):
    return CASES[index]
root = Path(__file__).parent / "data"
for index in range(20):
    content = generate_case(index)
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
