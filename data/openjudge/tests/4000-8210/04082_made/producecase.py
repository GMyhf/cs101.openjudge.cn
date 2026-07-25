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

def build_cases():
    return [SAMPLE_IN] + [g4082(random.Random(NUMBER + i)) for i in range(1, 20)]

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
