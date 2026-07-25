"""29803 测试数据生成器：让防护等级真的变化，重跑可逐字节复现 data/。

出处：build_t003_002_round4 —— 2026-07-25 回归扫描修正。
原生成器每张图都放一条直连边 (1, n)，且时限 limit 一定够走它；一次性光学迷彩
正好把这条边的交火等级抹掉 —— 于是 21 组里 20 组答案都是 0，数据几乎没有
鉴别力（唯一非 0 的一组来自另一种形状）。

现在：直连边 (1, n) 的耗时故意超过时限，逼着必须走链路 1-2-...-n；
迷彩只能抹掉链上一条边，答案即链上**第二大**的交火等级，随机后天然分散。
题面保证「100 的防护等级下可以按时到达」-> 链路总耗时 <= T，生成器内断言。
另用 Floyd + 枚举迷彩边的独立实现复核（参考解法是二分 + Dijkstra，不同族）。
"""
import random
from pathlib import Path

SAMPLE_IN = '4 4 6\n1 2 4 0\n2 4 4 10\n1 3 3 50\n3 4 3 60\n'
SAMPLE_OUT = '50\n'
INF = float("inf")


def reachable_within(n, edges, allowed, camo, limit):
    """Floyd 求最短路：只用交火等级 <= allowed 的边，外加至多一条迷彩边 camo。"""
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    for v in range(1, n + 1):
        dist[v][v] = 0
    for i, (u, v, t, a) in enumerate(edges):
        if a <= allowed or i == camo:
            dist[u][v] = min(dist[u][v], t)
            dist[v][u] = min(dist[v][u], t)
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist[1][n] <= limit


def min_armor(n, edges, limit):
    """独立实现：枚举防护等级候选与迷彩边，不用二分也不用 Dijkstra。"""
    for allowed in sorted({0} | {a for _, _, _, a in edges}):
        if any(reachable_within(n, edges, allowed, camo, limit)
               for camo in [-1] + list(range(len(edges)))):
            return allowed
    return 100


def solve_text(text):
    rows = text.split("\n")
    n, m, limit = map(int, rows[0].split())
    edges = [tuple(map(int, rows[1 + i].split())) for i in range(m)]
    return str(min_armor(n, edges, limit)) + "\n"


def one_case(r):
    n = r.randint(4, 9)
    chain = [(v, v + 1, r.randint(1, 6), r.randint(0, 100)) for v in range(1, n)]
    total = sum(e[2] for e in chain)
    limit = total + r.randint(0, 2)
    # 直连边耗时超过时限 -> 用不上，逼着走链路
    edges = chain + [(1, n, limit + r.randint(1, 5), r.randint(0, 100))]
    if r.random() < .5:                      # 一条绕远的旁路，也超时限
        u = r.randint(2, n - 1)
        edges.append((u, n, limit + r.randint(1, 5), r.randint(0, 100)))
    r.shuffle(edges)
    assert total <= limit, "题面保证 100 的防护等级下可以按时到达"
    assert all(0 <= a <= 100 for _, _, _, a in edges), "题面：交火等级 0~100"
    assert all(1 <= u <= n and 1 <= v <= n and u != v for u, v, _, _ in edges)
    body = f"{n} {len(edges)} {limit}\n" + "".join("%d %d %d %d\n" % e for e in edges)
    # 期望：迷彩抹掉链上最高的那条，答案是链上第二大的交火等级
    levels = sorted((a for _, _, _, a in chain), reverse=True)
    expect = levels[1] if len(levels) > 1 else 0
    assert int(solve_text(body)) == expect, "构造意图与独立实现不符"
    return body


def build_cases():
    cases = [SAMPLE_IN]
    for index in range(1, 40):
        if len(cases) >= 21:
            break
        content = one_case(random.Random(29803 + index * 6151))
        if content not in cases:
            cases.append(content)
    answers = [solve_text(c).strip() for c in cases]
    assert len(set(answers)) >= 10, "答案要真的分散，不能塌缩"
    assert max(int(a) for a in answers) >= 50, "要有需要高防护等级的组"
    assert len(set(cases)) >= 15, "去重后至少 15 组"
    return cases


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
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip(), "独立实现跑不出样例输出"
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"

    emit(cases, solve_text)


if __name__ == "__main__":
    main()
