"""5907 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5907
SAMPLE_IN = '2\n5 5\n0 1 2\n1 -1 -1\n2 3 4\n3 -1 -1\n4 -1 -1\n2 0\n1 1 2\n2 0\n1 3 4\n2 2\n3 2\n0 1 2\n1 -1 -1\n2 -1 -1\n1 1 2\n2 0\n'
SAMPLE_OUT = '1\n3\n4\n2\n'
REFERENCE_SOURCE = '# 数学科学学院 王镜廷 2300010724\ndef find_leftmost_node(son, u):\n    while son[u][0] != -1:\n        u = son[u][0]\n    return u\n\ndef main():\n    t = int(input())\n    for _ in range(t):\n        n, m = map(int, input().split())\n\n        son = [-1] * (n + 1)  # 存储每个节点的子节点\n        parent = {}  # 存储每个节点的父节点和方向，{节点: (父节点, 方向)}\n\n        for _ in range(n):\n            i, u, v = map(int, input().split())\n            son[i] = [u, v]\n            parent[u] = (i, 0)  # 左子节点\n            parent[v] = (i, 1)  # 右子节点\n\n        for _ in range(m):\n            s = input().split()\n            if s[0] == "1":\n                u, v = map(int, s[1:])\n                fu, diru = parent[u]\n                fv, dirv = parent[v]\n                son[fu][diru] = v\n                son[fv][dirv] = u\n                parent[v] = (fu, diru)\n                parent[u] = (fv, dirv)\n            elif s[0] == "2":\n                u = int(s[1])\n                root = find_leftmost_node(son, u)\n                print(root)\n\nif __name__ == "__main__":\n    main()\n'

def g5907(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        n = r.randint(3, 10); m = r.randint(2, 10)
        children = [[-1, -1] for _ in range(n)]
        leaves = list(range(n))
        for i in range(1, n):
            parent = (i - 1) // 2
            children[parent][i % 2] = i
        ops = []
        leaf_ids = [i for i, pair in enumerate(children) if pair == [-1, -1]]
        for _ in range(m):
            if len(leaf_ids) >= 2 and r.random() < .45:
                a, b = r.sample(leaf_ids, 2); ops.append(f"1 {a} {b}")
            else:
                ops.append(f"2 {r.randrange(n)}")
        lines = [f"{n} {m}"] + [f"{i} {a} {b}" for i, (a, b) in enumerate(children)] + ops
        cases.append("\n".join(lines))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"

# 题面：t <= 100；每组 n m（1<=n<=100，m<=100），n 行 "X Y Z"（节点标识 0..n-1，-1 为空，根恒为 0），
# m 行操作 "1 x y"（保证 x、y 不是祖先关系）或 "2 x"。
def parse_tree(lines, n):
    """返回 (son, parent) 或 None。"""
    son = {}
    for ln in lines:
        toks = ln.split(" ")
        if len(toks) != 3:
            return None
        try:
            x, y, z = map(int, toks)
        except ValueError:
            return None
        if any(str(v) != tok for v, tok in zip((x, y, z), toks)):
            return None
        if not 0 <= x < n or x in son or not all(-1 <= c < n for c in (y, z)):
            return None
        son[x] = [y, z]
    parent = {}
    for x, (y, z) in son.items():
        for d, c in enumerate((y, z)):
            if c == -1:
                continue
            if c == 0 or c in parent:
                return None
            parent[c] = (x, d)
    if len(parent) != n - 1:
        return None
    seen = set(); stack = [0]
    while stack:
        u = stack.pop(); seen.add(u)
        stack += [c for c in son[u] if c != -1]
    return (son, parent) if len(seen) == n else None


def is_ancestor(parent, a, b):
    while True:
        if a == b:
            return True
        if b not in parent:
            return False
        b = parent[b][0]


def valid(text):
    if not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or str(int(lines[0])) != lines[0]:
        return False
    t = int(lines[0]); i = 1
    if not 1 <= t <= 100:
        return False
    for _ in range(t):
        if i >= len(lines):
            return False
        hd = lines[i].split(" ")
        if len(hd) != 2 or not all(h.isdigit() and str(int(h)) == h for h in hd):
            return False
        n, m = map(int, hd); i += 1
        if not (1 <= n <= 100 and 0 <= m <= 100) or i + n + m > len(lines):
            return False
        tr = parse_tree(lines[i:i + n], n)
        if tr is None:
            return False
        son, parent = tr; i += n
        for ln in lines[i:i + m]:
            toks = ln.split(" ")
            if not all(x.isdigit() and str(int(x)) == x for x in toks):
                return False
            v = list(map(int, toks))
            if v[0] == 1 and len(v) == 3 and all(0 <= x < n for x in v[1:]):
                a, b = v[1], v[2]
                if is_ancestor(parent, a, b) or is_ancestor(parent, b, a):
                    return False
                fa, da = parent[a]; fb, db = parent[b]
                son[fa][da] = b; son[fb][db] = a
                parent[a], parent[b] = (fb, db), (fa, da)
            elif v[0] == 2 and len(v) == 2 and 0 <= v[1] < n:
                pass
            else:
                return False
        i += m
    return i == len(lines)


def make_tree(r, n, shape):
    """返回 children 列表（按标识），根为 0，其余标识随机打乱。"""
    pos = [[-1, -1] for _ in range(n)]       # 先按位置 0..n-1 建树，位置 0 为根
    for i in range(1, n):
        if shape == "left":
            pos[i - 1][0] = i
        elif shape == "right":
            pos[i - 1][1] = i
        elif shape == "zig":
            pos[i - 1][i % 2] = i
        elif shape == "full":
            pos[(i - 1) // 2][(i - 1) % 2] = i
        else:
            while True:
                p = r.randrange(i) if shape == "rand" else r.randint(max(0, i - 3), i - 1)
                free = [d for d in (0, 1) if pos[p][d] == -1]
                if free:
                    pos[p][r.choice(free)] = i
                    break
    label = [0] + r.sample(range(1, n), n - 1)
    son = [None] * n
    for i in range(n):
        son[label[i]] = [label[c] if c != -1 else -1 for c in pos[i]]
    return son


def tree_group(r, n, m, shape, swap_p):
    son = make_tree(r, n, shape)
    parent = {}
    for x in range(n):
        for d, c in enumerate(son[x]):
            if c != -1:
                parent[c] = (x, d)
    lines = [f"{n} {m}"]
    order = list(range(n)); r.shuffle(order)
    if r.random() < 0.5:
        order = list(range(n))
    lines += [f"{x} {son[x][0]} {son[x][1]}" for x in order]
    for _ in range(m):
        done = False
        if n >= 3 and r.random() < swap_p:
            for _ in range(50):
                a, b = r.sample(range(1, n), 2)
                if not is_ancestor(parent, a, b) and not is_ancestor(parent, b, a):
                    fa, da = parent[a]; fb, db = parent[b]
                    son[fa][da] = b; son[fb][db] = a
                    parent[a], parent[b] = (fb, db), (fa, da)
                    lines.append(f"1 {a} {b}"); done = True
                    break
        if not done:
            lines.append(f"2 {r.choice([0, r.randrange(n)])}")
    return "\n".join(lines)


def g5907_hard(r, kind):
    groups = []
    if kind == "min":
        groups = [tree_group(r, 1, 1, "rand", 0), tree_group(r, 1, 0, "rand", 0), tree_group(r, 2, 3, "rand", 0)]
    elif kind == "max":
        groups = [tree_group(r, 100, 100, r.choice(["rand", "full", "cat", "left", "zig"]), r.choice([0.3, 0.5, 0.7]))
                  for _ in range(100)]
    else:
        for _ in range(r.randint(1, 30)):
            n = r.choice([r.randint(1, 10), r.randint(1, 100), 100])
            groups.append(tree_group(r, n, r.randint(0, 100), r.choice(["rand", "full", "cat", "left", "right", "zig"]),
                                     r.choice([0.2, 0.5, 0.8])))
    return str(len(groups)) + "\n" + "\n".join(groups) + "\n"


def build_cases():
    kinds = ["min", "max", "max", "max"] + ["mix"] * 16
    return build_cases_base() + [g5907_hard(random.Random(NUMBER * 100 + i), k) for i, k in enumerate(kinds)]


def build_cases_base():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g5907(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases

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
