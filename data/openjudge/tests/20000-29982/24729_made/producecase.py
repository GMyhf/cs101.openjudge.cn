"""24729 括号嵌套树 数据生成器。

第 0 组为题面样例；其余为固定种子生成的树：单结点、两结点、26 结点长链、
26 结点菊花、满二叉、多叉随机树等。答案由下面 AC 逻辑（与 samplecode.py 相同）计算。
"""
import random
import re
import string
from pathlib import Path

SAMPLE = "A(B(E),C(F,G),D(H(I)))\n"
SEED = 24729


# --- AC 逻辑（同 samplecode.py） ---
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []


def parse_tree(s):
    stack = []
    node = None
    for char in s:
        if char.isalpha():
            node = TreeNode(char)
            if stack:
                stack[-1].children.append(node)
        elif char == '(':
            if node:
                stack.append(node)
                node = None
        elif char == ')':
            if stack:
                node = stack.pop()
    return node


def preorder(node):
    output = [node.value]
    for child in node.children:
        output.extend(preorder(child))
    return ''.join(output)


def postorder(node):
    output = []
    for child in node.children:
        output.extend(postorder(child))
    output.append(node.value)
    return ''.join(output)


def solve(text):
    root = parse_tree(''.join(text.split()))
    return preorder(root) + "\n" + postorder(root) + "\n"


# --- 输入校验 ---
def valid(text):
    """题面：一行括号嵌套表示，结点为大写字母，不超过 26 个结点，无空格。
    文法：T := L | L '(' T (',' T)* ')'。这里额外要求结点字母互异（前序/后序才有意义）。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    s = text[:-1]
    pos = 0

    def tree():
        nonlocal pos
        if pos >= len(s) or not ('A' <= s[pos] <= 'Z'):
            raise ValueError
        pos += 1
        if pos < len(s) and s[pos] == '(':
            pos += 1
            tree()
            while pos < len(s) and s[pos] == ',':
                pos += 1
                tree()
            if pos >= len(s) or s[pos] != ')':
                raise ValueError
            pos += 1

    try:
        tree()
    except ValueError:
        return False
    if pos != len(s):
        return False
    letters = re.findall(r'[A-Z]', s)
    return 1 <= len(letters) <= 26 and len(set(letters)) == len(letters)


# --- 生成 ---
def serialize(node):
    if not node[1]:
        return node[0]
    return node[0] + "(" + ",".join(serialize(c) for c in node[1]) + ")"


def labels(r, n):
    a = list(string.ascii_uppercase)
    r.shuffle(a)
    return a[:n]


def random_tree(r, n, mode="uniform"):
    lab = labels(r, n)
    nodes = [(lab[0], [])]
    for i in range(1, n):
        if mode == "deep":      # 偏向最近加入的结点，树更深
            p = nodes[max(0, len(nodes) - 1 - r.randint(0, 2))]
        elif mode == "wide":    # 偏向前几个结点，树更宽
            p = nodes[r.randint(0, min(2, len(nodes) - 1))]
        else:
            p = r.choice(nodes)
        c = (lab[i], [])
        p[1].append(c)
        nodes.append(c)
    return serialize(nodes[0])


def chain(lab):
    t = (lab[-1], [])
    for x in reversed(lab[:-1]):
        t = (x, [t])
    return serialize(t)


def full_binary(lab):
    nodes = [(x, []) for x in lab]
    for i in range(1, len(nodes)):
        nodes[(i - 1) // 2][1].append(nodes[i])
    return serialize(nodes[0])


def build_cases():
    r = random.Random(SEED)
    cases = [SAMPLE, "A\n", "Z\n", "B(A)\n", "A(B,C)\n"]
    cases.append(chain(list(string.ascii_uppercase)) + "\n")
    cases.append(chain(labels(r, 26)) + "\n")
    lab = labels(r, 26)
    cases.append(lab[0] + "(" + ",".join(lab[1:]) + ")\n")      # 菊花
    cases.append(full_binary(labels(r, 26)) + "\n")
    cases.append(full_binary(list(string.ascii_uppercase)[::-1]) + "\n")
    for n in (26, 26, 26, 25, 24):
        for mode in ("uniform", "deep", "wide"):
            cases.append(random_tree(r, n, mode) + "\n")
    while len(cases) < 40:
        cases.append(random_tree(r, r.randint(3, 23), r.choice(["uniform", "deep", "wide"])) + "\n")
    out = []
    for c in cases:
        if c not in out:
            out.append(c)
    return out


def main():
    d = Path("data")
    d.mkdir(exist_ok=True)
    cases = build_cases()
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i, c in enumerate(cases):
        (d / f"{i}.in").write_text(c)
        (d / f"{i}.out").write_text(solve(c))


if __name__ == "__main__":
    main()
