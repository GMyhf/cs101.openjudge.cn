import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '2\nA\n-B\n--*\n--C\n-D\n--E\n---*\n---F\n0\nA\n-B\n-C\n0\n'
SAMPLE_OUT = 'ABCDEF\nCBFEDA\nBCAEFD\n\nABC\nBCA\nBAC\n'
CASES = ['2\nA\n-B\n--*\n--C\n-D\n--E\n---*\n---F\n0\nA\n-B\n-C\n0\n', '2\nA\n-*\n-B\n0\nC\n-D\n--*\n--E\n---*\n---G\n-F\n0\n', '3\nA\n-B\n-C\n-D\n--*\n--E\n0\nF\n-G\n--*\n--I\n---J\n---L\n-H\n--*\n--N\n-K\n--*\n--M\n0\nO\n-P\n--*\n--Q\n---*\n---R\n----*\n----V\n-S\n--*\n--U\n-T\n0\n', '1\nA\n-B\n--D\n---*\n---F\n----*\n----G\n-----*\n-----I\n--H\n---*\n---J\n----*\n----K\n-C\n-E\n0\n', '3\nA\n-B\n--*\n--E\n---*\n---G\n-C\n--*\n--H\n-D\n-F\n0\nI\n-*\n-J\n0\nK\n-L\n--M\n---O\n----*\n----R\n---P\n----*\n----S\n---Q\n--N\n---*\n---T\n-U\n0\n', '1\nA\n-B\n-C\n0\n', '3\nA\n-B\n-C\n--D\n--F\n-E\n--*\n--I\n-G\n--*\n--H\n0\nJ\n-*\n-K\n--*\n--L\n---*\n---M\n----N\n----O\n0\nP\n-Q\n-R\n--*\n--S\n-T\n--*\n--U\n0\n', '2\nA\n-B\n-C\n0\nD\n-E\n--G\n---*\n---H\n--I\n--J\n--L\n-F\n-K\n0\n', '3\nA\n-B\n--*\n--E\n---*\n---G\n----*\n----H\n-C\n--*\n--F\n---*\n---I\n-D\n0\nJ\n-K\n-L\n-M\n0\nN\n-O\n-P\n--Q\n--R\n-S\n0\n', '1\nA\n-B\n--*\n--G\n-C\n--D\n---*\n---E\n--F\n-H\n0\n', '2\nA\n-B\n--D\n--E\n---*\n---H\n-C\n--F\n--G\n0\nI\n-J\n--*\n--K\n---L\n----*\n----O\n---S\n-M\n-N\n-P\n--*\n--Q\n---*\n---R\n0\n', '3\nA\n-B\n--*\n--C\n---*\n---E\n----*\n----F\n-D\n-G\n0\nH\n-*\n-I\n0\nJ\n-K\n--*\n--O\n-L\n--*\n--M\n---*\n---N\n0\n', '3\nA\n-*\n-B\n0\nC\n-D\n--E\n--F\n---*\n---J\n--G\n---*\n---H\n----*\n----I\n-----*\n-----M\n-K\n-L\n0\nN\n-O\n-P\n-Q\n--S\n--T\n-R\n0\n', '1\nA\n-*\n-B\n0\n', '1\nA\n-B\n--*\n--C\n-D\n-E\n--*\n--F\n-G\n0\n', '3\nA\n-B\n--C\n---D\n----*\n----F\n-----*\n-----H\n---E\n--I\n-G\n0\nJ\n-K\n--L\n--M\n-N\n0\nO\n-P\n--Q\n---*\n---Z\n--Y\n-R\n--S\n---U\n---X\n--T\n---V\n---W\n0\n', '3\nA\n-B\n--D\n---*\n---E\n----*\n----H\n--F\n-C\n--*\n--G\n0\nI\n-J\n-K\n--*\n--L\n0\nM\n-*\n-N\n0\n', '2\nA\n-B\n--C\n--E\n-D\n0\nF\n-G\n-H\n0\n', '2\nA\n-B\n--*\n--F\n-C\n--D\n--H\n-E\n-G\n-I\n0\nJ\n-K\n--L\n--N\n-M\n0\n', '3\nA\n-*\n-B\n--*\n--C\n---*\n---D\n----*\n----E\n0\nF\n-G\n-H\n--*\n--I\n-J\n0\nK\n-L\n--M\n---*\n---P\n--N\n-O\n0\n']
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
