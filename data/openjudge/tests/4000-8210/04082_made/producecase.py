"""4082 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4082
SAMPLE_IN = '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n'
SAMPLE_OUT = 'a f c b e d\n'
REFERENCE_SOURCE = "from collections import defaultdict\n\nn = int(input())\nif n == 0:\n    print()\n    exit()\n\npreorder = input().split()\n\n# 初始化根节点\nroot = preorder[0][0]\nroot_type = preorder[0][1]\n\ntier = defaultdict(list)\ntier[0].append(root)\n\nnodes = [root]\nlevel = 0\ntypes = {root: root_type}\n\nfor i in range(1, n):\n    current = preorder[i]\n    name = current[0]\n    typ = current[1]\n    types[name] = typ\n\n    prev_node = nodes[-1]\n    prev_type = types[prev_node]\n\n    # 计算层级变化\n    if prev_type == '1':\n        level -= 1\n    else:\n        level += 1\n\n    nodes.append(name)\n\n    # 只添加非虚节点到对应层级\n    if name != '$':\n        tier[level].append(name)\n\n# 按层级顺序排序并逆序每层节点\nsorted_levels = sorted(tier.items(), key=lambda x: x[0])\nresult = []\nfor level, chars in sorted_levels:\n    result.extend(reversed(chars))\n\nprint(' '.join(result))\n"

def g4082(r):
    node_count = r.randint(4, 16)
    children = [[] for _ in range(node_count)]
    for node in range(1, node_count):
        children[r.randrange(node)].append(node)

    class Binary:
        def __init__(self, label):
            self.label = label
            self.left = None
            self.right = None

    def convert(node, sibling=None):
        result = Binary(chr(ord("a") + node))
        if children[node]:
            result.left = convert(children[node][0], children[node][1:])
        if sibling:
            result.right = convert(sibling[0], sibling[1:])
        return result

    def complete(node):
        if node is None:
            return
        if node.left is None and node.right is not None:
            node.left = Binary("$")
        elif node.left is not None and node.right is None:
            node.right = Binary("$")
        complete(node.left)
        complete(node.right)

    def tokens(node):
        if node is None:
            return []
        internal = node.left is not None or node.right is not None
        result = [node.label + ("0" if internal else "1")]
        result += tokens(node.left)
        result += tokens(node.right)
        return result

    root = convert(0)
    complete(root)
    values = tokens(root)
    return str(len(values)) + "\n" + " ".join(values) + "\n"

def valid(text):
    """题面契约：第一行结点数 n（不大于 50），第二行 n 个两字符结点，
    编号为小写字母或虚结点 $，标记 0/1；整体须是一棵合法“伪满二叉树”的前序：
    内部结点恰有两个孩子、虚结点只能是叶且不会成对出现、根（原树根无兄弟）
    若非叶则右孩子为 $。"""
    lines = text.split("\n")
    if not text.endswith("\n") or len(lines) != 3:
        return False
    head = lines[0].split()
    if len(head) != 1 or not head[0].isdigit():
        return False
    n = int(head[0])
    toks = lines[1].split(" ")
    if not (1 <= n <= 50) or len(toks) != n:
        return False
    for t in toks:
        if len(t) != 2 or t[1] not in "01":
            return False
        if not ("a" <= t[0] <= "z" or t[0] == "$"):
            return False
        if t[0] == "$" and t[1] != "1":
            return False
    pos = 0

    def parse():
        # 返回子树是否为虚结点；失败抛 ValueError
        nonlocal pos
        if pos >= n:
            raise ValueError
        t = toks[pos]
        pos += 1
        if t[1] == "1":
            return t[0] == "$"
        left = parse()
        right = parse()
        if left and right:
            raise ValueError
        return False

    try:
        if toks[0][0] == "$":
            return False
        pos = 1
        if toks[0][1] == "0":
            if parse():          # 根的左孩子（第一个子结点）必须是真结点
                return False
            if pos >= n or toks[pos] != "$1":
                return False     # 原树根没有兄弟，右孩子只能是虚结点
            pos += 1
    except (ValueError, RecursionError):
        return False
    return pos == n


def tokens_from_parents(parent, labels):
    """parent[i] < i；按左儿子右兄弟转二叉树、补 $、前序输出。"""
    k = len(parent)
    children = [[] for _ in range(k)]
    for v in range(1, k):
        children[parent[v]].append(v)
    left = [None] * k
    right = [None] * k
    for v in range(k):
        if children[v]:
            left[v] = children[v][0]
            for a, b in zip(children[v], children[v][1:]):
                right[a] = b
    out = []
    stack = [0]
    while stack:
        v = stack.pop()
        if v == "$":
            out.append("$1")
            continue
        l, r = left[v], right[v]
        if l is None and r is None:
            out.append(labels[v] + "1")
            continue
        out.append(labels[v] + "0")
        stack.append("$" if r is None else r)
        stack.append("$" if l is None else l)
    return str(len(out)) + "\n" + " ".join(out) + "\n"


def extra_cases():
    """补规模与形状：原数据最多 23 个结点，题面上限 50。"""
    r = random.Random(NUMBER * 7 + 1)
    letters = "abcdefghijklmnopqrstuvwxyz"
    cases = ["1\na1\n"]                                       # 只有根
    cases.append(tokens_from_parents([-1, 0], "ab"))            # 两个结点
    cases.append(tokens_from_parents([-1, 0, 0], "abc"))
    cases.append(tokens_from_parents([-1] + list(range(24)), letters))        # 链：25 个真结点 + 24 个 $
    cases.append(tokens_from_parents([-1] + [0] * 24, letters))               # 菊花：25 个结点（共 49 个 token）
    cases.append(tokens_from_parents([-1] + [(v - 1) // 3 for v in range(1, 26)], letters[::-1]))
    tries = 0
    while len(cases) < 16:
        tries += 1
        k = r.randint(20, 26)
        mode = len(cases) % 3
        if mode == 0:
            par = [-1] + [r.randrange(v) for v in range(1, k)]
        elif mode == 1:
            par = [-1] + [r.randrange(max(0, v - 3), v) for v in range(1, k)]
        else:
            par = [-1] + [r.randrange(min(v, 3)) for v in range(1, k)]
        labs = list(letters)
        r.shuffle(labs)
        c = tokens_from_parents(par, labs[:k])
        if int(c.split()[0]) <= 50 and c not in cases:
            cases.append(c)
    return cases


def build_cases():
    return [SAMPLE_IN] + [g4082(random.Random(NUMBER + i)) for i in range(1, 20)] + extra_cases()

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
