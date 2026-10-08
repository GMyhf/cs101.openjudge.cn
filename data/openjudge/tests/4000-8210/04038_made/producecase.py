"""4038 观光公交 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

2026-10 审计重写：
- 原生成器 n<=7、m<=7、k<=8，离题面 n<=1000、m<=10000、k<=100000 差得太远；原参考解
  （也是原 samplecode）把 k 个加速器在各段间做全部分配的暴力，指数级，只能跑这种玩具规模。
- 现参考解：经典贪心，每次把加速器用在「受益乘客最多」的一段上；同一段在受益集合不变期间
  成批使用（批量 = min(剩余 k, D_i, 受影响站上的最小松弛)），批次数 O(n)，总 O(n^2)。
- BRUTE_SOURCE 即原暴力（全部分配方案取最优），每次生成都在全部小组上与参考解对拍；
  另有 GREEDY1_SOURCE（逐个加速器、不成批的贪心）在中等组上对拍。
"""
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path

NUMBER = 4038
SAMPLE_IN = '3 3 2 \n1 4 \n0 1 3 \n1 1 2 \n5 2 3\n'
SAMPLE_OUT = '10\n'

REFERENCE_SOURCE = r'''import sys
def main():
    a = sys.stdin.buffer.read().split()
    n, m, k = int(a[0]), int(a[1]), int(a[2])
    D = [0] + [int(x) for x in a[3:3 + n - 1]]          # D[i]: i -> i+1
    p = 3 + n - 1
    last = [0] * (n + 2)                                 # 站点最晚到达乘客时刻
    down = [0] * (n + 2)                                 # 在该站下车人数
    sumT = 0
    for _ in range(m):
        t, x, y = int(a[p]), int(a[p + 1]), int(a[p + 2]); p += 3
        if t > last[x]:
            last[x] = t
        down[y] += 1
        sumT += t
    arr = [0] * (n + 2)
    def compute():
        arr[1] = 0
        for i in range(1, n):
            arr[i + 1] = max(arr[i], last[i]) + D[i]
    compute()
    while k > 0:
        # far[i]: 从站 i 起，到达时间的减少能一直传到的最远站（arr[j]>last[j] 时继续传）
        best = 0; bi = -1; bslack = 0
        reach = 0; slack = 0; ben = 0
        # 从后往前：g[j] = 若站 j 到达提前 1，受益的下车人数；以及传播链上最小松弛
        g = [0] * (n + 2); sl = [0] * (n + 2)
        g[n] = down[n]; sl[n] = 1 << 60
        for j in range(n - 1, 1, -1):
            if arr[j] > last[j]:
                g[j] = down[j] + g[j + 1]
                s = arr[j] - last[j]
                sl[j] = s if s < sl[j + 1] else sl[j + 1]
            else:
                g[j] = down[j]; sl[j] = 1 << 60
        for i in range(1, n):
            if D[i] > 0 and g[i + 1] > best:
                best = g[i + 1]; bi = i
        if bi < 0:
            break
        # 站 i+1 的到达提前不受 i+1 自身松弛约束（传播到 i+2 才需要 arr[i+1]>last[i+1]）
        j = bi + 1
        lim = sl[j] if j <= n - 1 and arr[j] > last[j] else 1 << 60
        use = min(k, D[bi], lim)
        D[bi] -= use; k -= use
        compute()
    total = 0
    p = 3 + n - 1
    for _ in range(m):
        y = int(a[p + 2]); p += 3
        total += arr[y]
    print(total - sumT)
main()
'''

GREEDY1_SOURCE = r'''import sys
a = sys.stdin.read().split()
n, m, k = int(a[0]), int(a[1]), int(a[2])
D = [0] + [int(x) for x in a[3:3 + n - 1]]
ps = [tuple(map(int, a[3 + n - 1 + 3 * i:6 + n - 1 + 3 * i])) for i in range(m)]
last = [0] * (n + 2)
for t, x, y in ps:
    last[x] = max(last[x], t)
def arrivals():
    arr = [0] * (n + 2)
    for i in range(1, n):
        arr[i + 1] = max(arr[i], last[i]) + D[i]
    return arr
for _ in range(k):
    arr = arrivals()
    base = sum(arr[y] for _, _, y in ps)
    best = 0; bi = -1
    for i in range(1, n):
        if D[i] > 0:
            D[i] -= 1
            z = base - sum(arrivals()[y] for _, _, y in ps)
            D[i] += 1
            if z > best:
                best = z; bi = i
    if bi < 0:
        break
    D[bi] -= 1
arr = arrivals()
print(sum(arr[y] - t for t, _, y in ps))
'''

BRUTE_SOURCE = r'''import sys
a = sys.stdin.read().split()
n, m, k = map(int, a[:3]); d = list(map(int, a[3:3 + n - 1]))
ps = [tuple(map(int, a[3 + n - 1 + 3 * i:3 + n - 1 + 3 * i + 3])) for i in range(m)]
def total(cut):
    travel = [d[i] - cut[i] for i in range(n - 1)]; clock = 0; ans = 0
    waiting = {i: [] for i in range(1, n + 1)}; active = []
    for t, x, y in ps:
        waiting[x].append((t, y))
    for station in range(1, n):
        if waiting[station]:
            clock = max(clock, max(t for t, _ in waiting[station])); active.extend(waiting[station])
        clock += travel[station - 1]
        done = [z for z in active if z[1] == station + 1]
        ans += sum(clock - t for t, _ in done)
        active = [z for z in active if z[1] != station + 1]
    return ans
best = 10 ** 18
def distribute(i, left, cut):
    global best
    if i == n - 1:
        best = min(best, total(cut)); return
    for x in range(min(left, d[i]) + 1):
        distribute(i + 1, left - x, cut + [x])
distribute(0, k, [])
print(best)
'''

