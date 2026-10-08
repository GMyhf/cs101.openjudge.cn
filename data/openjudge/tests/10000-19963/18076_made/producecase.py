"""18076 链状基团大小判定 测试数据生成器（固定种子，可复现）。

题面规则有几处说不清：不饱和键复制出来的原子怎么往下走、「最大的一个支链」
并列时选哪个、两个基团完全相同输出什么、原子的化合价没有给出。生成器全部绕开：
  * 除题面两组样例外，只生成「饱和」的基团：全部单键，每个原子的邻居数
    （含父原子；根原子的父是手性碳）恰好等于常见化合价
    H/F/Cl/Br/I=1，O=2，N=3，C/Si=4，规则 (0) 永远不触发；
    不用 P、S：它们的化合价有多种（P 3/5，S 2/4/6），按别的化合价理解会被
    规则 (0) 当成不饱和原子；
  * 对每组输入用 5 种理解方式（按完整比较选最大支链 / 原子序数并列时取序号最小的 /
    取序号最大的 / 所有支链按大小依次深入比较 / 按层把同一层全部原子从大到小比较）
    分别算答案，只保留 5 种都给出同一个确定答案（1 或 2）的输入，相同基团直接丢弃。
深层数据用「主链」构造：C/Si 主链上，下一个主链原子的原子序数严格大于同层其他支链首原子，
最大支链唯一；第二个基团是同一结构在主链深处改一处（H 换卤素/甲基，或主链提前截断），
于是要一路比到几十到近 300 层才分出大小，n、m 最大到九百多。
第 0、1 组是题面两组样例（答案按题面给的 2、2 断言）。
samplecode.py 是第一种理解的实现，生成时逐组比对。
"""
import random
import subprocess
import sys
from collections import deque
from pathlib import Path

SEED = 18076
CASES = 40
SAMPLES = [
    ("4 4\n0 -1 6 1\n1 0 1 1\n2 0 1 1\n3 0 1 1\n0 -1 6 1\n1 0 1 1\n2 0 1 1\n3 0 9 1\n", "2\n"),
    ("7 5\n0 -1 6 1\n1 0 6 1\n2 0 1 1\n3 0 1 1\n4 1 1 1\n5 1 1 1\n6 1 1 1\n"
     "0 -1 6 1\n1 0 6 2\n2 0 1 1\n3 1 1 1\n4 1 1 1\n", "2\n"),
]
VALENCE = {1: 1, 9: 1, 17: 1, 35: 1, 53: 1, 8: 2, 16: 2, 7: 3, 15: 3, 6: 4, 14: 4}
HEAVY = [6] * 12 + [7] * 2 + [8] * 2 + [14]  # 不含化合价多变的 P、S
TERMINAL = [1] * 14 + [9, 17, 35, 53]


