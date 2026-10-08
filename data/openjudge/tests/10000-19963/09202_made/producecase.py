"""9202 测试数据生成器：有环 / 无环两个分支各占一半，重跑可逐字节复现 data/。

出处：build_001c —— 2026-07-25 回归扫描修正。
原生成器 `for i in range(1, n): edges.add((i, randint(1, i)))` 在 i=1 时
必然产生 (1,1) 自环，而题面明写「接下来 M 行每行 2 个**不相等**的整数 x,y」——
20/20 组都违反了题面的输入约定；自环同时把答案锁死成 Yes，整份数据里唯一的
No 来自题面样例本身，「无环」分支等于没被数据覆盖。

现在：随机取一个拓扑序，只在序上从前往后连边得到 DAG（天然 x != y），
一半的组再加一条回边成环。每组都用独立的 DFS 三色法复核有环性
（参考解法走的是 Kahn 拓扑排序 + 计数，不同族），确保标注与事实一致。
"""
import random
from pathlib import Path

SAMPLE_IN = '2\n7 6\n1 2\n1 3\n2 4\n2 5\n3 6\n3 7\n12 13\n1 2\n2 3\n2 4\n3 5\n5 6\n4 6\n6 7\n7 8\n8 4\n7 9\n9 10\n10 11\n10 12\n'
SAMPLE_OUT = 'No\nYes\n'


