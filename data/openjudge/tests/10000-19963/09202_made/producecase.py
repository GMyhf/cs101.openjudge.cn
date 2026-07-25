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


def build_cases():
    cases = [SAMPLE_IN]
    for index in range(1, 21):
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
    assert len(set(cases)) >= 15, "去重后至少 15 组"
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