def valid(text):
    """严格核输入：首行 n m（1≤n,m<1000），随后 n 行、m 行各一个基团，
    每行 4 个整数：序号依次 0..n-1；0 号父为 -1，其余父序号在 0..序号-1；
    原子序数 1..118；键级 1..3。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def ints(line):
        try:
            v = [int(p) for p in line.split(" ")]
        except ValueError:
            return None
        return v if " ".join(map(str, v)) == line else None
    head = ints(lines[0])
    if head is None or len(head) != 2:
        return False
    n, m = head
    if not (1 <= n < 1000 and 1 <= m < 1000) or len(lines) != 1 + n + m:
        return False
    pos = 1
    for size in (n, m):
        for i in range(size):
            v = ints(lines[pos])
            pos += 1
            if v is None or len(v) != 4 or v[0] != i:
                return False
            if (i == 0 and v[1] != -1) or (i > 0 and not 0 <= v[1] < i):
                return False
            if not (1 <= v[2] <= 118 and 1 <= v[3] <= 3):
                return False
    return True


# ---------- 解析与 5 种理解 ----------
def parse(text):
    v = list(map(int, text.split()))
    n, m = v[0], v[1]
    rows = [v[2 + 4 * i: 6 + 4 * i] for i in range(n + m)]
    groups = []
    for part in (rows[:n], rows[n:]):
        z = [r[2] for r in part]
        kids = [[] for _ in part]
        for r in part[1:]:
            kids[r[1]].append(r[0])
        groups.append((z, kids))
    return groups


def keys(g):
    """key(x) = (z_x, 子原子序数从大到小补 0 到 3 个, 最大支链的 key 去掉首项...)。"""
    z, kids = g
    key = [None] * len(z)
    for x in range(len(z) - 1, -1, -1):
        ks = sorted((z[c] for c in kids[x]), reverse=True)
        ks += [0] * (3 - len(ks))
        tail = max((key[c] for c in kids[x]), default=(0, 0, 0, 0))[1:] if kids[x] else ()
        key[x] = (z[x],) + tuple(ks) + tail
    return key


def cmp(a, b):
    return (a > b) - (a < b)


def by_key(A, B):
    return cmp(keys(A)[0], keys(B)[0])


def by_path(A, B, pick):
    x = y = 0
    while True:
        r = cmp(A[0][x], B[0][y])
        if r:
            return r
        ka = sorted((A[0][c] for c in A[1][x]), reverse=True)
        kb = sorted((B[0][c] for c in B[1][y]), reverse=True)
        L = max(len(ka), len(kb))
        r = cmp(ka + [0] * (L - len(ka)), kb + [0] * (L - len(kb)))
        if r:
            return r
        if not A[1][x] or not B[1][y]:
            return 0
        x = pick([c for c in A[1][x] if A[0][c] == ka[0]])
        y = pick([c for c in B[1][y] if B[0][c] == kb[0]])


def by_all_branches(A, B):
    kA, kB = keys(A), keys(B)
    sys.setrecursionlimit(10000)
    def rec(x, y):
        r = cmp(A[0][x], B[0][y])
        if r:
            return r
        ka = sorted((A[0][c] for c in A[1][x]), reverse=True)
        kb = sorted((B[0][c] for c in B[1][y]), reverse=True)
        L = max(len(ka), len(kb))
        r = cmp(ka + [0] * (L - len(ka)), kb + [0] * (L - len(kb)))
        if r:
            return r
        ca = sorted(A[1][x], key=lambda c: kA[c], reverse=True)
        cb = sorted(B[1][y], key=lambda c: kB[c], reverse=True)
        for p, q in zip(ca, cb):
            r = rec(p, q)
            if r:
                return r
        return 0
    return rec(0, 0)


def by_layers(A, B):
    la, lb = [0], [0]
    while la or lb:
        za = sorted((A[0][c] for c in la), reverse=True)
        zb = sorted((B[0][c] for c in lb), reverse=True)
        L = max(len(za), len(zb))
        r = cmp(za + [0] * (L - len(za)), zb + [0] * (L - len(zb)))
        if r:
            return r
        la = [c for x in la for c in A[1][x]]
        lb = [c for x in lb for c in B[1][x]]
    return 0


def all_answers(text):
    A, B = parse(text)
    return [by_key(A, B), by_path(A, B, min), by_path(A, B, max),
            by_all_branches(A, B), by_layers(A, B)]


# ---------- 生成饱和基团 ----------
class Node:
    __slots__ = ("z", "kids")

    def __init__(self, z):
        self.z, self.kids = z, []


def grow(r, heavy, chain_bias, terminal=TERMINAL, heavy_set=HEAVY):
    """heavy 个非端基原子组成的树，空位最后补 H/卤素。chain_bias 越大越像长链。"""
    root = Node(r.choice(heavy_set))
    open_nodes = [root]
    order = [root]
    for _ in range(heavy - 1):
        cand = [o for o in open_nodes if len(o.kids) < VALENCE[o.z] - 1]
        if not cand:
            break
        host = cand[-1] if r.random() < chain_bias else r.choice(cand)
        a = Node(r.choice(heavy_set))
        host.kids.append(a)
        order.append(a)
        if VALENCE[a.z] > 1:
            open_nodes.append(a)
    for o in order:
        while len(o.kids) < VALENCE[o.z] - 1:
            o.kids.append(Node(r.choice(terminal)))
    return root


def clone(t):
    c = Node(t.z)
    c.kids = [clone(k) for k in t.kids]
    return c


def nodes(t):
    out, st = [], [(t, 0)]
    while st:
        x, d = st.pop()
        out.append((x, d))
        st.extend((k, d + 1) for k in x.kids)
    return out


def serialize(t, r):
    rows, q = [], deque([(t, -1)])
    while q:
        x, p = q.popleft()
        idx = len(rows)
        rows.append(f"{idx} {p} {x.z} 1")
        kids = x.kids[:]
        r.shuffle(kids)
        q.extend((k, idx) for k in kids)
    return rows


def mutate(r, t):
    """随机把一个端基原子换成别的端基（或换成甲基）。"""
    t = clone(t)
    x = r.choice([x for x, _ in nodes(t) if not x.kids])
    if r.random() < 0.2:
        x.z = 6
        x.kids = [Node(r.choice(TERMINAL)) for _ in range(3)]
    else:
        x.z = r.choice([z for z in set(TERMINAL) if z != x.z])
    return t


def size(t):
    return len(nodes(t))


def spine(r, length, side_budget):
    """一条 C/Si 主链：主链上下一个原子的原子序数严格大于同层其他支链的首原子，
    所以「最大支链」唯一、一路沿主链往下；Si 后面可以挂 C/N/O 开头的小支链。"""
    zs = [r.choice([6, 6, 14]) for _ in range(length)]
    root = Node(zs[0])
    chain = [root]
    for i in range(1, length):
        a = Node(zs[i])
        prev = chain[-1]
        prev.kids.append(a)
        chain.append(a)
    budget = side_budget
    for i, x in enumerate(chain):
        nxt = zs[i + 1] if i + 1 < length else None
        while len(x.kids) < 3:
            if nxt == 14 and budget > 0 and r.random() < 0.5:
                side = grow(r, r.randint(1, min(4, budget)), 0.5, [1] * 6 + [9], [6, 7, 8])
                budget -= size(side)
                x.kids.append(side)
            else:
                x.kids.append(Node(1))
    return root, chain


def spine_mutate(r, chain, deep):
    """在主链深处做一处改动：H 换卤素 / H 换甲基 / 主链在此处截断成 H。"""
    lo = len(chain) * 2 // 3 if deep else 0
    op = r.random()
    if op < 0.25:
        i = r.randrange(lo, len(chain) - 1)
    else:
        i = r.choice([j for j in range(lo, len(chain)) if any(not k.kids for k in chain[j].kids)])
    x = chain[i]
    if op < 0.25:
        nxt = chain[i + 1]
        x.kids[x.kids.index(nxt)] = Node(1)
        return
    hs = [k for k in x.kids if not k.kids]
    h = r.choice(hs)
    if op < 0.4:
        h.z = 6
        h.kids = [Node(1) for _ in range(3)]
    else:
        h.z = r.choice([z for z in (1, 9, 17, 35, 53) if z != h.z])


def make_case(r, kind):
    if kind == "tiny":
        A = grow(r, r.randint(1, 3), 0.3)
        B = grow(r, r.randint(1, 3), 0.3) if r.random() < 0.5 else mutate(r, A)
    elif kind == "single":
        A, B = Node(r.choice(TERMINAL)), Node(r.choice(TERMINAL))  # n=m=1：只有一个端基原子
    elif kind == "random":
        A, B = grow(r, r.randint(5, 60), 0.5), grow(r, r.randint(5, 60), 0.5)
    else:
        length, side = {"mid": (r.randint(8, 40), 30), "deep": (r.randint(60, 200), 120),
                        "big": (r.randint(280, 330), 0),
                        "wide": (r.randint(120, 160), 520)}[kind]
        sub = r.randrange(1 << 30)
        A, _ = spine(random.Random(sub), length, side)
        B, chainB = spine(random.Random(sub), length, side)   # 同一结构的副本，带主链
        spine_mutate(r, chainB, kind != "mid")
    if size(A) >= 1000 or size(B) >= 1000:
        return None
    if r.random() < 0.5:
        A, B = B, A
    ra, rb = serialize(A, r), serialize(B, r)
    return f"{len(ra)} {len(rb)}\n" + "\n".join(ra + rb) + "\n"


def depth_of_decision(text):
    A, B = parse(text)
    x = y = d = 0
    kA, kB = keys(A), keys(B)
    while True:
        if A[0][x] != B[0][y]:
            return d
        if sorted(A[0][c] for c in A[1][x]) != sorted(B[0][c] for c in B[1][y]):
            return d + 1
        x = max(A[1][x], key=lambda c: kA[c])
        y = max(B[1][y], key=lambda c: kB[c])
        d += 1


def swap(text):
    """交换两个基团的先后顺序（答案随之 1<->2）。"""
    lines = text[:-1].split("\n")
    n, m = map(int, lines[0].split())
    return "\n".join([f"{m} {n}"] + lines[1 + n:] + lines[1:1 + n]) + "\n"


def build():
    r = random.Random(SEED)
    plan = (["single"] * 2 + ["tiny"] * 5 + ["random"] * 6 + ["mid"] * 9 +
            ["deep"] * 10 + ["big"] * 4 + ["wide"] * 2)
    cases = [s for s, _ in SAMPLES]
    for kind in plan:
        while True:
            t = make_case(r, kind)
            if t is None or t in cases:
                continue
            ans = all_answers(t)
            if ans[0] != 0 and all(a == ans[0] for a in ans) and ans[0] != (-1 if len(cases) % 2 else 1):
                t = swap(t)        # 让答案 1、2 交替出现（ans 为 1 表示第一个基团大，-1 表示第二个大）
                ans = all_answers(t)
            if t not in cases and ans[0] != 0 and all(a == ans[0] for a in ans):
                cases.append(t)
                break
    assert len(cases) == CASES
    return cases


def main():
    cases = build()
    out = Path("data")
    out.mkdir(exist_ok=True)
    for p in out.glob("*"):
        p.unlink()
    for i, text in enumerate(cases):
        assert valid(text), i
        res = subprocess.run([sys.executable, "-I", "samplecode.py"], input=text, text=True,
                             capture_output=True, timeout=60, check=True).stdout.rstrip() + "\n"
        if i < len(SAMPLES):
            assert res == SAMPLES[i][1], i
        else:
            a = all_answers(text)[0]
            assert res == ("1\n" if a == 1 else "2\n"), i
        (out / f"{i}.in").write_text(text)
        (out / f"{i}.out").write_text(res)
        if i >= len(SAMPLES):
            print(i, text.split("\n")[0], "decided at depth", depth_of_decision(text), res.strip())


if __name__ == "__main__":
    main()
