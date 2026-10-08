import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "class TreeNode:\n    def __init__(self, value):\n        self.value = value\n        self.left = None\n        self.right = None\n\ndef build_tree(preorder, inorder):\n    if not preorder or not inorder:\n        return None\n    root_value = preorder[0]\n    root = TreeNode(root_value)\n    root_index_inorder = inorder.index(root_value)\n    root.left = build_tree(preorder[1:1+root_index_inorder], inorder[:root_index_inorder])\n    root.right = build_tree(preorder[1+root_index_inorder:], inorder[root_index_inorder+1:])\n    return root\n\ndef postorder_traversal(root):\n    if root is None:\n        return ''\n    return postorder_traversal(root.left) + postorder_traversal(root.right) + root.value\n\nwhile True:\n    try:\n        preorder = input().strip()\n        inorder = input().strip()\n        root = build_tree(preorder, inorder)\n        print(postorder_traversal(root))\n    except EOFError:\n        break\n"
SAMPLE_IN = 'DURPA\nRUDPA\nXTCNB\nCTBNX\n'
SAMPLE_OUT = 'RUAPD\nCBNTX\n'
def generate_case(r):
    def build(seq):
        if not seq: return None
        i = r.randrange(len(seq))
        return (seq[i], build(seq[:i]), build(seq[i + 1:]))

    def preorder(node):
        return "" if node is None else node[0] + preorder(node[1]) + preorder(node[2])

    out = []
    for _ in range(r.randint(2, 4)):
        size = 26 if r.random() < .25 else r.randint(2, 26)          # 题面：长度均不超过 26
        chars = r.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", size)
        tree = build(chars); pre = preorder(tree); ino = "".join(chars)
        def inorder(node):
            return "" if node is None else inorder(node[1]) + node[0] + inorder(node[2])
        assert inorder(tree) == ino and sorted(pre) == sorted(ino) and len(set(pre)) == size
        out.extend([pre, ino])
    return "\n".join(out) + "\n"

UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def valid(text):
    """题面：多组数据，每组两行：前序、中序遍历序列；节点为互不相同的大写字母，长度不超过 26；两序列须对应同一棵二叉树。"""
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    if not lines or len(lines) % 2: return False
    def ok(pre, ino):
        if not pre: return True
        k = ino.find(pre[0])
        return k >= 0 and ok(pre[1:k + 1], ino[:k]) and ok(pre[k + 1:], ino[k + 1:])
    for pre, ino in zip(lines[::2], lines[1::2]):
        if not (1 <= len(pre) <= 26 and len(ino) == len(pre)): return False
        if not all(c in UPPER for c in pre + ino) or len(set(pre)) != len(pre) or set(pre) != set(ino): return False
        if not ok(pre, ino): return False
    return True

def extra_cases():
    """补充：单节点树、左链、右链、之字形、满 26 节点多组（追加在原 20 组之后）。"""
    r = random.Random(221580); out = []
    def pre_of(node): return "" if node is None else node[0] + pre_of(node[1]) + pre_of(node[2])
    def in_of(node): return "" if node is None else in_of(node[1]) + node[0] + in_of(node[2])
    def chain(chars, mode):
        node = None
        for i, c in enumerate(chars):
            side = mode if mode in "LR" else ("L" if i % 2 else "R") if mode == "Z" else r.choice("LR")
            node = (c, node, None) if side == "L" else (c, None, node)
        return node
    def rand_tree(chars):
        if not chars: return None
        i = r.randrange(len(chars)); return (chars[i], rand_tree(chars[:i]), rand_tree(chars[i + 1:]))
    def pair(t): return [pre_of(t), in_of(t)]
    L = []
    for c in r.sample(UPPER, 5): L += [c, c]
    out.append("\n".join(L) + "\n")
    for mode in "LRZ":
        L = []
        for size in (26, 26, 13, 2):
            L += pair(chain(r.sample(UPPER, size), mode))
        out.append("\n".join(L) + "\n")
    L = []
    for _ in range(30): L += pair(chain(r.sample(UPPER, 26), "X"))   # 随机链（每层随机左右）
    out.append("\n".join(L) + "\n")
    for _ in range(3):
        L = []
        for _ in range(100): L += pair(rand_tree(r.sample(UPPER, r.choice([1, 2, 3, 26, 26, r.randint(1, 26)]))))
        out.append("\n".join(L) + "\n")
    return out

def main():
    assert SAMPLE_IN == 'DURPA\nRUDPA\nXTCNB\nCTBNX\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(22158 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        for index, content in enumerate(extra_cases(), start=20):
            assert valid(content) and content not in seen
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=30, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
    assert all(valid(c) for c in seen)

if __name__ == "__main__":
    main()
