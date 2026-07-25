import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "from collections import deque\n\nclass TreeNode:\n    def __init__(self, value):\n        self.value = value\n        self.left = None\n        self.right = None\n\ndef build_tree(postfix):\n    stack = []\n    for char in postfix:\n        node = TreeNode(char)\n        if char.isupper():\n            node.right = stack.pop()\n            node.left = stack.pop()\n        stack.append(node)\n    return stack[0]\n\ndef level_order_traversal(root):\n    dq = [root]\n    traversal = []\n    while dq:\n        node = dq.pop(0)\n        traversal.append(node.value)\n        if node.left:\n            dq.append(node.left)\n        if node.right:\n            dq.append(node.right)\n    return traversal\n\nn = int(input().strip())\nfor _ in range(n):\n    postfix = input().strip()\n    root = build_tree(postfix)\n    queue_expression = level_order_traversal(root)[::-1]\n    print(''.join(queue_expression))\n"
SAMPLE_IN = '2\nxyPzwIM\nabcABdefgCDEF\n'
SAMPLE_OUT = 'wzyxIPM\ngfCecbDdAaEBF\n'
def _postfix(r, letters=False, depth=0):
    if depth >= 3 or r.random() < .35:
        return r.choice("abcdefghijklmnopqrstuvwxyz") if letters else str(r.randint(1, 30))
    op = r.choice("+-*/") if not letters else r.choice("PQRS")
    return _postfix(r, letters, depth + 1) + " " + _postfix(r, letters, depth + 1) + " " + op

def generate_case(r):
    lines = [_postfix(r, letters=True) for _ in range(r.randint(3, 8))]
    assert all(len(line.replace(" ", "")) <= 100 for line in lines)
    return str(len(lines)) + "\n" + "\n".join(line.replace(" ", "") for line in lines) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(25140 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