def has_cycle(n, edges):
    """DFS 三色法 —— 与参考解法的 Kahn 拓扑排序不同族，用来复核。"""
    adj = {v: [] for v in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
    color = {v: 0 for v in range(1, n + 1)}

    def walk(start):
        stack = [(start, iter(adj[start]))]
        color[start] = 1
        while stack:
            node, it = stack[-1]
            for nxt in it:
                if color[nxt] == 1:
                    return True
                if color[nxt] == 0:
                    color[nxt] = 1
                    stack.append((nxt, iter(adj[nxt])))
                    break
            else:
                color[node] = 2
                stack.pop()
        return False

    return any(color[v] == 0 and walk(v) for v in range(1, n + 1))


def one_graph(r, want_cycle):
    n = r.randint(4, 25)
    order = list(range(1, n + 1))
    r.shuffle(order)
    rank = {v: i for i, v in enumerate(order)}
    pool = [(a, b) for a in range(1, n + 1) for b in range(1, n + 1)
            if a != b and rank[a] < rank[b]]
    r.shuffle(pool)
    edges = pool[:r.randint(max(1, n // 2), min(len(pool), 2 * n))]
    if want_cycle:
        u, v = r.choice(edges)
        edges.append((v, u))                 # 加一条回边，必成环
    r.shuffle(edges)
    assert all(x != y for x, y in edges), "题面：每行两个不相等的整数"
    assert all(1 <= x <= n and 1 <= y <= n for x, y in edges), "题面：目标编号 1..N"
    assert has_cycle(n, edges) == want_cycle, "构造意图与独立判定不符"
    return n, edges


def valid(text):
    """题面：T（1<=T<=5）组；每组 N M（1<=N<=100000，1<=M<=500000），
    再 M 行各两个不相等的整数 x y（1..N）。按行严格核对。"""
    lines = text.split("\n")
    if not lines or lines[-1] != "":
        return False
    lines = lines[:-1]
    pos = 0

    def ints(k):
        nonlocal pos
        if pos >= len(lines):
            return None
        tok = lines[pos].split()
        pos += 1
        if len(tok) != k or not all(t.isdigit() for t in tok):
            return None
        return list(map(int, tok))

    head = ints(1)
    if head is None or not 1 <= head[0] <= 5:
        return False
    for _ in range(head[0]):
        nm = ints(2)
        if nm is None:
            return False
        n, m = nm
        if not (1 <= n <= 100000 and 1 <= m <= 500000):
            return False
        for _ in range(m):
            e = ints(2)
            if e is None or e[0] == e[1] or not all(1 <= v <= n for v in e):
                return False
    return pos == len(lines)


def block(n, edges):
    return f"{n} {len(edges)}\n" + "".join(f"{u} {v}\n" for u, v in edges)


def big_graph(r, n, kind, m):
    """大图：kind 取 chain / chain_cycle / dag / dag_cycle。编号随机打乱，
    m 受单组 .in ≤ 1MB 的限制（题面上限 M=500000 放不进 1MB）。"""
    label = list(range(1, n + 1))
    r.shuffle(label)
    if kind.startswith("chain"):
        edges = [(label[i], label[i + 1]) for i in range(m)]
        if kind == "chain_cycle":
            edges.append((label[m], label[0]))          # 长度 m+1 的大环
    else:
        edges = set()
        while len(edges) < m:
            a = r.randrange(n - 1)
            b = min(n - 1, a + 1 + int(r.expovariate(1 / 30)))
            edges.add((a, b))
        edges = sorted(edges)
        if kind == "dag_cycle":                         # 沿已有边走一段长路，再连回去
            adj = {}
            for a, b in edges:
                adj.setdefault(a, []).append(b)
            start = edges[r.randrange(len(edges) // 10)][0]
            cur, steps = start, 0
            while cur in adj and steps < 5000:
                cur = r.choice(adj[cur])
                steps += 1
            edges.append((cur, start))
        edges = [(label[a], label[b]) for a, b in edges]
    r.shuffle(edges)
    assert has_cycle(n, edges) == kind.endswith("cycle")
    return edges


def extra_cases():
    """2026-10 审计补充：原数据 N<=25，递归 DFS 爆栈、O(N^2) 写法都卡不住；
    也没有 N=2 这样的最小图、多连通块且环不在 1 号点所在块的情形。"""
    r = random.Random(92020)
    out = ["1\n2 1\n1 2\n", "1\n2 2\n1 2\n2 1\n", "1\n3 3\n1 2\n2 3\n3 1\n",
           "1\n100000 1\n100000 1\n",
           "2\n3 2\n2 1\n3 1\n3 3\n1 2\n1 3\n2 3\n"]
    for kind, m in (("chain", 69999), ("chain_cycle", 69998), ("dag", 70000), ("dag_cycle", 70000)):
        out.append("1\n" + block(100000, big_graph(r, 100000, kind, m)))
    blocks = []
    for kind in ("dag", "chain_cycle", "chain", "dag_cycle", "dag"):
        blocks.append(block(20000, big_graph(r, 20000, kind, 14000 if kind.startswith("dag") else 13999)))
    out.append("5\n" + "".join(blocks))
    # 很多个互不相连的小链，只有编号最大的一块里有环
    edges, k = [], 0
    while k + 4 <= 60000:
        edges += [(k + 1, k + 2), (k + 2, k + 3), (k + 3, k + 4)]
        k += 4
    edges.append((k, k - 3))
    out.append("1\n" + block(100000, edges))
    return out


def build_cases():
    cases = [SAMPLE_IN]
    for index in range(1, 40):
        r = random.Random(9202 + index * 1013)
        groups = r.randint(1, 3)             # 每份文件多组数据，压到 T 的循环
        blocks, want = [], []
        for g in range(groups):
            wc = bool((index + g) % 2)
            n, edges = one_graph(r, wc)
            want.append(wc)
            blocks.append(f"{n} {len(edges)}\n" + "".join(f"{u} {v}\n" for u, v in edges))
        content = f"{groups}\n" + "".join(blocks)
        if content not in cases:
            cases.append(content)
    cases += [c for c in extra_cases() if c not in cases]
    assert len(set(cases)) >= 15, "去重后至少 15 组"
    assert all(valid(c) for c in cases), "题面输入格式与取值范围"
    return cases


def solve_text(text):
    """与参考解法同形（Kahn），只用于产生 .out；正确性由 has_cycle 交叉复核。"""
    it = iter(text.split())
    t = int(next(it))
    out = []
    for _ in range(t):
        n, m = int(next(it)), int(next(it))
        edges = [(int(next(it)), int(next(it))) for _ in range(m)]
        indeg = {v: 0 for v in range(1, n + 1)}
        adj = {v: [] for v in range(1, n + 1)}
        for u, v in edges:
            adj[u].append(v)
            indeg[v] += 1
        queue = [v for v in indeg if indeg[v] == 0]
        seen = 0
        while queue:
            u = queue.pop()
            seen += 1
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    queue.append(v)
        cyc = seen != n
        assert cyc == has_cycle(n, edges), "Kahn 与 DFS 三色法判定不一致"
        out.append("Yes" if cyc else "No")
    return "\n".join(out) + "\n"


def emit(cases, solve):
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for old in list(root.glob("*.in")) + list(root.glob("*.out")):
        old.unlink()
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve(content), encoding="utf-8")
    print(f"generated {len(cases)} cases")


def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip(), "参考解法跑不出样例输出"
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    answers = [solve_text(c) for c in cases]
    flat = " ".join(answers).split()
    assert flat.count("Yes") >= 10 and flat.count("No") >= 10, "两个分支都要有足够数据"

    emit(cases, solve_text)


if __name__ == "__main__":
    main()