N_MAX, M_MAX, K_MAX, D_MAX, T_MAX = 1000, 10000, 100000, 100, 100000


def valid(text):
    """题面：第 1 行 n m k；第 2 行 n-1 个 D_i；随后 m 行 T A B（A<B）。
    1<=n<=1000，1<=m<=10000，0<=k<=100000，0<=D_i<=100，0<=T_i<=100000，1<=A<B<=n。"""
    try:
        lines = text.split("\n")
        while lines and lines[-1].strip() == "":
            lines.pop()
        rows = [ln.split() for ln in lines]
        if len(rows) < 2 or len(rows[0]) != 3:
            return False
        n, m, k = map(int, rows[0])
        if not (1 <= n <= N_MAX and 1 <= m <= M_MAX and 0 <= k <= K_MAX):
            return False
        if len(rows) != 2 + m or len(rows[1]) != n - 1:
            return False
        if any(not (0 <= int(x) <= D_MAX) for x in rows[1]):
            return False
        for row in rows[2:]:
            if len(row) != 3:
                return False
            t, x, y = map(int, row)
            if not (0 <= t <= T_MAX and 1 <= x < y <= n):
                return False
        return True
    except ValueError:
        return False


def fmt(n, k, d, ps):
    return f"{n} {len(ps)} {k}\n{' '.join(map(str, d))}\n" + "\n".join(f"{t} {x} {y}" for t, x, y in ps) + "\n"


def gen(r, n, m, k, dmax, tmax, style="rand"):
    d = [r.randint(0, dmax) for _ in range(n - 1)]
    ps = []
    for _ in range(m):
        if style == "short":            # 短途乘客为主
            x = r.randint(1, n - 1); y = min(n, x + r.randint(1, 3))
        elif style == "long":           # 长途乘客为主
            x = r.randint(1, max(1, n // 10)); y = r.randint(max(x + 1, n - n // 10), n)
        else:
            x = r.randint(1, n - 1); y = r.randint(x + 1, n)
        if style == "inc":              # 到达时刻随站号递增，车经常要等
            t = min(tmax, x * tmax // n + r.randint(0, max(1, tmax // n)))
        else:
            t = r.randint(0, tmax)
        ps.append((t, x, y))
    return fmt(n, k, d, ps)


def build_cases():
    cases = [SAMPLE_IN]
    r = random.Random(NUMBER)
    # 边界小组
    cases.append("2 1 0\n0\n0 1 2\n")                       # 最小，k=0，D=0
    cases.append("2 1 100000\n100\n100000 1 2\n")           # k 远大于可用，D 减到 0
    cases.append("3 2 1\n5 5\n0 1 2\n10 2 3\n")             # k=1
    cases.append("4 3 5\n0 0 0\n1 1 4\n2 2 4\n3 3 4\n")     # 全 0 段，加速器无用
    # 小规模随机，和指数暴力对拍
    for i in range(14):
        n = r.randint(2, 6); m = r.randint(1, 8); k = r.randint(0, 9)
        cases.append(gen(r, n, m, k, r.choice([3, 6, 10]), r.choice([5, 20, 500]),
                         ["rand", "short", "long", "inc"][i % 4]))
    # 中等规模，和逐个贪心对拍
    for i in range(8):
        n = r.randint(20, 100); m = r.randint(50, 1000); k = r.randint(0, 100)
        cases.append(gen(r, n, m, k, 100, r.choice([500, 10000]), ["rand", "short", "long", "inc"][i % 4]))
    # 满规模 n=1000, m=10000
    big = [
        (1000, 10000, 100000, 100, 100000, "rand"),
        (1000, 10000, 100000, 100, 100000, "inc"),
        (1000, 10000, 100000, 100, 100000, "short"),
        (1000, 10000, 100000, 100, 100000, "long"),
        (1000, 10000, 0, 100, 100000, "rand"),          # k=0
        (1000, 10000, 1, 100, 100000, "inc"),           # k=1
        (1000, 10000, 50000, 100, 100000, "inc"),
        (1000, 10000, 20000, 100, 1000, "rand"),
        (1000, 10000, 100000, 10, 100000, "inc"),       # k 超过 sum(D)
        (1000, 10000, 3000, 100, 100000, "long"),
        (1000, 10000, 100000, 100, 100, "short"),
        (999, 9999, 77777, 100, 100000, "inc"),
        (1000, 10000, 100000, 100, 100000, "inc"),
    ]
    for n, m, k, dmax, tmax, style in big:
        cases.append(gen(r, n, m, k, dmax, tmax, style))
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
    cases = build_cases()
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
    for i, c in enumerate(cases):
        out = _run(REFERENCE_SOURCE, c)
        n, m, k = map(int, c.split()[:3])
        if n <= 6 and k <= 10:
            assert _run(BRUTE_SOURCE, c) == out, f"第 {i} 组参考解与暴力不一致"
        if n <= 100 and k <= 100 and m <= 1000:
            assert _run(GREEDY1_SOURCE, c) == out, f"第 {i} 组参考解与逐个贪心不一致"
        (root / f"{i}.in").write_text(c, encoding="utf-8")
        (root / f"{i}.out").write_text(out, encoding="utf-8")
    print(f"generated {len(cases)} cases")


if __name__ == "__main__":
    main()
