"""4081 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4081
SAMPLE_IN = 'dudduduudu\n'
SAMPLE_OUT = '2 => 4\n'
REFERENCE_SOURCE = "# 赵思懿，生科\nclass BinaryTreeNode:\n    def __init__(self):\n        self.parent = None\n        self.left = None\n        self.right = None\n\ndef tree_height(root):  # 计算二叉树高度\n    if not root:\n        return -1\n    else:\n        return max(tree_height(root.left), tree_height(root.right)) + 1\n\ndef original_tree_height(arr):  # 原树高度\n    height, max_height = 0, 0\n    for action in arr:\n        if action == 'd':\n            height += 1\n        elif action == 'u':\n            height -= 1\n        max_height = max(max_height, height)\n    return max_height\n\ndef build_binary_tree(arr):  # 根据输入序列建立二叉树\n    root = BinaryTreeNode()\n    current_node = root\n    for action in arr:\n        if action == 'd':\n            current_node.left = BinaryTreeNode()\n            current_node.left.parent = current_node\n            current_node = current_node.left\n        elif action == 'x':\n            current_node.right = BinaryTreeNode()\n            current_node.right.parent = current_node.parent\n            current_node = current_node.right\n        elif action == 'u':\n            current_node = current_node.parent\n    return root\n\ninput_sequence = input().replace('ud', 'x')\nbinary_tree_root = build_binary_tree(input_sequence)\nprint(original_tree_height(input_sequence), '=>', tree_height(binary_tree_root))\n\n"

def g4081(r):
    node_count = r.randint(2, 80)
    children = [[] for _ in range(node_count)]
    for node in range(1, node_count):
        children[r.randrange(node)].append(node)

    def encode(node):
        result = []
        for child in children[node]:
            result.append("d")
            result.append(encode(child))
            result.append("u")
        return "".join(result)

    return encode(0) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4081(random.Random(NUMBER + i)) for i in range(1, 20)]

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
