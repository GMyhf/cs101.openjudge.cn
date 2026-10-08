import random, subprocess, sys, tempfile
from pathlib import Path

def _insert(tree, c):
    # tree: dict 字母 -> [左, 右]；返回根
    root = tree.get("#")
    if root is None:
        tree["#"] = c; tree[c] = [None, None]; return
    x = root
    while True:
        side = 0 if c < x else 1
        if tree[x][side] is None:
            tree[x][side] = c; tree[c] = [None, None]; return
        x = tree[x][side]

def _leaf_layers(tree):
    root = tree.get("#"); layers = []
    def height(x):
        if x is None: return -1
        h = 1 + max(height(tree[x][0]), height(tree[x][1]))
        while len(layers) <= h: layers.append([])
        layers[h].append(x); return h
    height(root)
    return ["".join(sorted(l)) for l in layers]

def valid(text):
    # 题面：若干组，每组一行或多行大写字母（行内按字母升序），组间以只含 '*' 的行分隔，
    # 最后一组后跟只含 '$' 的行；无空格无空行；每组必须恰是某棵字母二叉搜索树逐轮摘叶的结果。
    if not text.endswith("\n"): text += "\n"
    lines = text[:-1].split("\n")
    if not lines or lines[-1] != "$": return False
    groups, cur = [], []
    for ln in lines[:-1]:
        if ln == "*":
            groups.append(cur); cur = []
        else:
            cur.append(ln)
    groups.append(cur)
    for g in groups:
        if not g: return False
        for ln in g:
            if not ln or not all("A" <= c <= "Z" for c in ln) or list(ln) != sorted(set(ln)): return False
        letters = "".join(g)
        if len(set(letters)) != len(letters): return False
        tree = {}
        for ln in reversed(g):
            for c in ln: _insert(tree, c)
        if _leaf_layers(tree) != g: return False
    return True

UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def layers_of(order):
    tree = {}
    for c in order: _insert(tree, c)
    return _leaf_layers(tree)

def balanced(letters):
    if not letters: return []
    m = len(letters) // 2
    return [letters[m]] + balanced(letters[:m]) + balanced(letters[m + 1:])

def fmt(groups):
    return "\n*\n".join("\n".join(layers_of(g)) for g in groups) + "\n$\n"

def build_cases():
    r = random.Random(1577)
    cases = []
    # 边界：单节点、两节点（左/右）、链（26 层）、满 26 字母平衡树
    cases.append(fmt(["A", "Z", "BA", "AB"]))
    cases.append(fmt([UP, UP[::-1]]))
    cases.append(fmt(["".join(balanced(UP)), "".join(balanced(UP[3:20]))]))
    zig = []
    lo, hi = 0, 25
    while lo <= hi:
        zig.append(UP[lo]); lo += 1
        if lo <= hi: zig.append(UP[hi]); hi -= 1
    cases.append(fmt(["".join(zig), "".join(zig[::-1])]))
    # 原数据那样的小随机
    for _ in range(10):
        cases.append(fmt(["".join(r.sample(UP, r.randint(1, 18))) for _ in range(r.randint(1, 3))]))
    # 全 26 字母随机插入序
    for _ in range(12):
        cases.append(fmt(["".join(r.sample(UP, r.randint(20, 26))) for _ in range(r.randint(1, 6))]))
    # 多组
    cases.append(fmt(["".join(r.sample(UP, r.randint(1, 26))) for _ in range(300)]))
    cases.append(fmt(["".join(r.sample(UP, 26)) for _ in range(500)]))
    while len(cases) < 39:
        cases.append(fmt(["".join(r.sample(UP, r.randint(1, 26))) for _ in range(r.randint(1, 20))]))
    return cases

REFERENCE="# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 1577: Falling Leaves\n# Fenced code block index: 5\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01577/\n# License: not declared in source collection; no license is inferred.\nclass TreeNode:\n    def __init__(self, data):\n        self.data = data\n        self.left = None\n        self.right = None\n\n\ndef build_bst(leaves):\n    if not leaves:\n        return None\n\n    root = TreeNode(leaves[0])\n    for leaf in leaves[1:]:\n        insert_node(root, leaf)\n\n    return root\n\n\ndef insert_node(root, leaf):\n    if leaf < root.data:\n        if root.left is None:\n            root.left = TreeNode(leaf)\n        else:\n            insert_node(root.left, leaf)\n    else:\n        if root.right is None:\n            root.right = TreeNode(leaf)\n        else:\n            insert_node(root.right, leaf)\n\n\ndef preorder_traversal(root):\n    if root is None:\n        return []\n    traversal = [root.data]\n    traversal.extend(preorder_traversal(root.left))\n    traversal.extend(preorder_traversal(root.right))\n    return traversal\n\n\n# 读取输入数据\nflag = 0\nwhile True:\n    leaves = []\n    while True:\n        line = input().strip()\n        if line == '*':\n            break\n        elif line == '$':\n            flag = 1\n            break\n        else:\n            leaves.extend(line)\n\n    # 构建二叉搜索树\n    root = build_bst(leaves[::-1])\n\n    # 输出前序遍历结果\n    traversal_result = preorder_traversal(root)\n    print(''.join(traversal_result))\n\n    if flag:\n        break\n"
SAMPLE='BDHPY\nCM\nGQ\nK\n*\nAC\nB\n$\n'
LANGUAGE='Python3'

def run_all(cases):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); src = tmp/('s.py' if LANGUAGE == 'Python3' else 's.cpp'); src.write_text(REFERENCE)
        cmd = [sys.executable, '-I', str(src)]
        if LANGUAGE != 'Python3':
            exe = tmp/'s'; subprocess.run(['g++', '-std=c++20', '-O2', '-pipe', str(src), '-o', str(exe)], check=True); cmd = [str(exe)]
        outs = []
        for x in cases:
            q = subprocess.run(cmd, input=x, text=True, capture_output=True, timeout=120, check=True)
            outs.append('\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines()) + '\n')
        return outs

def main():
    cases = [SAMPLE] + build_cases()
    for i, x in enumerate(cases):
        assert valid(x), f"第 {i} 组不满足题面约束"
    outs = run_all(cases)
    out = Path('data'); out.mkdir(exist_ok=True)
    for p in out.glob('*'): p.unlink()
    for i, (x, y) in enumerate(zip(cases, outs)):
        (out/f'{i}.in').write_text(x); (out/f'{i}.out').write_text(y)

if __name__ == '__main__':
    main()
