import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n'
SAMPLE_OUT = 'a f c b e d\n'
CASES = ['9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n', '9\na0 b0 $1 c0 d0 $1 e1 f1 $1\n']
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
