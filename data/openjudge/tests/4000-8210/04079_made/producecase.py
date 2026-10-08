"""4079 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 30 组数据。

2026-10 审计：原数据全是 r.sample 取的互异值，题面明说「数字可能会有重复」却只有样例里有一次重复；
也没有单个数、全相同、单调序列（退化成链）、负数、较大规模等情形。第 1..9 组保留原随机小组，
其余换成上述边界组；单调链长度控制在 500，免得递归插入的写法因 Python 默认递归深度出错。

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

def valid(text):
    """题面：只有一行，包含若干个数字，空格分隔（可能重复）。题面未给个数与取值范围，
    只核：恰一行、至少一个数、每个都是整数（样例为整数）。"""
    lines = text.split("\n")
    while lines and lines[-1].strip() == "":
        lines.pop()
    if len(lines) != 1:
        return False
    toks = lines[0].split()
    if not toks:
        return False
    try:
        for t in toks:
            int(t)
    except ValueError:
        return False
    return True


def line(vals):
    return " ".join(map(str, vals)) + "\n"


def g4079(r):
    vals = r.sample(range(1, 1000), r.randint(3, 40))
    return " ".join(map(str, vals)) + "\n"

def build_cases():
    cases = [SAMPLE_IN] + [g4079(random.Random(NUMBER + i)) for i in range(1, 10)]
    r = random.Random(NUMBER * 11)
    cases.append(line([5]))                                       # 单个数
    cases.append(line([7] * 30))                                  # 全相同
    cases.append(line([3, 3, 1, 1, 2, 2, 5, 4, 5, 4]))           # 成对重复
    cases.append(line(list(range(1, 501))))                       # 递增：右链
    cases.append(line(list(range(500, 0, -1))))                   # 递减：左链
    cases.append(line([r.randint(-1000, 1000) for _ in range(300)]))   # 负数、重复
    cases.append(line([r.randint(1, 20) for _ in range(200)]))         # 大量重复
    cases.append(line([r.randint(0, 10 ** 9) for _ in range(2000)]))   # 较大规模
    cases.append(line([r.randint(1, 5000) for _ in range(5000)]))      # 较大规模 + 重复
    zig = []
    lo, hi = 1, 400
    while lo <= hi:
        zig += [lo, hi] if lo != hi else [lo]
        lo += 1; hi -= 1
    cases.append(line(zig))                                       # 之字形链
    cases.append(line([0, -1, 1, 0, -1, 1]))
    mid = list(range(1, 128))
    def bal(lo, hi, out):
        if lo > hi:
            return
        m = (lo + hi) // 2; out.append(m); bal(lo, m - 1, out); bal(m + 1, hi, out)
    out = []; bal(1, 127, out)
    cases.append(line(out))                                       # 完全平衡：输出与输入相同
    cases.append(line(sorted(r.sample(range(1, 10 ** 6), 300)) + r.sample(range(1, 10 ** 6), 300)))
    cases.append(line([2, 1, 3]))
    cases.append(line([r.randint(1, 3) for _ in range(50)]))
    cases.append(line([1, 2]))
    cases.append(line([2, 1]))
    cases.append(line([r.randint(-10 ** 9, 10 ** 9) for _ in range(1000)]))
    cases.append(line([10 ** 6 - i // 2 for i in range(800)]))    # 递减且相邻成对重复
    cases.append(line([r.randint(1, 10 ** 4) for _ in range(10000)]))
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
    assert len(set(cases)) == len(cases), "组间不得重复"
    for i, c in enumerate(cases):
        assert valid(c), f"第 {i} 组越出题面约束"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
