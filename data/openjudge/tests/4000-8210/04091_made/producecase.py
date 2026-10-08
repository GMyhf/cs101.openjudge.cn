"""4091 最近餐馆 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

2026-10 审计：原数据 n≤10、K≤3，询问点全是 (-20,...,-20)，距离并列屡见不鲜，
违反「最近的 M+1 家餐馆距离各不相同」的保证。改为：坐标取 [0,10000] 的整数，
每个询问都校验前 M+1 近的距离严格递增（不满足就重抽询问点），覆盖 K=1..5、
n 到 5000、t 到 10000（受 2MB 输出上限约束）、多组数据直到文件结束。
2026-10 体积收口：data/ 合计须 ≤10MB。满规模保留第 29 组（K=5、输出接近 2MB）与
第 31-33 组（t=10000 满额），其余大组 n 仍为 5000 但询问数按约 250KB 输出缩小。
答案由 samplecode.cpp（KD 树）给出。距离校验优先用 numpy（仅做整数运算，不影响随机序列）。
"""
import random
import subprocess
from pathlib import Path

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None

SAMPLE_IN = '3 2\n1 1\n1 3\n3 4\n2\n2 3\n2\n2 3\n1\n'
CMAX = 10000
IN_LIMIT = 1_000_000
OUT_LIMIT = 2_000_000
SMALL_OUT = 250_000  # 非满规模大组的输出预算，使 data/ 合计不超过 10MB


def as_array(points):
    return np.asarray(points, dtype=np.int64) if np is not None else points


def _sorted_d2(points, q):
    if np is not None:
        d = ((points - np.asarray(q, dtype=np.int64)) ** 2).sum(axis=1)
        return d
    return [sum((x - y) ** 2 for x, y in zip(p, q)) for p in points]


def unique_top(points, q, m):
    """前 m+1 近（不足则全体）的距离两两不同；points 须先经 as_array。"""
    d = _sorted_d2(points, q)
    k = min(m + 1, len(points))
    if np is not None:
        top = np.sort(np.partition(d, k - 1)[:k]) if k < len(points) else np.sort(d)
        return bool(np.all(top[1:] > top[:-1]))
    top = sorted(d)[:k]
    return all(top[i] < top[i + 1] for i in range(k - 1))


