import random
import sys
from pathlib import Path

# 原生成器把 1..n 的随机排列直接当作前序序列，绝大多数不是任何二叉搜索树的前序遍历（越出题面），且 n<=80。
# 现改为：随机构造 1..n 上的二叉搜索树再取前序；覆盖 n=1、链状（深度 2000）、满规模 n=2000。
sys.setrecursionlimit(10000)


def solve_text(text):
    values = list(map(int, text.split())); preorder = values[1:]; postorder = []
    def visit(sequence):
        if not sequence: return
        root = sequence[0]; cut = 1
        while cut < len(sequence) and sequence[cut] < root: cut += 1
        visit(sequence[1:cut]); visit(sequence[cut:]); postorder.append(str(root))
    visit(preorder)
    return " ".join(postorder) + "\n"


def valid(text):
    """题面：首行正整数 n（n<=2000）；第二行 n 个正整数，1~n 各出现一次，且是一棵二叉搜索树的前序遍历。"""
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    if len(lines) != 2 or not lines[0].isdigit(): return False
    n = int(lines[0])
    if not 1 <= n <= 2000: return False
    t = lines[1].split(" ")
    if len(t) != n or not all(x.isdigit() for x in t): return False
    a = list(map(int, t))
    if sorted(a) != list(range(1, n + 1)): return False
    low, st = 0, []          # 单调栈判定是否为 BST 前序
    for x in a:
        if x < low: return False
        while st and st[-1] < x: low = st.pop()
        st.append(x)
    return True


def preorder_of(n, shape, rng):
    """在键 1..n 上构造 BST，返回前序序列。"""
    out = []
    def build(lo, hi):                # 迭代，避免深递归
        stack = [(lo, hi)]
        while stack:
            lo, hi = stack.pop()
            if lo > hi: continue
            if shape == "random": k = rng.randint(lo, hi)
            elif shape == "balanced": k = (lo + hi) // 2
            elif shape == "left": k = hi
            elif shape == "right": k = lo
            elif shape == "zigzag": k = hi if (hi - lo) % 2 else lo
            elif shape == "skewed": k = lo + int((hi - lo) * rng.random() ** 0.15) if rng.random() < 0.5 else hi - int((hi - lo) * rng.random() ** 0.15)
            out.append(k)
            stack.append((k + 1, hi)); stack.append((lo, k - 1))
    build(1, n)
    return out


def case(seq):
    return f"{len(seq)}\n" + " ".join(map(str, seq)) + "\n"


def insertion_bst(n, rng):
    """按随机插入顺序建 BST（形状分布与随机排列插入一致）。"""
    order = list(range(1, n + 1)); rng.shuffle(order)
    left, right = {}, {}; root = order[0]
    for x in order[1:]:
        cur = root
        while True:
            side = left if x < cur else right
            if cur in side: cur = side[cur]
            else: side[cur] = x; break
    out, st = [], [root]
    while st:
        v = st.pop(); out.append(v)
        if v in right: st.append(right[v])
        if v in left: st.append(left[v])
    return out


SAMPLE_IN = '5\n4 2 1 3 5\n'
SAMPLE_OUT = '1 3 2 5 4\n'


def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
    rng = random.Random(22275)
    cases = [SAMPLE_IN, case([1]), case([1, 2]), case([2, 1])]
    for n, shape in [(2000, "left"), (2000, "right"), (2000, "zigzag"), (2000, "balanced"),
                     (2000, "skewed"), (1999, "skewed"), (7, "zigzag"), (15, "balanced")]:
        cases.append(case(preorder_of(n, shape, rng)))
    for n in [2000, 2000, 2000, 1500, 1000, 500, 100, 30, 10, 3]:
        cases.append(case(insertion_bst(n, rng)))
    for n in [2000, 1234, 64, 5]:
        cases.append(case(preorder_of(n, "random", rng)))
    assert len(set(cases)) == len(cases) and all(valid(c) for c in cases)
    root = Path(__file__).parent / "data"
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 22275")


if __name__ == "__main__":
    main()
