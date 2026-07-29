import random, subprocess, sys, tempfile
from pathlib import Path
def g1145(r):
    def tree(depth):
        if depth == 0 or r.random() < .22: return "()", []
        value = r.randint(-30, 30); left, lp = tree(depth - 1); right, rp = tree(depth - 1)
        paths = [value + x for x in lp + rp] or [value]
        return f"({value}{left}{right})", paths
    expression, paths = tree(r.randint(2, 5))
    target = r.choice(paths) if paths and r.random() < .55 else r.randint(-100, 100)
    return f"{target} {expression}\n"

REFERENCE='# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 1145: Tree Summing\n# Fenced code block index: 3\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01145/\n# License: not declared in source collection; no license is inferred.\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef has_path_sum(root, target_sum):\n    if root is None:\n        return False\n\n    if root.left is None and root.right is None:  # The current node is a leaf node\n        return root.val == target_sum\n\n    left_exists = has_path_sum(root.left, target_sum - root.val)\n    right_exists = has_path_sum(root.right, target_sum - root.val)\n\n    return left_exists or right_exists\n\n\n# Parse the input string and build a binary tree\ndef parse_tree(s):\n    stack = []\n    i = 0\n\n    while i < len(s):\n        if s[i].isdigit() or s[i] == \'-\':\n            j = i\n            while j < len(s) and (s[j].isdigit() or s[j] == \'-\'):\n                j += 1\n            num = int(s[i:j])\n            node = TreeNode(num)\n            if stack:\n                parent = stack[-1]\n                if parent.left is None:\n                    parent.left = node\n                else:\n                    parent.right = node\n            stack.append(node)\n            i = j\n        elif s[i] == \'[\':\n            i += 1\n        elif s[i] == \']\' and s[i - 1] != \'[\' and len(stack) > 1:\n            stack.pop()\n            i += 1\n        else:\n            i += 1\n\n    return stack[0] if len(stack) > 0 else None\n\n\nwhile True:\n    try:\n        s = input()\n    except:\n        break\n\n    s = s.split()\n    target_sum = int(s[0])\n    tree = ("").join(s[1:])\n    tree = tree.replace(\'(\', \',[\').replace(\')\', \']\')\n    while True:\n        try:\n            tree = eval(tree[1:])\n            break\n        except SyntaxError:\n            s = input().split()\n            s = ("").join(s)\n            s = s.replace(\'(\', \',[\').replace(\')\', \']\')\n            tree += s\n\n    tree = str(tree)\n    tree = tree.replace(\',[\', \'[\')\n    if tree == \'[]\':\n        print("no")\n        continue\n\n    root = parse_tree(tree)\n\n    if has_path_sum(root, target_sum):\n        print("yes")\n    else:\n        print("no")\n'
SAMPLE='22 (5(4(11(7()())(2()()))()) (8(13()())(4()(1()()))))\n20 (5(4(11(7()())(2()()))()) (8(13()())(4()(1()()))))\n10 (3\n     (2 (4 () () )\n        (8 () () ) )\n     (1 (6 () () )\n        (4 () () ) ) )\n5 ()\n'
GENERATOR='g1145'

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
