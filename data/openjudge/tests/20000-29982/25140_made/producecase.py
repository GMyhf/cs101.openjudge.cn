import random, re, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "from collections import deque\n\nclass TreeNode:\n    def __init__(self, value):\n        self.value = value\n        self.left = None\n        self.right = None\n\ndef build_tree(postfix):\n    stack = []\n    for char in postfix:\n        node = TreeNode(char)\n        if char.isupper():\n            node.right = stack.pop()\n            node.left = stack.pop()\n        stack.append(node)\n    return stack[0]\n\ndef level_order_traversal(root):\n    dq = [root]\n    traversal = []\n    while dq:\n        node = dq.pop(0)\n        traversal.append(node.value)\n        if node.left:\n            dq.append(node.left)\n        if node.right:\n            dq.append(node.right)\n    return traversal\n\nn = int(input().strip())\nfor _ in range(n):\n    postfix = input().strip()\n    root = build_tree(postfix)\n    queue_expression = level_order_traversal(root)[::-1]\n    print(''.join(queue_expression))\n"
SAMPLE_IN = '2\nxyPzwIM\nabcABdefgCDEF\n'
SAMPLE_OUT = 'wzyxIPM\ngfCecbDdAaEBF\n'
def _postfix(r, letters=False, depth=0):
    if depth >= 3 or r.random() < .35:
        return r.choice("abcdefghijklmnopqrstuvwxyz") if letters else str(r.randint(1, 30))
    op = r.choice("+-*/") if not letters else r.choice("PQRS")
    return _postfix(r, letters, depth + 1) + " " + _postfix(r, letters, depth + 1) + " " + op

def generate_case(r):
    lines = [_postfix(r, letters=True) for _ in range(r.randint(3, 8))]
    assert all(len(line.replace(" ", "")) <= 100 for line in lines)
    return str(len(lines)) + "\n" + "\n".join(line.replace(" ", "") for line in lines) + "\n"

LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def valid(text):
    """题面契约：第一行正整数 n (n<100)；接下来恰好 n 行，每行是由字母构成、长度不超过 100 的后序表达式，
    小写字母为操作数、大写字母为二元运算符。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines or not re.fullmatch(r"[1-9][0-9]*", lines[0]):
        return False
    n = int(lines[0])
    if not 1 <= n < 100 or len(lines) != n + 1:
        return False
    for expr in lines[1:]:
        if not re.fullmatch(r"[A-Za-z]{1,100}", expr):
            return False
        depth = 0
        for ch in expr:
            if ch.islower():
                depth += 1
            else:
                if depth < 2:
                    return False
                depth -= 1
        if depth != 1:
            return False
    return True

def _shaped(r, ops, shape):
    """生成含 ops 个运算符的后序表达式；shape 控制树形：random/left/right/balanced。"""
    def leaf():
        return r.choice(LOWER)
    def build(k):
        if k == 0:
            return leaf()
        if shape == "left":
            lk = k - 1
        elif shape == "right":
            lk = 0
        elif shape == "balanced":
            lk = (k - 1) // 2
        else:
            lk = r.randint(0, k - 1)
        return build(lk) + build(k - 1 - lk) + r.choice(UPPER)
    return build(ops)

def extra_cases():
    cases = []
    # 最小规模：n=1，单个操作数
    cases.append("1\nq\n")
    # 只有一个运算符 / 两个运算符的各种形状
    cases.append("4\nabP\nabcPQ\nabPcQ\nabPcdQR\n")
    shapes = ["left", "right", "balanced", "random"]
    for idx, shape in enumerate(shapes):
        r = random.Random(251400 + idx)
        lines = [_shaped(r, 49, shape) for _ in range(99)]
        cases.append("99\n" + "\n".join(lines) + "\n")
    # 混合长度、混合树形、满 n
    r = random.Random(251499)
    lines = [_shaped(r, r.randint(0, 49), r.choice(shapes)) for _ in range(99)]
    cases.append("99\n" + "\n".join(lines) + "\n")
    return cases

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        extras = extra_cases()  # 第 13..19 组：边界与满规模（catalog 固定 20 组）
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            elif index >= 20 - len(extras):
                content = extras[index - (20 - len(extras))]
                assert content not in seen, index
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(25140 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
