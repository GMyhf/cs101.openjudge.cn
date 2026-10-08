"""4076 寻找矩阵路径 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

2026-10 审计重写：
- 原生成器 M,N<=8、K<=10、元素 0..4，离题面 M,N<=200、K<=1000 太远；也没有专门卡
  「每个点只能经过一次」（允许回头就会误判为 1）、K>M*N、1x1 等边界的组。
- 原参考解（也是原 samplecode）是递归 DFS，K 接近 1000 时会撞上 Python 默认递归深度，
  现参考解改为显式栈的迭代 DFS（同一搜索顺序与剪枝）。
- 校验：小组（格子数 <= 30）与 ORACLE_SOURCE 对拍——它按 (当前格, 已访问集合) 做逐层集合扩展，
  与 DFS 回溯不同族；大组的答案由构造保证（YES 组在网格里埋了一条自回避路径；NO 组的序列含
  网格中不存在的值；回头陷阱组由参考解求得并断言为 0），生成时逐组断言参考解与构造一致。
"""
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path

NUMBER = 4076
SAMPLE_IN = '3 4\n0 1 2 4\n10 5 2 10\n0 3 4 4\n6\n0 1 2 2 4 3\n'
SAMPLE_OUT = '1\n'

REFERENCE_SOURCE = r'''import sys
def main():
    a = sys.stdin.buffer.read().split()
    m, n = int(a[0]), int(a[1])
    g = [int(x) for x in a[2:2 + m * n]]
    k = int(a[2 + m * n]); pat = [int(x) for x in a[3 + m * n:3 + m * n + k]]
    if k > m * n:
        print(0); return
    nb = []
    for i in range(m):
        for j in range(n):
            z = []
            if i + 1 < m: z.append((i + 1) * n + j)
            if i > 0: z.append((i - 1) * n + j)
            if j + 1 < n: z.append(i * n + j + 1)
            if j > 0: z.append(i * n + j - 1)
            nb.append(z)
    used = bytearray(m * n)
    for s in range(m * n):
        if g[s] != pat[0]:
            continue
        if k == 1:
            print(1); return
        used[s] = 1
        stack = [(s, 0)]               # (格子, 已尝试到的邻居下标)
        while stack:
            u, t = stack[-1]
            p = len(stack)             # 下一个要匹配 pat[p]
            nxt = -1
            z = nb[u]
            while t < len(z):
                v = z[t]; t += 1
                if not used[v] and g[v] == pat[p]:
                    nxt = v; break
            if nxt < 0:
                stack.pop(); used[u] = 0
                continue
            stack[-1] = (u, t)
            if p + 1 == k:
                print(1); return
            used[nxt] = 1
            stack.append((nxt, 0))
    print(0)
main()
'''

ORACLE_SOURCE = r'''import sys
a = sys.stdin.read().split()
m, n = int(a[0]), int(a[1])
g = [int(x) for x in a[2:2 + m * n]]
k = int(a[2 + m * n]); pat = [int(x) for x in a[3 + m * n:3 + m * n + k]]
# 状态 = (当前格, 已访问格的位集)，逐层推进
layer = {(s, 1 << s) for s in range(m * n) if g[s] == pat[0]}
for p in range(1, k):
    new = set()
    for u, mask in layer:
        i, j = divmod(u, n)
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < m and 0 <= y < n:
                v = x * n + y
                if not mask >> v & 1 and g[v] == pat[p]:
                    new.add((v, mask | 1 << v))
    layer = new
    if not layer:
        break
print(1 if layer else 0)
'''


def valid(text):
    """题面：第一行正整数 M N（M,N<=200）；M 行、每行 N 个整数；一行正整数 K（K<=1000）；
    最后一行 K 个整数。元素取值范围题面未给，只核为整数。"""
    try:
        lines = text.split("\n")
        while lines and lines[-1].strip() == "":
            lines.pop()
        rows = [ln.split() for ln in lines]
        if not rows or len(rows[0]) != 2:
            return False
        m, n = map(int, rows[0])
        if not (1 <= m <= 200 and 1 <= n <= 200):
            return False
        if len(rows) != m + 3:
            return False
        for i in range(1, m + 1):
            if len(rows[i]) != n:
                return False
            for tok in rows[i]:
                int(tok)
        if len(rows[m + 1]) != 1:
            return False
        k = int(rows[m + 1][0])
        if not 1 <= k <= 1000 or len(rows[m + 2]) != k:
            return False
        for tok in rows[m + 2]:
            int(tok)
        return True
    except ValueError:
        return False


