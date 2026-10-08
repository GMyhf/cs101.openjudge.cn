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
    reachable = {1}; changed = True
    while changed:
        changed = False
        for left, right in rows:
            for child in (left, right):
                if child != -1 and any(parent + 1 in reachable for parent, row in enumerate(rows) if child in row):
                    changed |= child not in reachable; reachable.add(child)
    assert reachable == set(range(1, n + 1))
    return str(n) + "\n" + "\n".join(f"{a} {b}" for a, b in rows) + "\n"

def valid(text):
    """题面：第 1 行 N（1<=N<=1000）；接下来 N 行，第 i 行是 i 号节点的左、右子节点编号（1~N 或 -1）。
    1 号为根；构成一棵二叉树：除根外每个节点恰有一个父亲，且都能从根到达。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0] != str(int(lines[0])):
        return False
    n = int(lines[0])
    if not 1 <= n <= 1000 or len(lines) != n + 1:
        return False
    kids = []
    parent_cnt = [0] * (n + 1)
    for line in lines[1:]:
        parts = line.split(" ")
        if len(parts) != 2:
            return False
        row = []
        for t in parts:
            if t == "-1":
                row.append(-1); continue
            if not t.isdigit() or t != str(int(t)) or not 1 <= int(t) <= n:
                return False
            row.append(int(t)); parent_cnt[int(t)] += 1
        kids.append(row)
    if parent_cnt[1] != 0 or any(parent_cnt[v] != 1 for v in range(2, n + 1)):
        return False
    seen = {1}; stack = [1]
    while stack:
        u = stack.pop()
        for v in kids[u - 1]:
            if v != -1 and v not in seen:
                seen.add(v); stack.append(v)
    return len(seen) == n


def build(n, edges, r):
    """edges: [(parent, side, child)]，节点按 0..n-1 内部编号，0 为根；再把 1..n-1 随机重编号（根固定为 1）。"""
    perm = list(range(2, n + 1)); r.shuffle(perm)
    lab = [1] + perm
    rows = [[-1, -1] for _ in range(n)]
    for p, side, c in edges:
        assert rows[lab[p] - 1][side] == -1
        rows[lab[p] - 1][side] = lab[c]
    return str(n) + "\n" + "\n".join(f"{a} {b}" for a, b in rows) + "\n"


def extra_case(kind, r):
    n = 1000
    e = []
    if kind == "single":
        return "1\n-1 -1\n"
    if kind == "left":         # 纯左链，深度 1000：右视图就是全部节点
        e = [(i, 0, i + 1) for i in range(n - 1)]
    elif kind == "right":
        e = [(i, 1, i + 1) for i in range(n - 1)]
    elif kind == "zig":
        e = [(i, i % 2, i + 1) for i in range(n - 1)]
    elif kind == "complete":   # 完全二叉树
        e = [((i - 1) // 2, (i - 1) % 2, i) for i in range(1, n)]
    elif kind == "deepleft":   # 根的右子树很浅，左子树很深：只沿右指针走的写法会漏
        e = [(0, 1, 1), (1, 1, 2)]
        prev = 0
        for i in range(3, n):
            e.append((prev, 0, i)); prev = i
    elif kind == "random_shuffled":
        free = [(0, 0), (0, 1)]
        for i in range(1, n):
            j = r.randrange(len(free)); p, side = free[j]; free[j] = free[-1]; free.pop()
            e.append((p, side, i)); free += [(i, 0), (i, 1)]
    elif kind == "deep_random":  # 偏向挂在最新节点上，深而窄、左右随机
        for i in range(1, n):
            p = i - 1 if r.random() < .9 else r.randrange(i)
            used = {s for q, s, _ in e if q == p}
            while len(used) == 2:
                p = r.randrange(i); used = {s for q, s, _ in e if q == p}
            side = r.choice([s for s in (0, 1) if s not in used])
            e.append((p, side, i))
    elif kind == "small_two":
        return build(2, [(0, 0, 1)], r)
    elif kind == "small_right":
        return build(3, [(0, 1, 1), (1, 0, 2)], r)
    return build(n, e, r)


EXTRA = ["single", "small_two", "small_right", "left", "right", "zig", "complete", "deepleft",
         "random_shuffled", "deep_random"]


def main():
    assert SAMPLE_IN == '5\n2 3\n-1 5\n-1 4\n-1 -1\n-1 -1\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        cases = []
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(22485 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            seen.append(content)
            cases.append(content)
        for k, kind in enumerate(EXTRA):
            content = extra_case(kind, random.Random(22485 * 100 + k))
            assert content not in cases, kind
            cases.append(content)
        for index, content in enumerate(cases):
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
