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

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(24750 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