def fmt(g, seq):
    return (f"{len(g)} {len(g[0])}\n" + "\n".join(" ".join(map(str, row)) for row in g)
            + f"\n{len(seq)}\n{' '.join(map(str, seq))}\n")


def _room(m, n, seen, start, need):
    """从 start 出发、不经过 seen 能到达的格子数是否 >= need（数够就停）。"""
    stack = [start]; mark = {start}
    while stack and len(mark) < need:
        i, j = stack.pop()
        for c in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= c[0] < m and 0 <= c[1] < n and c not in seen and c not in mark:
                mark.add(c); stack.append(c)
    return len(mark) >= need


def saw(r, m, n, k):
    """自回避随机游走，长度恰为 k。每步只走「剩余可达格子够用」的方向，失败就重来。"""
    if k == m * n:                      # 走满：蛇形
        return [(i, j if i % 2 == 0 else n - 1 - j) for i in range(m) for j in range(n)]
    while True:
        s = (r.randrange(m), r.randrange(n)); path = [s]; seen = {s}
        while len(path) < k:
            i, j = path[-1]
            opts = [(x, y) for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
                    if 0 <= x < m and 0 <= y < n and (x, y) not in seen]
            r.shuffle(opts)
            nxt = None
            for c in opts:
                if _room(m, n, seen, c, k - len(path)):
                    nxt = c; break
            if nxt is None:
                break
            path.append(nxt); seen.add(nxt)
        if len(path) == k:
            return path


def planted(r, m, n, k, vals):
    """YES：随机网格里埋一条长 k 的自回避路径，序列取其上的值。"""
    g = [[r.choice(vals) for _ in range(n)] for _ in range(m)]
    path = saw(r, m, n, k)
    seq = [g[i][j] for i, j in path]
    return g, seq


def absent_value(r, m, n, k, vals, pos):
    """NO：序列由埋好的路径改出，第 pos 个改成网格里不存在的值。"""
    g, seq = planted(r, m, n, k, vals)
    seq[pos] = max(vals) + 1 + r.randint(0, 5)
    return g, seq


