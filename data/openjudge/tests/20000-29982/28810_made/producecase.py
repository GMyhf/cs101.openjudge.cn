import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'class TreeNode:\n    def __init__(self, val):\n        self.val = val\n        self.left = None\n        self.right = None\n\ndef insert(root, val):\n    if not root:\n        return TreeNode(val)\n    if val < root.val:\n        root.left = insert(root.left, val)\n    else:\n        root.right = insert(root.right, val)\n    return root\n\ndef build_bst(sequence):\n    root = None\n    for num in sequence:\n        root = insert(root, num)\n    return root\n\ndef is_same_tree(t1, t2):\n    if not t1 and not t2:\n        return True\n    if not t1 or not t2:\n        return False\n    if t1.val != t2.val:\n        return False\n    return is_same_tree(t1.left, t2.left) and is_same_tree(t1.right, t2.right)\n\n# 主程序\ndef main():\n    while True:\n        try:\n            N, L = map(int, input().split())\n            if N == 0:\n                break\n            base_seq = list(map(int, input().split()))\n            base_tree = build_bst(base_seq)\n\n            for _ in range(L):\n                check_seq = list(map(int, input().split()))\n                check_tree = build_bst(check_seq)\n                print("Yes" if is_same_tree(base_tree, check_tree) else "No")\n        except EOFError:\n            break\n\n# 示例输入运行\nif __name__ == "__main__":\n    main()\n\n'
SAMPLE_IN = '4 2\n3 1 4 2\n3 4 1 2\n3 2 4 1\n'
SAMPLE_OUT = 'Yes\nNo\n'
def generate_case(r):
    n = r.randint(2, 8); base = r.sample(range(1, 100), n); queries = []
    for _ in range(r.randint(2, 7)):
        q = base[:]; r.shuffle(q); queries.append(q)
    return f"{n} {len(queries)}\n" + " ".join(map(str, base)) + "\n" + "\n".join(" ".join(map(str, q)) for q in queries) + "\n"


def valid(text):
    """题面契约：首行正整数 N（≤10）与正整数 L；第二行 N 个正整数；其后恰 L 行，每行 N 个正整数。
    （题面未写 L 上界、未明说各序列为同一组元素的排列，这里不作额外要求。）"""
    if not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    def ints(line):
        parts = line.split(" ")
        if any(not p.isdigit() or p[0] == "0" for p in parts):
            return None
        return [int(p) for p in parts]
    first = ints(lines[0])
    if first is None or len(first) != 2:
        return False
    n, l = first
    if not 1 <= n <= 10 or l < 1 or len(lines) != l + 2:
        return False
    return all((row := ints(line)) is not None and len(row) == n for line in lines[1:])


def fmt(base, queries):
    return f"{len(base)} {len(queries)}\n" + " ".join(map(str, base)) + "\n" + "\n".join(" ".join(map(str, q)) for q in queries) + "\n"


def same_tree_order(r, base):
    """随机生成一个与 base 建出同一棵 BST 的插入序列（树的随机拓扑序：父先于子）。"""
    children = {}
    root = base[0]
    for v in base[1:]:
        cur = root
        while True:
            side = 0 if v < cur else 1
            nxt = children.get((cur, side))
            if nxt is None:
                children[(cur, side)] = v
                break
            cur = nxt
    order, frontier = [], [root]
    while frontier:
        v = frontier.pop(r.randrange(len(frontier)))
        order.append(v)
        for side in (0, 1):
            if (v, side) in children:
                frontier.append(children[(v, side)])
    return order


def mixed_queries(r, base, count):
    queries = []
    for _ in range(count):
        kind = r.random()
        q = same_tree_order(r, base)
        if kind < 0.45:
            pass                                        # Yes
        elif kind < 0.8 and len(q) >= 3:
            i, j = sorted(r.sample(range(1, len(q)), 2))  # 只交换非根的两个元素：常变成 No 的近似序列
            q[i], q[j] = q[j], q[i]
        else:
            r.shuffle(q)
        queries.append(q)
    return queries


def extra_cases():
    r = random.Random(288100)
    out = []
    out.append(fmt([5], [[5], [5]]))                                   # N=1
    out.append(fmt([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6, 7, 8, 10, 9]]))  # 链
    out.append(fmt([2, 1], [[2, 1], [1, 2]]))
    for _ in range(7):
        n = r.choice([9, 10, 10, 10])
        base = r.sample(range(1, 1000), n)
        out.append(fmt(base, mixed_queries(r, base, r.randint(20, 200))))
    # 根相同、左右子树元素集合相同但结构不同，只比较根或先序集合会错
    base = [50, 30, 70, 20, 40, 60, 80, 10, 90, 35]
    out.append(fmt(base, mixed_queries(r, base, 100) + [[50, 30, 20, 40, 10, 35, 70, 60, 80, 90], [50, 70, 30, 40, 20, 35, 10, 80, 90, 60], [50, 40, 30, 20, 10, 35, 70, 80, 90, 60]]))
    return out


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0: content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(28810 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        for index, content in enumerate(extra_cases(), start=20):
            assert content not in seen, index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        assert (root / "0.out").read_text(encoding="utf-8") == SAMPLE_OUT
        for index in range(len(seen) - 1):
            assert valid((root / f"{index}.in").read_text(encoding="utf-8")), index


if __name__ == "__main__":
    main()
