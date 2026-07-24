import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = 'dudduduudu\n'
SAMPLE_OUT = '2 => 4\n'
CASES = ['dudduduudu\n', 'dddduuuddduuddduuuduuuddduudddduuuduudduuu\n', 'ddudduuddudduuuudddduduuddduududuudduududuudduududuuddduduuddddduuduuduuddddduuduudddduduududuuuududduuududduduuuddududduuudududuu\n', 'dddddududuuduuduudududduuuddddduduuuddduduuduuuddduudddduduuuuuu\n', 'ddduudddduduudduudduddduduududuuduudduuddduduuududuuddduuduuuduudddduduuuduududdduudduudduuudddduuudduuduududduu\n', 'ddudduddduuduuuddududuuduu\n', 'ddduudddduuudddduududuuudddduududduudduuuduudduuudduuduuddudduuudu\n', 'ddduuu\n', 'ddddduduuduuuddududuudddduuududduuudduuuddduuduudduduu\n', 'ddddudduuuduududduduuudddddddduudduuududuuddduduuuddduuuddduuuuddduudduuuddduuudduuuudduduuudddddduuudududuududduduudduuduududduduuduudu\n', 'ddddddduuuddduuuddudduuduuddduudduuuduuddddduuduudduuuuddddduuuuduududuudduuduudduudddududuuuudddduuudddududuuudduuududdduududuu\n', 'ddddduuddddduduudduduuduuduuudududuudddudduuduuduudduudduuudduuddduuuudddddduuduuddduuudduuuddudduuuuddduddduuuuuddddduduuuududduuduuduudddduduuuduudu\n', 'duddduuddduudududuududduuduuddddduuduuduudduudddduuduuuduudddduduudduududuuddduuuduuddduduuduududu\n', 'dddddudddduuuuuudddudduuduuddduudduuuudddudduuuduudduduuduudddduuuuudddudduuduuu\n', 'dddddduududddduuduuuudududuudduddududuuduuduududduddddduuduudduuuddduudduuudduuudddddduuuuduuduuduudduduudududuudduu\n', 'ddduuddududuuudduududu\n', 'ddduuuddduddduuuddduduuuudduuddduuuudduduuddudduuduudu\n', 'dddddduududuuuuudddddududuududduduuudddduududdduuddduuduuduuududuududdduuuduudddududuuuuddddududuuduududuuddduuudduu\n', 'dddudduuudddduuduuddudduuudduduudduuduudduuddduduuudddduuduudduuudduduuduuddddduuuudduudduduudduuu\n', 'ddddduuududuududududuuddduudddududduuuuddddduuuuddddduduuduudddduuduudduuududuududuudddduuduuuudddduudduuduudddduuuduuduuddduuuduudddduudduuududuuddduudduuudu\n']
REFERENCE_SOURCE = "# 赵思懿，生科\nclass BinaryTreeNode:\n    def __init__(self):\n        self.parent = None\n        self.left = None\n        self.right = None\n\ndef tree_height(root):  # 计算二叉树高度\n    if not root:\n        return -1\n    else:\n        return max(tree_height(root.left), tree_height(root.right)) + 1\n\ndef original_tree_height(arr):  # 原树高度\n    height, max_height = 0, 0\n    for action in arr:\n        if action == 'd':\n            height += 1\n        elif action == 'u':\n            height -= 1\n        max_height = max(max_height, height)\n    return max_height\n\ndef build_binary_tree(arr):  # 根据输入序列建立二叉树\n    root = BinaryTreeNode()\n    current_node = root\n    for action in arr:\n        if action == 'd':\n            current_node.left = BinaryTreeNode()\n            current_node.left.parent = current_node\n            current_node = current_node.left\n        elif action == 'x':\n            current_node.right = BinaryTreeNode()\n            current_node.right.parent = current_node.parent\n            current_node = current_node.right\n        elif action == 'u':\n            current_node = current_node.parent\n    return root\n\ninput_sequence = input().replace('ud', 'x')\nbinary_tree_root = build_binary_tree(input_sequence)\nprint(original_tree_height(input_sequence), '=>', tree_height(binary_tree_root))\n\n"
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(4081)
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
