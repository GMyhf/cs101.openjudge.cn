import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "from collections import deque\n\nclass Node:\n    def __init__(self, data):\n        self.data = data\n        self.left = None\n        self.right = None\n\ndef build_tree(inorder, postorder):\n    if inorder:\n        root = Node(postorder.pop())\n        root_index = inorder.index(root.data)\n        root.right = build_tree(inorder[root_index+1:], postorder)\n        root.left = build_tree(inorder[:root_index], postorder)\n        return root\n\ndef level_order_traversal(root):\n    if root is None:\n        return []\n    result = []\n    queue = deque([root])\n    while queue:\n        node = queue.popleft()\n        result.append(node.data)\n        if node.left:\n            queue.append(node.left)\n        if node.right:\n            queue.append(node.right)\n    return result\n\nn = int(input())\nfor _ in range(n):\n    inorder = list(input().strip())\n    postorder = list(input().strip())\n    root = build_tree(inorder, postorder)\n    print(''.join(level_order_traversal(root)))\n"
SAMPLE_IN = '2\nLZGD\nLGDZ\nBKTVQP\nTPQVKB\n'
SAMPLE_OUT = 'ZLDG\nBKVTQP\n'
def _tree_pair(r, max_size=20):
    def build(chars):
        if not chars: return None
        i = r.randrange(len(chars))
        return (chars[i], build(chars[:i]), build(chars[i + 1:]))
    chars = r.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", r.randint(2, max_size)); tree = build(chars)
    def inorder(node): return "" if node is None else inorder(node[1]) + node[0] + inorder(node[2])
    def postorder(node): return "" if node is None else postorder(node[1]) + postorder(node[2]) + node[0]
    def preorder(node): return "" if node is None else node[0] + preorder(node[1]) + preorder(node[2])
    ino, post, pre = inorder(tree), postorder(tree), preorder(tree)
    assert len(ino) == len(post) == len(pre) and sorted(ino) == sorted(post) == sorted(pre)
    return tree, ino, post, pre

def generate_case(r):
    pairs = [_tree_pair(r, 26)[1:3] for _ in range(r.randint(2, 8))]
    assert all(len(ino) <= 26 for ino, _ in pairs)
    return str(len(pairs)) + "\n" + "\n".join(f"{ino}\n{post}" for ino, post in pairs) + "\n"

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def _consistent(ino, post):
    """中序/后序能否对应同一棵二叉树。"""
    stack = [(0, len(ino), 0, len(post))]
    pos = {c: i for i, c in enumerate(ino)}
    while stack:
        a, b, c, d = stack.pop()
        if b - a != d - c:
            return False
        if a == b:
            continue
        root = post[d - 1]
        k = pos.get(root)
        if k is None or not a <= k < b:
            return False
        left = k - a
        stack.append((a, k, c, c + left))
        stack.append((k + 1, b, c + left, d - 1))
    return True

def valid(text):
    """题面契约：第一行整数 n (n<=30)；之后每棵树两行：中序序列、后序序列；
    结点为互不重复的大写字母，两行须是同一棵二叉树的遍历。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines or not lines[0].isdigit() or lines[0] != str(int(lines[0])):
        return False
    n = int(lines[0])
    if not 1 <= n <= 30 or len(lines) != 2 * n + 1:
        return False
    for i in range(n):
        ino, post = lines[1 + 2 * i], lines[2 + 2 * i]
        if not ino or any(ch not in LETTERS for ch in ino + post):
            return False
        if len(set(ino)) != len(ino) or sorted(ino) != sorted(post):
            return False
        if not _consistent(ino, post):
            return False
    return True

def _orders(tree):
    def inorder(node): return "" if node is None else inorder(node[1]) + node[0] + inorder(node[2])
    def postorder(node): return "" if node is None else postorder(node[1]) + postorder(node[2]) + node[0]
    return inorder(tree), postorder(tree)

def _shaped_tree(r, size, shape):
    chars = r.sample(LETTERS, size)
    def build(cs):
        if not cs: return None
        if shape == "left": return (cs[0], build(cs[1:]), None)
        if shape == "right": return (cs[0], None, build(cs[1:]))
        if shape == "zigzag":
            return (cs[0], build(cs[1:]), None) if len(cs) % 2 else (cs[0], None, build(cs[1:]))
        if shape == "complete":
            # 用堆下标建完全二叉树
            def h(i): return None if i >= len(cs) else (cs[i], h(2 * i + 1), h(2 * i + 2))
            return h(0)
        i = r.randrange(len(cs))
        return (cs[i], build(cs[:i]), build(cs[i + 1:]))
    return _orders(build(chars))

def extra_cases():
    cases = []
    cases.append("1\nQ\nQ\n")  # 最小：单结点
    r = random.Random(251450)
    pairs = [_shaped_tree(r, 26, "random") for _ in range(30)]  # n=30，每棵 26 结点
    cases.append("30\n" + "\n".join(f"{a}\n{b}" for a, b in pairs) + "\n")
    for idx, shape in enumerate(["left", "right", "zigzag", "complete"]):
        r = random.Random(251451 + idx)
        pairs = [_shaped_tree(r, r.randint(1, 26), shape) for _ in range(30)]
        cases.append("30\n" + "\n".join(f"{a}\n{b}" for a, b in pairs) + "\n")
    r = random.Random(251459)
    pairs = [_shaped_tree(r, r.randint(1, 3), "random") for _ in range(30)]
    cases.append("30\n" + "\n".join(f"{a}\n{b}" for a, b in pairs) + "\n")
    return cases

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        extras = extra_cases()  # 末尾若干组：边界与满规模（catalog 固定 20 组）
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            elif index >= 20 - len(extras):
                content = extras[index - (20 - len(extras))]
                assert content not in seen, index
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(25145 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
