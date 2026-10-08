"""7161 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 33 组数据（原 20 组 + 13 组追加）。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 7161
SAMPLE_IN = '2\nC 3 E 3 F 0 G 0 K 0 H 0 J 0\nD 2 X 0 I 0\n'
SAMPLE_OUT = 'K H J E F G C X I D\n'
REFERENCE_SOURCE = 'from collections import deque\n\nn = int(input())\nans = []\n\nclass TreeNode:\n    def __init__(self, x):\n        self.val = x\n        self.first_child = None\n        self.next_sibling = None\n    def __str__(self):\n        return str(self.val)\n\ndef postorder(x):\n    global ans\n    if x is None:\n        return\n    y = x.first_child\n    while y:\n        postorder(y)\n        y = y.next_sibling\n    ans.append(x.val)\n\ndef inorder(x):\n    global ans\n    if x:\n        inorder(x.first_child)\n        ans.append(x.val)\n        inorder(x.next_sibling)\n\n\nfor _ in range(n):\n    s = input().split()\n    root = TreeNode(s[0])\n    q = deque([[root, int(s[1])]])\n    i = 2\n    while q:\n        front = q.popleft()\n        cur = front[0]\n        for j in range(front[1]):\n            if j == 0:\n                cur.first_child = TreeNode(s[i])\n                cur = cur.first_child\n            else:\n                cur.next_sibling = TreeNode(s[i])\n                cur = cur.next_sibling\n            q.append((cur, int(s[i+1])))\n            i += 2\n    #postorder(root)\n    inorder(root)   #二叉树的中序遍历 = 原多叉树的后序遍历\nprint(*ans)\n'

def g7161(r):
    count = r.randint(1, 3); used = 0; lines = [str(count)]
    for tree in range(count):
        size = r.randint(2, min(8, 26 - used)); labels = [chr(65 + used + i) for i in range(size)]; used += size
        children = [[] for _ in range(size)]
        for i in range(1, size): children[r.randrange(i)].append(i)
        queue = [0]; encoded = []
        while queue:
            node = queue.pop(0); kids = children[node]
            encoded += [labels[node], str(len(kids))]
            queue.extend(kids)
        lines.append(" ".join(encoded))
    return "\n".join(lines) + "\n"

def valid(text):
    """题面：第一行正整数 n（非空树的数目）；随后 n 行，每行一棵树的带度数层次序列 "名 度 名 度 ..."，
    结点名为 A-Z 的单个大写字母，度数为非负整数，且序列必须恰好构成一棵树（层次序列的度数自洽）。"""
    try:
        lines = text.split("\n")
        if lines[-1] != "": return False
        lines = lines[:-1]
        if lines[0] != str(int(lines[0])): return False
        n = int(lines[0])
        if n < 1 or len(lines) != n + 1: return False
        for ln in lines[1:]:
            t = ln.split(" ")
            if len(t) % 2: return False
            names, degs = t[0::2], t[1::2]
            if not all(len(x) == 1 and "A" <= x <= "Z" for x in names): return False
            if any(d != str(int(d)) or int(d) < 0 for d in degs): return False
            k = len(names); avail = 1
            for i, d in enumerate(map(int, degs)):
                avail += d
                if i < k - 1 and avail < i + 2: return False
            if avail != k: return False
        return True
    except Exception:
        return False

def encode(r, parent_choice, sizes):
    """sizes: 每棵树的结点数；parent_choice(i, r) 给出 BFS 之前第 i 个结点的父亲（< i）。字母全局互异且打乱。"""
    letters = [chr(65 + i) for i in range(26)]; r.shuffle(letters)
    used = 0; lines = [str(len(sizes))]
    for size in sizes:
        labels = letters[used:used + size]; used += size
        children = [[] for _ in range(size)]
        for i in range(1, size): children[parent_choice(i, r)].append(i)
        queue = [0]; enc = []
        while queue:
            node = queue.pop(0); kids = children[node]
            enc += [labels[node], str(len(kids))]
            queue.extend(kids)
        lines.append(" ".join(enc))
    return "\n".join(lines) + "\n"

def rand_sizes(r, total, trees):
    cuts = sorted(r.sample(range(1, total), trees - 1))
    return [b - a for a, b in zip([0] + cuts, cuts + [total])]

RANDP = lambda i, r: r.randrange(i)
EXTRA = [
    lambda r: "1\nA 0\n",
    lambda r: "3\nZ 0\nY 1 X 0\nW 0\n",
    lambda r: encode(r, RANDP, [1] * 26),
    lambda r: encode(r, lambda i, r: i - 1, [26]),
    lambda r: encode(r, lambda i, r: 0, [26]),
    lambda r: encode(r, lambda i, r: (i - 1) // 2, [26]),
    lambda r: encode(r, lambda i, r: (i - 1) // 3, [13, 13]),
    lambda r: encode(r, RANDP, [26]),
    lambda r: encode(r, RANDP, [25, 1]),
    lambda r: encode(r, lambda i, r: max(0, i - r.randint(1, 2)), rand_sizes(r, 26, 4)),
    lambda r: encode(r, RANDP, rand_sizes(r, 26, 8)),
    lambda r: encode(r, RANDP, rand_sizes(r, 26, 3)),
    lambda r: encode(r, RANDP, rand_sizes(r, 20, 5)),
]

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g7161(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    for i, f in enumerate(EXTRA):
        cases.append(f(random.Random(NUMBER * 10 + i)))
    assert all(valid(c) for c in cases)
    assert len(set(cases)) == len(cases)
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
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
