import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "class TreeNode:\n    def __init__(self, value):\n        self.value = value\n        self.left = None\n        self.right = None\n\ndef build_tree(preorder, inorder):\n    if not preorder or not inorder:\n        return None\n    root_value = preorder[0]\n    root = TreeNode(root_value)\n    root_index_inorder = inorder.index(root_value)\n    root.left = build_tree(preorder[1:1+root_index_inorder], inorder[:root_index_inorder])\n    root.right = build_tree(preorder[1+root_index_inorder:], inorder[root_index_inorder+1:])\n    return root\n\ndef postorder_traversal(root):\n    if root is None:\n        return ''\n    return postorder_traversal(root.left) + postorder_traversal(root.right) + root.value\n\nwhile True:\n    try:\n        preorder = input().strip()\n        inorder = input().strip()\n        root = build_tree(preorder, inorder)\n        print(postorder_traversal(root))\n    except EOFError:\n        break\n"
SAMPLE_IN = 'DURPA\nRUDPA\nXTCNB\nCTBNX\n'
SAMPLE_OUT = 'RUAPD\nCBNTX\n'
def generate_case(r):
    out = []
    for _ in range(r.randint(2, 4)):
        chars = list(r.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", r.randint(2, 10))); r.shuffle(chars)
        pre = "".join(chars); ino = "".join(chars); out.extend([pre, ino])
    return "\n".join(out) + "\n"

assert SAMPLE_IN == 'DURPA\nRUDPA\nXTCNB\nCTBNX\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(22158 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
