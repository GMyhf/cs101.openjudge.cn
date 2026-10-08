"""4037 聪明的质监员 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

2026-10 审计重写：
- 原生成器 n<=30、S 可取 0、区间 L>R 都会出现，越出题面「0<S」「L<=R」约束，且规模远小于
  n,m<=200000；原参考解（也是原 samplecode）是 O(maxw*n*m) 暴力，而且只枚举 W∈[0,maxw]，
  漏掉 W>maxw（Y=0、答案为 S）这一支。
- 现参考解：Y(W) 对 W 单调不增，二分 W∈[1,maxw+1]，每次前缀和 O(n+m)。
- BRUTE_SOURCE 为独立暴力（枚举全部候选 W，逐区间直接求和），每次生成都对全部小规模组对拍。
- 大组保证 Y 的最大值 < 9.2e18（64 位有符号可存），同时远超 2^31，卡 int32 溢出。
"""
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path

NUMBER = 4037
SAMPLE_IN = '5 3 15 \n1 5 \n2 5 \n3 5 \n4 5 \n5 5 \n1 5 \n2 4 \n3 3\n'
SAMPLE_OUT = '10\n'

REFERENCE_SOURCE = r'''import sys
from itertools import accumulate
def main():
    data = sys.stdin.buffer.read().split()
    n, m, S = int(data[0]), int(data[1]), int(data[2])
    w = list(map(int, data[3:3 + 2 * n:2]))
    v = list(map(int, data[4:4 + 2 * n:2]))
    base = 3 + 2 * n
    L = list(map(int, data[base:base + 2 * m:2]))
    R = list(map(int, data[base + 1:base + 2 * m:2]))
    def Y(W):
        c = [0] + list(accumulate(1 if x >= W else 0 for x in w))
        s = [0] + list(accumulate(y if x >= W else 0 for x, y in zip(w, v)))
        return sum((c[r] - c[l - 1]) * (s[r] - s[l - 1]) for l, r in zip(L, R))
    lo, hi = 1, max(w) + 1          # Y(maxw+1)=0<=S，找最小的 W 使 Y(W)<=S
    while lo < hi:
        mid = (lo + hi) // 2
        if Y(mid) <= S:
            hi = mid
        else:
            lo = mid + 1
    ans = S - Y(lo)
    if lo > 1:
        ans = min(ans, Y(lo - 1) - S)
    print(ans)
main()
'''

BRUTE_SOURCE = r'''import sys
a = sys.stdin.read().split()
n, m, S = int(a[0]), int(a[1]), int(a[2])
w = [int(a[3 + 2 * i]) for i in range(n)]
v = [int(a[4 + 2 * i]) for i in range(n)]
q = [(int(a[3 + 2 * n + 2 * i]), int(a[4 + 2 * n + 2 * i])) for i in range(m)]
best = None
for W in sorted(set(w) | {max(w) + 1, 0}):
    tot = 0
    for l, r in q:
        cnt = sum(1 for j in range(l - 1, r) if w[j] >= W)
        sv = sum(v[j] for j in range(l - 1, r) if w[j] >= W)
        tot += cnt * sv
    d = abs(tot - S)
    best = d if best is None else min(best, d)
print(best)
'''

N_MAX = 200000
V_MAX = 10 ** 6
S_MAX = 10 ** 12
Y_LIMIT = 9 * 10 ** 18


def valid(text):
    """严格按题面：第一行 n m S；n 行 w v；m 行 L R。
    1<=n,m<=200000，0<w,v<=1e6，0<S<=1e12，1<=L<=R<=n。"""
    try:
        lines = text.split("\n")
        while lines and lines[-1].strip() == "":
            lines.pop()
        rows = [ln.split() for ln in lines]
        if not rows or len(rows[0]) != 3:
            return False
        n, m, S = map(int, rows[0])
        if not (1 <= n <= N_MAX and 1 <= m <= N_MAX and 0 < S <= S_MAX):
            return False
        if len(rows) != 1 + n + m:
            return False
        for i in range(1, 1 + n):
            if len(rows[i]) != 2:
                return False
            w, v = map(int, rows[i])
            if not (0 < w <= V_MAX and 0 < v <= V_MAX):
                return False
        for i in range(1 + n, 1 + n + m):
            if len(rows[i]) != 2:
                return False
            l, r = map(int, rows[i])
            if not (1 <= l <= r <= n):
                return False
        return True
    except ValueError:
        return False


def y_max(text):
    a = text.split()
    n, m = int(a[0]), int(a[1])
    v = [int(a[4 + 2 * i]) for i in range(n)]
    pre = [0]
    for x in v:
        pre.append(pre[-1] + x)
    tot = 0
    for i in range(m):
        l, r = int(a[3 + 2 * n + 2 * i]), int(a[4 + 2 * n + 2 * i])
        tot += (r - l + 1) * (pre[r] - pre[l - 1])
    return tot