def valid(text):
    """题面契约：多组数据到 EOF；每组 n K（1≤n≤5000,1≤K≤5）、n 行 K 个坐标、t（1≤t≤10000）、
    t 个询问（K 个坐标一行 + M 一行，1≤M≤10）；坐标绝对值不超过 10000；
    最近的 M+1 家（M≤n）距离各不相同。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()

    def ints(line, cnt):
        parts = line.split()
        if len(parts) != cnt:
            return None
        try:
            v = [int(s) for s in parts]
        except ValueError:
            return None
        if any(s.startswith("+") for s in parts):
            return None
        return v

    pos = 0
    if not lines:
        return False
    while pos < len(lines):
        head = ints(lines[pos], 2); pos += 1
        if head is None:
            return False
        n, k = head
        if not (1 <= n <= 5000 and 1 <= k <= 5) or pos + n >= len(lines):
            return False
        pts = []
        for line in lines[pos:pos + n]:
            p = ints(line, k)
            if p is None or any(abs(x) > CMAX for x in p):
                return False
            pts.append(p)
        pos += n
        pts = as_array(pts)
        t = ints(lines[pos], 1); pos += 1
        if t is None or not 1 <= t[0] <= 10000 or pos + 2 * t[0] > len(lines):
            return False
        for _ in range(t[0]):
            q = ints(lines[pos], k)
            m = ints(lines[pos + 1], 1)
            pos += 2
            if q is None or m is None or any(abs(x) > CMAX for x in q):
                return False
            m = m[0]
            if not 1 <= m <= 10 or m > n or not unique_top(pts, q, m):
                return False
    return True


def rand_points(r, n, k, lo, hi, mode="uniform"):
    pts = []
    if mode == "mod3":
        # 一维满规模：点取 3 的倍数、询问点模 3 余 1/2，到所有点的距离两两不同
        return [[x] for x in r.sample(range(lo, hi + 1, 3), n)]
    if mode == "cluster":
        centers = [[r.randint(lo, hi) for _ in range(k)] for _ in range(r.randint(1, 4))]
        for _ in range(n):
            c = r.choice(centers)
            pts.append([min(hi, max(lo, x + r.randint(-60, 60))) for x in c])
    elif mode == "line":
        # 大多数点落在一条坐标轴附近，KD 树按该维切分时剪枝效果差
        for _ in range(n):
            p = [r.randint(lo, lo + 3) for _ in range(k)]
            p[0] = r.randint(lo, hi)
            pts.append(p)
    else:
        pts = [[r.randint(lo, hi) for _ in range(k)] for _ in range(n)]
    return pts


def make_dataset(r, n, k, t, lo=0, hi=CMAX, mode="uniform", mmax=10, qmode="mix"):
    pts = rand_points(r, n, k, lo, hi, mode)
    arr = as_array(pts)
    queries = []
    for _ in range(t):
        for _attempt in range(1000):
            m = r.randint(1, min(mmax, n))
            if r.random() < 0.3:
                m = min(mmax, n)
            pick = qmode if qmode != "mix" else r.choice(["near", "free", "corner"])
            if mode == "mod3":
                q = [r.randrange(lo, hi - 2, 3) + r.randint(1, 2)]
            elif pick == "near":
                base = r.choice(pts)
                q = [min(hi, max(lo, x + r.randint(-30, 30))) for x in base]
            elif pick == "corner":
                q = [r.choice([lo, hi]) for _ in range(k)]
                q = [min(hi, max(lo, x + r.randint(-5, 5))) for x in q]
            else:
                q = [r.randint(lo, hi) for _ in range(k)]
            if unique_top(arr, q, m):
                break
        else:
            raise AssertionError("找不到距离互异的询问点")
        queries.append((q, m))
    s = [f"{n} {k}"] + [" ".join(map(str, p)) for p in pts] + [str(t)]
    for q, m in queries:
        s.append(" ".join(map(str, q)))
        s.append(str(m))
    return "\n".join(s) + "\n"


def max_t(n, k, mmax, budget_in=IN_LIMIT, budget_out=OUT_LIMIT):
    """按 1MB 输入、2MB 输出估算可放下的最多询问数。"""
    per_out = 27 + mmax * k * 6
    per_in = k * 6 + 3
    room_in = budget_in - n * k * 6 - 20
    return max(1, min(10000, int(budget_out * 0.92) // per_out, int(room_in * 0.95) // per_in))


def build_cases():
    r = random.Random(4091)
    cases = [SAMPLE_IN]
    # 1 最小规模
    cases.append("1 1\n7\n1\n3\n1\n")
    # 2 K=1，多组数据，询问点在点集两侧与中间
    cases.append(make_dataset(r, 6, 1, 5, 0, 30) + make_dataset(r, 3, 1, 3, 0, 30) + make_dataset(r, 11, 1, 6, 0, 100))
    # 3-12 小规模随机：小坐标范围（易出并列，靠校验挑询问点），多组数据
    for i in range(3, 13):
        k = (i - 3) % 5 + 1
        c = "".join(make_dataset(r, r.randint(2, 30), k, r.randint(1, 20), 0, r.choice([20, 100, CMAX]))
                    for _ in range(r.randint(1, 3)))
        cases.append(c)
    # 13-20 中规模
    for i in range(13, 21):
        k = (i - 13) % 5 + 1
        n = r.randint(300, 1500)
        cases.append(make_dataset(r, n, k, r.randint(300, 1500),
                                  mode=["uniform", "cluster"][i % 2]))
    # 21-30 满规模单组：n=5000，K=1..5 各两组，t 取到文件上限（K 小时可到 10000）。
    # K=1 时坐标只有 10001 种取值，5000 个点必有大量对称并列，只能用 3 的倍数（最多 3334 个点）。
    for i in range(21, 31):
        k = (i - 21) // 2 + 1
        mode = "uniform" if i % 2 else "cluster"
        n = 5000
        if k == 1:
            mode, n = "mod3", 3334 if i % 2 else 2500
        mmax = 10
        # 体积控制：只有 i=29（K=5 均匀、满规模）保留到 2MB 输出上限，其余压到约 250KB 输出
        budget = OUT_LIMIT if i == 29 else SMALL_OUT
        cases.append(make_dataset(r, n, k, max_t(n, k, mmax, budget_out=budget), mode=mode, mmax=mmax))
    # 31-33 t=10000 满额（M 较小以压住输出）
    for i, k in zip(range(31, 34), (2, 3, 5)):
        cases.append(make_dataset(r, 5000, k, 10000, mmax=2 if k < 5 else 1))
    # 34-36 退化分布：点贴在一条线上 / 高维聚团，询问来自角落
    cases.append(make_dataset(r, 5000, 5, max_t(5000, 5, 10, budget_out=SMALL_OUT), mode="line"))
    cases.append(make_dataset(r, 5000, 4, max_t(5000, 4, 10, budget_out=SMALL_OUT), mode="cluster", qmode="corner"))
    cases.append(make_dataset(r, 5000, 3, max_t(5000, 3, 10, budget_out=SMALL_OUT), mode="line", qmode="free"))
    # 37-39 多组数据，每组都较大（漏清空上一组的写法会错）
    for i in range(37, 40):
        parts = []
        for _ in range(3):
            k = r.randint(2, 5)
            parts.append(make_dataset(r, r.randint(1500, 1700), k, max_t(1700, k, 10, budget_out=SMALL_OUT) // 3, mode="uniform"))
        cases.append("".join(parts))
    return cases


def main():
    root = Path(__file__).parent
    binary = root / "reference"
    subprocess.run(["g++", "-std=c++17", "-O2", str(root / "samplecode.cpp"), "-o", str(binary)], check=True)
    try:
        cases = build_cases()
        assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
        (root / "data").mkdir(exist_ok=True)
        for i, c in enumerate(cases):
            assert valid(c), f"第 {i} 组不满足题面约束"
            p = subprocess.run([str(binary)], input=c, text=True, capture_output=True, check=True)
            (root / "data" / f"{i}.in").write_text(c)
            (root / "data" / f"{i}.out").write_text(p.stdout)
    finally:
        binary.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
