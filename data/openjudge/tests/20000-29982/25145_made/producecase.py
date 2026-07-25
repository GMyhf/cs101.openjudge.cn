import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "from collections import deque\n\nclass Node:\n    def __init__(self, data):\n        self.data = data\n        self.left = None\n        self.right = None\n\ndef build_tree(inorder, postorder):\n    if inorder:\n        root = Node(postorder.pop())\n        root_index = inorder.index(root.data)\n        root.right = build_tree(inorder[root_index+1:], postorder)\n        root.left = build_tree(inorder[:root_index], postorder)\n        return root\n\ndef level_order_traversal(root):\n    if root is None:\n        return []\n    result = []\n    queue = deque([root])\n    while queue:\n        node = queue.popleft()\n        result.append(node.data)\n        if node.left:\n            queue.append(node.left)\n        if node.right:\n            queue.append(node.right)\n    return result\n\nn = int(input())\nfor _ in range(n):\n    inorder = list(input().strip())\n    postorder = list(input().strip())\n    root = build_tree(inorder, postorder)\n    print(''.join(level_order_traversal(root)))\n"
SAMPLE_IN = '2\nLZGD\nLGDZ\nBKTVQP\nTPQVKB\n'
SAMPLE_OUT = 'ZLDG\nBKVTQP\n'
def _tree_pair(r, max_size=20):
    def build(chars):
        if not chars: return None
        i = r.randrange(len(chars))
        return (chars[i], build(chars[:i]), build(chars[i + 1:]))
    chars = r.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", r.randint(2, max_size)); tree = build(chars)
    def inorder(node): return "" if node is None else inorder(node[1]) + node[0] + inorder(node[2])
    def postorder(node): return "" if node is None else postorder(node[1]) + postorder(node[2]) + node[0]
    def preorder(node): return "" if node is None else node[0] + preorder(node[1]) + preorder(node[2])
    ino, post, pre = inorder(tree), postorder(tree), preorder(tree)
    assert len(ino) == len(post) == len(pre) and sorted(ino) == sorted(post) == sorted(pre)
    return tree, ino, post, pre

def generate_case(r):
    pairs = [_tree_pair(r, 26)[1:3] for _ in range(r.randint(2, 8))]
    assert all(len(ino) <= 26 for ino, _ in pairs)
    return str(len(pairs)) + "\n" + "\n".join(f"{ino}\n{post}" for ino, post in pairs) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(25145 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
