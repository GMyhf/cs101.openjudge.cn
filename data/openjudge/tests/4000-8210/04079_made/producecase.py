"""4079 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4079
SAMPLE_IN = '41 467 334 500 169 724 478 358 962 464 705 145 281 827 961 491 995 942 827 436\n'
SAMPLE_OUT = '41 467 334 169 145 281 358 464 436 500 478 491 724 705 962 827 961 942 995\n'
REFERENCE_SOURCE = "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef insert_into_bst(root, val):\n    if root is None:\n        return TreeNode(val)\n    if val < root.val:\n        root.left = insert_into_bst(root.left, val)\n    elif val > root.val:\n        root.right = insert_into_bst(root.right, val)\n    return root\n\ndef preorder_traversal(root):\n    return [root.val] + preorder_traversal(root.left) + preorder_traversal(root.right) if root else []\n\ndef preorderTraversal(root):\n    if root is None:\n        return []\n\n    stack = []\n    result = []\n    stack.append(root)\n\n    while stack:\n        node = stack.pop()\n        result.append(node.val)\n\n        # 先将右子节点入栈，再将左子节点入栈\n        if node.right:\n            stack.append(node.right)\n        if node.left:\n            stack.append(node.left)\n\n    return result\n\n# 读取输入并转换成整数列表\nnumbers = list(map(int, input().split()))\n\n# 构造二叉搜索树\nbst_root = None\nfor num in numbers:\n    bst_root = insert_into_bst(bst_root, num)\n\n# 前序遍历二叉搜索树并输出\n#print(' '.join(map(str, preorder_traversal(bst_root))))\nprint(' '.join(map(str, preorderTraversal(bst_root))))\n"

def sample(body, label):
    fence = r"\x60\x60\x60"
    pattern = rf"(?:{label})\s*\n+{fence}\n(.*?){fence}"
    values = re.findall(pattern, body, re.S | re.I)
    if not values: raise ValueError("missing " + label)
    return values[0].strip() + "\n"

def g4079(r):
    vals = r.sample(range(1, 1000), r.randint(3, 40))
    return " ".join(map(str, vals)) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4079(random.Random(NUMBER + i)) for i in range(1, 20)]

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