def y_of(text, W):
    a = text.split()
    n, m = int(a[0]), int(a[1])
    w = [int(a[3 + 2 * i]) for i in range(n)]
    v = [int(a[4 + 2 * i]) for i in range(n)]
    c = [0]; s = [0]
    for x, y in zip(w, v):
        c.append(c[-1] + (x >= W)); s.append(s[-1] + (y if x >= W else 0))
    tot = 0
    for i in range(m):
        l, r = int(a[3 + 2 * n + 2 * i]), int(a[4 + 2 * n + 2 * i])
        tot += (c[r] - c[l - 1]) * (s[r] - s[l - 1])
    return tot


def fmt(n, m, S, wv, qs):
    return (f"{n} {m} {S}\n" + "\n".join(f"{w} {v}" for w, v in wv) + "\n"
            + "\n".join(f"{l} {r}" for l, r in qs) + "\n")


def gen(r, n, m, wmax, vmax, maxlen, s_mode):
    """s_mode: 'rand' 随机 S；'hit' S 恰为某个 Y(W)（答案 0）；'tiny' S 很小（最优常落在 W>maxw）；
    'huge' S 取上限附近（最优在 W 很小一侧）。"""
    wv = [(r.randint(1, wmax), r.randint(1, vmax)) for _ in range(n)]
    qs = []
    for _ in range(m):
        ln = r.randint(1, min(maxlen, n))
        l = r.randint(1, n - ln + 1)
        qs.append((l, l + ln - 1))
    body = fmt(n, m, 1, wv, qs)
    ymax = y_max(body)
    assert ymax < Y_LIMIT, ymax
    if s_mode == "tiny":
        S = r.randint(1, 3)
    elif s_mode == "huge":
        S = r.randint(S_MAX // 2, S_MAX)
    elif s_mode == "hit":
        ws = sorted({w for w, _ in wv})
        W = r.choice(ws)
        S = y_of(body, W)
        if not (0 < S <= S_MAX):
            S = r.randint(1, min(S_MAX, max(1, ymax)))
    else:
        S = r.randint(1, min(S_MAX, max(1, ymax)))
    return fmt(n, m, S, wv, qs)


def build_cases():
    cases = [SAMPLE_IN]
    r = random.Random(NUMBER)
    # 最小规模
    cases.append("1 1 1\n1 1\n1 1\n")                    # Y=1，答案 0
    cases.append("1 1 1000000000000\n1000000 1000000\n1 1\n")   # 上界 S、w、v
    cases.append("2 1 7\n3 2\n3 2\n1 2\n")               # 全部相同重量
    # 小规模随机（与暴力对拍），覆盖各种 S 取法
    modes = ["rand", "hit", "tiny", "huge"]
    for i in range(16):
        n = r.randint(1, 12); m = r.randint(1, 12)
        cases.append(gen(r, n, m, r.choice([3, 10, 10 ** 6]), r.choice([5, 10 ** 6]), n, modes[i % 4]))
    # 中等规模
    for i in range(8):
        n = r.randint(300, 3000); m = r.randint(300, 3000)
        cases.append(gen(r, n, m, r.choice([50, 10 ** 6]), 10 ** 6, n, modes[i % 4]))
    # 大规模：受「单组 .in<=1MB」所限，值域取满时 n=m=35000；n 取满 200000 时 w,v 取个位数、m 收小。
    # 体积收口（data/ 合计 ≤10MB）：满规模只保留 n=m=35000 值域取满、n=200000、m=200000、
    # 40000×30000 四类，其余大组规模减半。
    # 区间长度受限以保证 Y<9.2e18；仍远超 2^31，并能卡掉 O(nm) 与逐个枚举 W 的 O(maxw*(n+m))。
    big = [
        (35000, 35000, 10 ** 6, 10 ** 6, 20000, "rand"),
        (17500, 17500, 10 ** 6, 10 ** 6, 10000, "hit"),
        (17500, 17500, 10 ** 6, 10 ** 6, 10000, "tiny"),
        (17500, 17500, 10 ** 6, 10 ** 6, 10000, "huge"),
        (17500, 17500, 10 ** 6, 10 ** 6, 300, "rand"),
        (17000, 17000, 1000, 10 ** 6, 8000, "hit"),
        (200000, 15000, 9, 9, 200000, "rand"),
        (100000, 15000, 9, 9, 100000, "hit"),
        (200000, 1, 9, 9, 200000, "tiny"),
        (1, 200000, 10 ** 6, 10 ** 6, 1, "rand"),
        (30000, 12500, 9, 10 ** 6, 10000, "huge"),
        (40000, 30000, 10 ** 6, 10 ** 6, 5, "hit"),
    ]
    for n, m, wmax, vmax, maxlen, mode in big:
        cases.append(gen(r, n, m, wmax, vmax, maxlen, mode))
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
        if len(c) < 2000:
            assert _run(BRUTE_SOURCE, c) == out, f"第 {i} 组参考解与暴力不一致"
        (root / f"{i}.in").write_text(c, encoding="utf-8")
        (root / f"{i}.out").write_text(out, encoding="utf-8")
    print(f"generated {len(cases)} cases")


if __name__ == "__main__":
    main()
