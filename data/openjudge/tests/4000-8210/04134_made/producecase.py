import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'n = int(input())\narr = list(map(int, input().split()))\nm = int(input())\n\nfor _ in range(m):\n    x = int(input())\n\n    # --- 手写二分（不能使用函数） ---\n    l, r = 0, n-1\n    while l <= r:\n        mid = (l + r) // 2\n        if arr[mid] < x:\n            l = mid + 1\n        else:\n            r = mid - 1\n    pos = l\n    # --- 二分结束 ---\n\n    candidates = []\n    if pos < n:\n        candidates.append(arr[pos])\n    if pos > 0:\n        candidates.append(arr[pos - 1])\n\n    # 选和 x 最接近的，如果差一样，取较小的\n    best = min(candidates, key=lambda v: (abs(v - x), v))\n\n    print(best)'
SAMPLE = '3\n2 5 8\n2\n10\n5\n'


def valid(text):
    """题面：n（1≤n≤100000）；n 个非降整数（0..1e9）；m（1≤m≤10000）；m 行各一个整数（0..1e9）。"""
    if not text.endswith("\n"):
        return False
    L = text[:-1].split("\n")
    def isint(x):
        return x.isdigit() and (x == "0" or x[0] != "0")
    if len(L) < 3 or not isint(L[0]):
        return False
    n = int(L[0])
    if not 1 <= n <= 100000:
        return False
    t = L[1].split(" ")
    if len(t) != n or not all(isint(x) for x in t):
        return False
    a = list(map(int, t))
    if any(not 0 <= x <= 10 ** 9 for x in a) or any(a[i] > a[i + 1] for i in range(n - 1)):
        return False
    if not isint(L[2]):
        return False
    m = int(L[2])
    if not 1 <= m <= 10000 or len(L) != 3 + m:
        return False
    return all(isint(x) and int(x) <= 10 ** 9 for x in L[3:])


def fmt(a, q):
    return f"{len(a)}\n{' '.join(map(str, a))}\n{len(q)}\n" + "".join(f"{x}\n" for x in q)


def queries(r, a, m, hi):
    """混合：命中元素、相邻两元素正中间（并列取小）、中间偏一、越过两端、随机。"""
    q = []
    for _ in range(m):
        t = r.randrange(6)
        i = r.randrange(len(a))
        if t == 0:
            x = a[i]
        elif t in (1, 2) and i + 1 < len(a) and (a[i] + a[i + 1]) % 2 == 0:
            x = (a[i] + a[i + 1]) // 2 + (0 if t == 1 else r.choice([-1, 1]))
        elif t == 3:
            x = r.randint(0, a[0]) if r.random() < 0.5 else r.randint(a[-1], hi)
        else:
            x = r.randint(0, hi)
        q.append(min(max(x, 0), hi))
    return q


def gen(i):
    r = random.Random(4134 * 1000 + i)
    if i == 1:
        return fmt([7], [7])
    if i == 2:
        return fmt([0], [10 ** 9, 0, 5])
    if i == 3:
        return fmt([10 ** 9], [0, 10 ** 9, 999999999])
    if i == 4:  # 并列取较小
        return fmt([1, 3], [2, 0, 4, 1, 3])
    if i == 5:  # 全部相等
        return fmt([5] * 10, [0, 5, 10, 10 ** 9])
    if i == 6:  # 两端极值
        return fmt([0, 0, 10 ** 9, 10 ** 9], [500000000, 499999999, 500000001, 0, 10 ** 9])
    if i <= 19:  # 小规模，含重复元素
        n = r.randint(2, 30); hi = r.choice([20, 300, 10 ** 9])
        a = sorted(r.randint(0, hi) for _ in range(n))
        return fmt(a, queries(r, a, r.randint(1, 30), hi))
    if i <= 27:  # 中规模
        n = r.randint(1000, 30000); hi = r.choice([10 ** 5, 10 ** 9])
        a = sorted(r.randint(0, hi) for _ in range(n))
        return fmt(a, queries(r, a, r.randint(1000, 10000), hi))
    # 大规模 m=1e4（卡 O(nm) 线性扫描）。.in 需 ≤1MB：元素取到 1e9 量级时 n 取 85000，
    # n 取满 1e5 时元素压在 1e6 以内（查询仍可到 1e9）。
    # 体积收口（data/ 合计 ≤10MB）：满规模只留 28/29/31 三组，其余大组 n 缩到 30000，m 仍为 1e4。
    m, hi = 10000, 10 ** 9
    if i == 28:
        n = 85000; a = sorted(r.sample(range(0, hi + 1, 2), n))  # 全偶数，制造大量正中间并列
    elif i == 29:
        n = 100000; a = sorted(r.randint(0, 1000) for _ in range(n))  # 大量重复
    elif i == 30:
        n = 30000; a = [hi - 2 * (n - 1) + 2 * k for k in range(n)]  # 挤在上端
    elif i == 31:
        n = 100000; a = list(range(0, 2 * n, 2))  # 挤在下端，查询多数越过最大值
    elif i <= 35:
        n = 30000; a = sorted(r.randint(0, hi) for _ in range(n))
    else:
        n = 30000; a = sorted(r.randint(0, 10 ** 6) for _ in range(n))
    return fmt(a, queries(r, a, m, hi))


def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[gen(i) for i in range(1, 40)]
    assert all(valid(c) and len(c) <= 10 ** 6 for c in cases) and len(set(cases)) == len(cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
