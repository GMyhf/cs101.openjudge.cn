import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "from collections import deque\n\ndef right_view(n, tree):\n    queue = deque([(1, tree[1])])  # start with root node\n    right_view = []\n\n    while queue:\n        level_size = len(queue)\n        for i in range(level_size):\n            node, children = queue.popleft()\n            if children[0] != -1:\n                queue.append((children[0], tree[children[0]]))\n            if children[1] != -1:\n                queue.append((children[1], tree[children[1]]))\n        right_view.append(node)\n\n    return right_view\n\nn = int(input())\ntree = {1: [-1, -1] for _ in range(n+1)}  # initialize tree with -1s\nfor i in range(1, n+1):\n    left, right = map(int, input().split())\n    tree[i] = [left, right]\n\nresult = right_view(n, tree)\nprint(' '.join(map(str, result)))\n"
SAMPLE_IN = '5\n2 3\n-1 5\n-1 4\n-1 -1\n-1 -1\n'
SAMPLE_OUT = '1 3 4\n'
def generate_case(r):
    n = 1000 if r.random() < .15 else r.randint(1, 60)               # 题面：1<=N<=1000
    rows = [[-1, -1] for _ in range(n)]
    for i in range(1, n):
        p = r.choice([k for k in range(i) if -1 in rows[k]])          # 只挑还有空位的父节点
        side = r.choice([k for k in (0, 1) if rows[p][k] == -1])      # 左右都可能，覆盖「只有右子」
        rows[p][side] = i + 1
    return str(n) + "\n" + "\n".join(f"{a} {b}" for a, b in rows) + "\n"

assert SAMPLE_IN == '5\n2 3\n-1 5\n-1 4\n-1 -1\n-1 -1\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(22485 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
