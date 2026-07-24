import random, subprocess, tempfile
from pathlib import Path
SAMPLE_IN = '2\nC 3 E 3 F 0 G 0 K 0 H 0 J 0\nD 2 X 0 I 0\n'
SAMPLE_OUT = 'K H J E F G C X I D\n'
CASES = ['2\nC 3 E 3 F 0 G 0 K 0 H 0 J 0\nD 2 X 0 I 0\n', '3\nA 1 B 1 C 0\nD 2 E 1 F 1 H 0 G 0\nI 3 J 0 K 0 L 0\n', '3\nA 2 B 0 C 0\nD 2 E 0 F 0\nG 4 H 0 I 1 J 0 L 0 K 0\n', '2\nA 3 B 0 C 0 D 0\nE 2 F 0 G 0\n', '3\nA 1 B 1 C 1 D 0\nE 3 F 1 G 1 H 0 J 0 I 0\nK 4 L 1 M 1 N 1 P 0 O 0 R 0 Q 0\n', '2\nA 2 B 1 C 0 D 0\nE 1 F 1 G 0\n', '1\nA 2 B 0 C 2 D 2 E 0 F 0 G 0\n', '3\nA 2 B 1 D 0 C 0\nE 4 F 1 H 0 I 0 J 0 G 0\nK 1 L 2 M 0 N 0\n', '2\nA 2 B 1 C 2 G 0 D 1 E 1 H 0 F 0\nI 1 J 0\n', '1\nA 2 B 2 C 1 E 1 G 0 D 0 F 0\n', '3\nA 3 B 0 C 0 D 1 E 0\nF 2 G 1 H 0 I 0\nJ 2 K 0 L 0\n', '3\nA 3 B 0 C 1 E 1 D 0 F 0\nG 4 H 1 I 0 K 0 L 0 J 0\nM 1 N 1 O 0\n', '3\nA 3 B 1 C 0 D 0 E 0\nF 1 G 0\nH 1 I 1 J 1 K 0\n', '3\nA 1 B 0\nC 3 D 0 E 0 F 0\nG 1 H 0\n', '2\nA 4 B 0 C 1 E 0 F 0 D 1 G 0\nH 2 I 1 K 0 J 2 L 0 M 1 N 0\n', '1\nA 3 B 1 C 0 D 2 G 0 E 0 F 0\n', '1\nA 2 B 0 C 0\n', '3\nA 5 B 0 C 1 D 0 E 0 F 1 G 0 H 0\nI 3 J 0 K 1 L 2 M 0 N 1 P 0 O 0\nQ 3 R 0 S 3 W 0 T 0 U 1 V 0 X 0\n', '1\nA 2 B 2 C 2 D 1 G 0 E 0 H 0 F 0\n', '3\nA 3 B 1 C 1 G 0 F 0 D 1 E 0\nH 1 I 2 J 0 K 0\nL 2 M 1 N 2 O 2 R 0 S 0 P 0 Q 0\n']
REFERENCE_SOURCE = 'from collections import deque\n\nn = int(input())\nans = []\n\nclass TreeNode:\n    def __init__(self, x):\n        self.val = x\n        self.first_child = None\n        self.next_sibling = None\n    def __str__(self):\n        return str(self.val)\n\ndef postorder(x):\n    global ans\n    if x is None:\n        return\n    y = x.first_child\n    while y:\n        postorder(y)\n        y = y.next_sibling\n    ans.append(x.val)\n\ndef inorder(x):\n    global ans\n    if x:\n        inorder(x.first_child)\n        ans.append(x.val)\n        inorder(x.next_sibling)\n\n\nfor _ in range(n):\n    s = input().split()\n    root = TreeNode(s[0])\n    q = deque([[root, int(s[1])]])\n    i = 2\n    while q:\n        front = q.popleft()\n        cur = front[0]\n        for j in range(front[1]):\n            if j == 0:\n                cur.first_child = TreeNode(s[i])\n                cur = cur.first_child\n            else:\n                cur.next_sibling = TreeNode(s[i])\n                cur = cur.next_sibling\n            q.append((cur, int(s[i+1])))\n            i += 2\n    #postorder(root)\n    inorder(root)   #二叉树的中序遍历 = 原多叉树的后序遍历\nprint(*ans)\n'
assert CASES[0] == SAMPLE_IN
random.seed(7161)
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index, content in enumerate(CASES):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
