import random
from pathlib import Path

SAMPLE_IN = '3\n2 3\n-1 -1\n-1 -1\n'
SAMPLE_OUT = '2\n'


def solve_text(text):
    it = iter(text.split()); n = int(next(it))
    children = [(int(next(it)), int(next(it))) for _ in range(n)]
    def depth(node):
        if node == -1: return 0
        left, right = children[node - 1]
        return 1 + max(depth(left), depth(right))
    return str(depth(1)) + "\n"


def valid(text):
    """题面：n<=10 个结点，编号 1..n，根为 1；接下来 n 行，每行左右儿子编号，-1 表示没有。
    结构上必须是一棵以 1 为根的二叉树：除根外每个结点恰有一个父亲，且都能从根到达。"""
    try:
        lines = text.split("\n")
        if lines[-1] != "": return False
        lines = lines[:-1]
        if lines[0] != str(int(lines[0])): return False
        n = int(lines[0])
        if not 1 <= n <= 10 or len(lines) != n + 1: return False
        parent = [0] * (n + 1)
        kids = []
        for ln in lines[1:]:
            t = ln.split(" ")
            if len(t) != 2 or any(x != str(int(x)) for x in t): return False
            pair = list(map(int, t))
            for c in pair:
                if c != -1 and not 1 <= c <= n: return False
            kids.append(pair)
        for u, pair in enumerate(kids, 1):
            for c in pair:
                if c == -1: continue
                if c == 1 or parent[c]: return False
                parent[c] = u
        seen, stack = {1}, [1]
        while stack:
            u = stack.pop()
            for c in kids[u - 1]:
                if c != -1 and c not in seen:
                    seen.add(c); stack.append(c)
        return len(seen) == n
    except Exception:
        return False


def build_tree(rng, n, shape="random"):
    """生成一棵 n 结点二叉树；根编号固定为 1，其余结点编号随机打乱。"""
    slots = {}  # 结点(按生成顺序 0..n-1) -> [left, right]
    slots[0] = [-1, -1]
    free = [(0, 0), (0, 1)]
    for v in range(1, n):
        if shape == "left":
            p, s = v - 1, 0
        elif shape == "right":
            p, s = v - 1, 1
        elif shape == "zigzag":
            p, s = v - 1, v % 2
        elif shape == "complete":
            p, s = (v - 1) // 2, (v - 1) % 2
        else:
            p, s = free.pop(rng.randrange(len(free)))
        if shape != "random":
            free.remove((p, s))
        slots[p][s] = v
        slots[v] = [-1, -1]
        free += [(v, 0), (v, 1)]
    label = [1] + rng.sample(range(2, n + 1), n - 1)
    rows = [None] * n
    for v in range(n):
        rows[label[v] - 1] = [label[c] if c != -1 else -1 for c in slots[v]]
    return str(n) + "\n" + "\n".join(f"{l} {r}" for l, r in rows) + "\n"


def generate_cases(rng):
    cases = [SAMPLE_IN]
    fixed = [
        (1, "random"), (2, "left"), (2, "right"),
        (10, "left"), (10, "right"), (10, "zigzag"), (10, "complete"),
        (7, "complete"), (9, "zigzag"),
    ]
    for n, shape in fixed:
        cases.append(build_tree(rng, n, shape))
    while len(cases) < 40:
        n = rng.randint(2, 10)
        c = build_tree(rng, n)
        if c not in cases:
            cases.append(c)
    return cases


def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    rng = random.Random(6646)
    root = Path(__file__).parent / "data"
    cases = generate_cases(rng)
    assert all(valid(c) for c in cases)
    assert len(set(cases)) == len(cases)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 06646")


if __name__ == "__main__":
    main()
