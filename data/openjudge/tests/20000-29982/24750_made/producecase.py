import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '"""\n后序遍历的最后一个元素是树的根节点。然后，在中序遍历序列中，根节点将左右子树分开。\n可以通过这种方法找到左右子树的中序遍历序列。然后，使用递归地处理左右子树来构建整个树。\n"""\ndef build_tree(inorder, postorder):\n    if not inorder or not postorder:\n        return []\n\n    root_val = postorder[-1]\n    root_index = inorder.index(root_val)\n\n    left_inorder = inorder[:root_index]\n    right_inorder = inorder[root_index + 1:]\n\n    left_postorder = postorder[:len(left_inorder)]\n    right_postorder = postorder[len(left_inorder):-1]\n\n    root = [root_val]\n    root.extend(build_tree(left_inorder, left_postorder))\n    root.extend(build_tree(right_inorder, right_postorder))\n\n    return root\n\n\ndef main():\n    inorder = input().strip()\n    postorder = input().strip()\n    preorder = build_tree(inorder, postorder)\n    print(\'\'.join(preorder))\n\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = 'BADC\nBDCA\n'
SAMPLE_OUT = 'ABCD\n'
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
    _, ino, post, pre = _tree_pair(r, 26)
    assert len(ino) <= 26
    return ino + "\n" + post + "\n"


def valid(text):
    """题面：2 行大写字母串，分别为同一棵二叉树的中序、后序序列；字母互不相同，长度不超过 26。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    ino, post = lines
    up = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if not (1 <= len(ino) <= 26) or len(post) != len(ino):
        return False
    if not set(ino) <= up or len(set(ino)) != len(ino) or set(post) != set(ino):
        return False
    # 结构保证：两序列必须对应同一棵二叉树
    def ok(i, p):
        if not i:
            return True
        r = p[-1]
        k = i.index(r)
        if set(i[:k]) != set(p[:k]):
            return False
        return ok(i[:k], p[:k]) and ok(i[k + 1:], p[k:-1])
    return ok(ino, post)


def _shape_case(shape, letters):
    """按给定形状生成整棵树：left/right 链、之字形、完全二叉树。"""
    def chain(chars, side):
        if not chars: return None
        if side == "left": return (chars[0], chain(chars[1:], side), None)
        if side == "right": return (chars[0], None, chain(chars[1:], side))
        nxt = "right" if side == "zl" else "left"
        sub = chain(chars[1:], "zr" if side == "zl" else "zl")
        return (chars[0], sub, None) if side == "zl" else (chars[0], None, sub)
    def complete(chars, i=0):
        if i >= len(chars): return None
        return (chars[i], complete(chars, 2 * i + 1), complete(chars, 2 * i + 2))
    tree = complete(letters) if shape == "complete" else chain(letters, shape)
    def inorder(node): return "" if node is None else inorder(node[1]) + node[0] + inorder(node[2])
    def postorder(node): return "" if node is None else postorder(node[1]) + postorder(node[2]) + node[0]
    return inorder(tree) + "\n" + postorder(tree) + "\n"


def extra_cases():
    r = random.Random(247500)
    letters = lambda k: "".join(r.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k))
    return [
        "Q\nQ\n",
        _shape_case("left", letters(26)),
        _shape_case("right", letters(26)),
        _shape_case("zl", letters(26)),
        _shape_case("complete", letters(26)),
        _shape_case("left", letters(2)),
        _shape_case("right", letters(2)),
        generate_case_n(r, 26),
    ]


def generate_case_n(r, k):
    def build(chars):
        if not chars: return None
        i = r.randrange(len(chars))
        return (chars[i], build(chars[:i]), build(chars[i + 1:]))
    tree = build(r.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k))
    def inorder(node): return "" if node is None else inorder(node[1]) + node[0] + inorder(node[2])
    def postorder(node): return "" if node is None else postorder(node[1]) + postorder(node[2]) + node[0]
    return inorder(tree) + "\n" + postorder(tree) + "\n"


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        extras = extra_cases()
        for index in range(20 + len(extras)):
            if index == 0:
                content = SAMPLE_IN
            elif index >= 20:
                content = extras[index - 20]
                if content in seen: raise AssertionError("duplicate extra case")
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(24750 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
