import random, subprocess, sys, tempfile
from pathlib import Path
def g1577(r):
    def layers(order):
        root = order[0]; left = [x for x in order[1:] if x < root]; right = [x for x in order[1:] if x > root]
        a, b = layers(left) if left else [], layers(right) if right else []
        out = []
        for i in range(max(len(a), len(b))): out.append((a[i] if i < len(a) else "") + (b[i] if i < len(b) else ""))
        out.append(root); return out
    datasets = []
    for _ in range(r.randint(1, 3)):
        letters = r.sample(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), r.randint(1, 18))
        datasets += layers(letters) + ["*"]
    datasets[-1] = "$"
    return "\n".join(datasets) + "\n"

REFERENCE="# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 1577: Falling Leaves\n# Fenced code block index: 5\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01577/\n# License: not declared in source collection; no license is inferred.\nclass TreeNode:\n    def __init__(self, data):\n        self.data = data\n        self.left = None\n        self.right = None\n\n\ndef build_bst(leaves):\n    if not leaves:\n        return None\n\n    root = TreeNode(leaves[0])\n    for leaf in leaves[1:]:\n        insert_node(root, leaf)\n\n    return root\n\n\ndef insert_node(root, leaf):\n    if leaf < root.data:\n        if root.left is None:\n            root.left = TreeNode(leaf)\n        else:\n            insert_node(root.left, leaf)\n    else:\n        if root.right is None:\n            root.right = TreeNode(leaf)\n        else:\n            insert_node(root.right, leaf)\n\n\ndef preorder_traversal(root):\n    if root is None:\n        return []\n    traversal = [root.data]\n    traversal.extend(preorder_traversal(root.left))\n    traversal.extend(preorder_traversal(root.right))\n    return traversal\n\n\n# 读取输入数据\nflag = 0\nwhile True:\n    leaves = []\n    while True:\n        line = input().strip()\n        if line == '*':\n            break\n        elif line == '$':\n            flag = 1\n            break\n        else:\n            leaves.extend(line)\n\n    # 构建二叉搜索树\n    root = build_bst(leaves[::-1])\n\n    # 输出前序遍历结果\n    traversal_result = preorder_traversal(root)\n    print(''.join(traversal_result))\n\n    if flag:\n        break\n"
SAMPLE='BDHPY\nCM\nGQ\nK\n*\nAC\nB\n$\n'
GENERATOR='g1577'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