def build_cases():
    cases = [(SAMPLE_IN, 1)]
    r = random.Random(NUMBER)
    # 边界小组
    cases.append(("1 1\n7\n1\n7\n", 1))
    cases.append(("1 1\n7\n1\n8\n", 0))
    cases.append(("1 1\n7\n2\n7 7\n", 0))                  # 不许原地/回头
    cases.append(("1 2\n5 5\n3\n5 5 5\n", 0))              # 允许回头就会误判 1
    cases.append(("2 2\n1 1\n1 1\n4\n1 1 1 1\n", 1))       # 恰好走满
    cases.append(("2 2\n1 1\n1 1\n5\n1 1 1 1 1\n", 0))     # K>M*N
    cases.append(("2 2\n1 2\n3 4\n2\n1 4\n", 0))           # 对角不算相邻
    cases.append(("3 3\n-1 -2 -3\n-4 -5 -6\n-7 -8 -9\n5\n-1 -2 -5 -8 -9\n", 1))
    # 小规模随机，与位集 oracle 对拍
    for i in range(12):
        m = r.randint(1, 5); n = r.randint(1, 6)
        g = [[r.randint(0, 2) for _ in range(n)] for _ in range(m)]
        if i % 2 == 0 and m * n >= 2:
            path = saw(r, m, n, r.randint(1, min(m * n, 8)))
            seq = [g[x][y] for x, y in path]
        else:
            seq = [r.randint(0, 2) for _ in range(r.randint(1, 9))]
        cases.append((fmt(g, seq), None))
    # 中大规模：答案由构造保证
    cases.append((fmt(*planted(r, 200, 200, 1000, list(range(10)))), 1))
    cases.append((fmt(*planted(r, 200, 200, 1000, list(range(4)))), 1))
    cases.append((fmt(*planted(r, 200, 200, 1000, [-10 ** 9, 10 ** 9, 0, 123456789, -5])), 1))
    cases.append((fmt(*planted(r, 200, 200, 1, list(range(100)))), 1))
    cases.append((fmt(*planted(r, 1, 200, 200, list(range(3)))), 1))        # 单行，路径走满
    cases.append((fmt(*planted(r, 200, 1, 150, list(range(3)))), 1))        # 单列
    cases.append((fmt(*planted(r, 30, 30, 900, list(range(5)))), 1))        # 哈密顿路径（蛇形走满）
    cases.append((fmt(*planted(r, 200, 200, 1000, list(range(1000)))), 1))
    cases.append((fmt(*planted(r, 150, 180, 777, list(range(6)))), 1))
    # NO 组用较宽的值域：本题是一般图上的简单路径匹配，值域很窄时「前缀全匹配、最后才失败」会让
    # 任何回溯解（含参考解）指数爆炸，那样的数据没有可行解法，故不造。
    cases.append((fmt(*absent_value(r, 200, 200, 1000, list(range(100)), 999)), 0))
    cases.append((fmt(*absent_value(r, 200, 200, 1000, list(range(10)), 150)), 0))
    cases.append((fmt(*absent_value(r, 200, 200, 1000, list(range(5)), 0)), 0))
    cases.append((fmt(*absent_value(r, 200, 200, 1000, list(range(1000)), 999)), 0))
    cases.append((fmt(*absent_value(r, 200, 200, 1000, list(range(300)), 700)), 0))
    cases.append((fmt(*absent_value(r, 120, 200, 600, list(range(50)), 599)), 0))
    # 只有回头才能凑出的序列：在埋好的路径末尾再接回倒数第二格的值；末格的其余邻居改掉该值，
    # 允许回头的写法会输出 1，正确答案为 0（由参考解给出并断言）
    vals = list(range(20, 1000))
    g = [[r.choice(vals) for _ in range(200)] for _ in range(200)]
    path = saw(r, 200, 200, 999); on = set(path)
    seq = [g[i][j] for i, j in path]
    i, j = path[-1]
    for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
        if 0 <= x < 200 and 0 <= y < 200 and (x, y) not in on and g[x][y] == seq[-2]:
            g[x][y] = seq[-2] + 1 if seq[-2] + 1 < 1000 else 20
    seq.append(seq[-2])
    cases.append((fmt(g, seq), 0))
    # K 超过格子数：沿蛇形走满全部 400 格的值再多接一个。值域取宽，未特判 K>M*N 的普通回溯
    # 也能很快走到底再失败（原先 0/1 值域的随机序列只有特判 K>M*N 才跑得动，对正确的回溯写法不公平）。
    # 用独立种子，不影响后续组的随机流。
    rk = random.Random(NUMBER * 13)
    g, seq = planted(rk, 20, 20, 400, list(range(1000)))
    cases.append((fmt(g, seq + [rk.randrange(1000)]), 0))
    cases.append((fmt([[0] * 200 for _ in range(5)], [0] * 1000), 1))      # 全同值，蛇形可走满
    cases.append((fmt(*planted(r, 100, 100, 500, list(range(-50, 0)))), 1))   # 负数值域
    return cases


def _run(source, content, limit=600):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8", delete=False) as fh:
        fh.write(source)
        path = fh.name
    try:
        return subprocess.run([sys.executable, path], input=content, text=True,
                              capture_output=True, timeout=limit, check=True).stdout
    finally:
        os.unlink(path)


def main():
    built = build_cases()
    cases = [c for c, _ in built]
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert len(set(cases)) == len(cases), "组间不得重复"
    for i, c in enumerate(cases):
        assert valid(c), f"第 {i} 组越出题面约束"
        assert len(c.encode()) <= 1 << 20, f"第 {i} 组 .in 超过 1MB"
    assert _run(REFERENCE_SOURCE, SAMPLE_IN) == SAMPLE_OUT, "参考解跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for old in list(root.glob("*.in")) + list(root.glob("*.out")):
        old.unlink()
    for i, (c, expect) in enumerate(built):
        out = _run(REFERENCE_SOURCE, c)
        if expect is not None:
            assert out == f"{expect}\n", f"第 {i} 组参考解与构造答案不一致"
        m, n = map(int, c.split()[:2])
        if m * n <= 30:
            assert _run(ORACLE_SOURCE, c) == out, f"第 {i} 组参考解与位集 oracle 不一致"
        (root / f"{i}.in").write_text(c, encoding="utf-8")
        (root / f"{i}.out").write_text(out, encoding="utf-8")
    print(f"generated {len(cases)} cases")


if __name__ == "__main__":
    main()
