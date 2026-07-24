import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n'
SAMPLE_OUT = 'a f c b e d\n'
CASES = ['9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '17\na0 b0 $1 c0 h0 $1 k1 d0 e0 l1 f0 g0 i1 j1 $1 $1 $1\n', '21\na0 b0 e0 l1 $1 c0 d0 f0 i0 $1 j1 h0 n1 m1 g0 $1 k0 o1 $1 $1 $1\n', '15\na0 b0 c0 $1 d0 g0 j1 $1 $1 e0 f1 h0 $1 i1 $1\n', '9\na0 b0 c0 $1 d0 $1 e1 $1 $1\n', '13\na0 b0 c0 $1 f0 g0 $1 h1 $1 d0 e1 $1 $1\n', '7\na0 b0 c0 d1 $1 $1 $1\n', '9\na0 b0 c0 g1 d0 $1 e1 f1 $1\n', '21\na0 b0 $1 c0 e0 f0 g0 k0 l1 $1 $1 $1 $1 d0 h0 i0 j1 $1 $1 $1 $1\n', '17\na0 b0 c0 d0 g0 h0 $1 j1 $1 k1 $1 e0 f0 $1 i1 $1 $1\n', '19\na0 b0 e0 k0 l0 $1 m1 $1 $1 c0 g0 h1 i0 j1 $1 d0 f1 $1 $1\n', '19\na0 b0 e1 c0 m0 $1 n1 d0 f0 $1 g1 h0 i0 $1 j0 l1 k1 o1 $1\n', '11\na0 b0 c0 d0 $1 g1 e0 f1 $1 h1 $1\n', '19\na0 b0 c0 g0 $1 k1 d0 $1 e0 f0 $1 h0 i0 j1 $1 $1 $1 $1 $1\n', '21\na0 b0 c0 $1 d0 j1 e0 h0 $1 k0 $1 m0 $1 n1 f0 i1 $1 g0 $1 l1 $1\n', '11\na0 b0 $1 c0 d0 e0 $1 f1 $1 g1 $1\n', '15\na0 b0 k1 c0 d0 e0 g0 i1 $1 h0 j1 $1 $1 f1 $1\n', '13\na0 b0 d0 e0 $1 g1 f0 h1 i1 c0 j1 $1 $1\n', '19\na0 b0 h0 $1 l1 c0 d0 $1 e0 $1 f0 g0 i1 k1 $1 j0 m1 $1 $1\n', '23\na0 b0 d0 $1 f0 i1 g0 k0 p1 $1 h0 m0 n1 $1 j1 c0 $1 e0 $1 l0 $1 o1 $1\n']
REFERENCE_SOURCE = "from collections import defaultdict\n\nn = int(input())\nif n == 0:\n    print()\n    exit()\n\npreorder = input().split()\n\n# 初始化根节点\nroot = preorder[0][0]\nroot_type = preorder[0][1]\n\ntier = defaultdict(list)\ntier[0].append(root)\n\nnodes = [root]\nlevel = 0\ntypes = {root: root_type}\n\nfor i in range(1, n):\n    current = preorder[i]\n    name = current[0]\n    typ = current[1]\n    types[name] = typ\n\n    prev_node = nodes[-1]\n    prev_type = types[prev_node]\n\n    # 计算层级变化\n    if prev_type == '1':\n        level -= 1\n    else:\n        level += 1\n\n    nodes.append(name)\n\n    # 只添加非虚节点到对应层级\n    if name != '$':\n        tier[level].append(name)\n\n# 按层级顺序排序并逆序每层节点\nsorted_levels = sorted(tier.items(), key=lambda x: x[0])\nresult = []\nfor level, chars in sorted_levels:\n    result.extend(reversed(chars))\n\nprint(' '.join(result))\n"
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(4082)
assert CASES[0] == SAMPLE_IN
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
def generate_case(index):
    return CASES[index]
root = Path(__file__).parent / "data"
for index in range(20):
    content = generate_case(index)
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
