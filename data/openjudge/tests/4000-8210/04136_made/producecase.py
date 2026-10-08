import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'r=int(input())\nn=int(input())\nrects=[]\narea=0\nfor _ in range(n):\n    l,t,w,h=[int(i) for i in input().split()]\n    rects.append((l,l+w,h))\n    area+=w*h\nleft=0\nright=r\nwhile True:\n    if right-left<=1:\n        ans=right\n        break\n    mid=left+(right-left)//2\n    half=0\n    for le,ri,we in rects:\n        if ri<=mid:\n            half+=(ri-le)*we\n        elif ri>mid and le<mid:\n            half+=(mid-le)*we\n    if half*2>=area:\n        right=mid\n    else:\n        left=mid\nleft=ans\nright=r+1\nwhile True:\n\n    if right-left<=1:\n        fans=left\n        break\n    mid=left+(right-left)//2\n    ahalf=0\n    for le,ri,we in rects:\n        if ri<=ans:\n            pass\n        elif ri<=mid:\n            ahalf+=(ri-le)*we\n        elif ri>mid and le<mid:\n            ahalf+=(mid-le)*we\n    if ahalf==0:\n        left=mid\n    else:\n        right=mid\n    \nprint(fans)'
SAMPLE = '1000\n2\n1 1 2 1\n5 1 2 1\n'


def valid(text):
    """题面：R（1≤R≤1e6）；N（0<N≤10000）；N 行 L T W H（0≤L,T≤R，0<W,H≤R），
    (L,T) 为左上角，小矩形不出大矩形（L+W≤R，T-H≥0），小矩形两两不重叠（边可相接）。"""
    import bisect
    if not text.endswith("\n"):
        return False
    Ls = text[:-1].split("\n")
    isint = lambda x: x.isdigit() and (x == "0" or x[0] != "0")
    if len(Ls) < 2 or not isint(Ls[0]) or not isint(Ls[1]):
        return False
    R, n = int(Ls[0]), int(Ls[1])
    if not (1 <= R <= 10 ** 6 and 0 < n <= 10000) or len(Ls) != n + 2:
        return False
    ev = []
    for line in Ls[2:]:
        t = line.split(" ")
        if len(t) != 4 or not all(isint(x) for x in t):
            return False
        l, top, w, h = map(int, t)
        if not (0 <= l <= R and 0 <= top <= R and 0 < w <= R and 0 < h <= R):
            return False
        if l + w > R or top - h < 0:
            return False
        ev.append((l, 1, top - h, top))
        ev.append((l + w, 0, top - h, top))
    ev.sort()  # 同一 x 先删后加：边相接不算重叠
    act = []  # 当前活跃的 y 区间（互不相交），按下端排序
    for x, kind, y0, y1 in ev:
        if kind == 0:
            act.pop(bisect.bisect_left(act, (y0, y1)))
        else:
            k = bisect.bisect_left(act, (y0, y1))
            if k < len(act) and act[k][0] < y1:
                return False
            if k > 0 and act[k - 1][1] > y0:
                return False
            act.insert(k, (y0, y1))
    return True


def fmt(R, rects):
    return f"{R}\n{len(rects)}\n" + "".join(f"{l} {t} {w} {h}\n" for l, t, w, h in rects)


def cuts(r, lo, hi, k):
    """把 [lo,hi] 切成 k 段（长度不足时尽量多）。"""
    k = min(k - 1, hi - lo - 1)
    return [lo] + sorted(r.sample(range(lo + 1, hi), k)) + [hi] if k > 0 else [lo, hi]


def grid(r, R, cols, rows, keep=0.8, shrink=0.5, x0=0, x1=None):
    """把 [x0,x1]×[0,R] 切成列、每列再切成格，格内放一个（可能缩小的）矩形，保证互不重叠。"""
    x1 = R if x1 is None else x1
    out = []
    xs = cuts(r, x0, x1, cols)
    for i in range(len(xs) - 1):
        ys = cuts(r, 0, R, rows)
        for j in range(len(ys) - 1):
            if r.random() > keep:
                continue
            a, b, c, d = xs[i], xs[i + 1], ys[j], ys[j + 1]
            if r.random() < shrink:
                a2 = r.randint(a, b - 1); b2 = r.randint(a2 + 1, b)
                c2 = r.randint(c, d - 1); d2 = r.randint(c2 + 1, d)
                a, b, c, d = a2, b2, c2, d2
            out.append((a, d, b - a, d - c))
    r.shuffle(out)
    return out


def old(r):
    """原生成器的形状，但把 T 修正到 [H, size]，保证小矩形不越出大矩形下边界。"""
    size = r.randint(8, 40); cs = sorted(r.sample(range(1, size), r.randint(1, min(6, size - 1))))
    b = [0] + cs + [size]
    z = []
    for i in range(len(b) - 1):
        h = r.randint(1, size - 1)
        z.append((b[i], r.randint(h, size), b[i + 1] - b[i], h))
    return fmt(size, z)


def gen(i):
    r = random.Random(4136 * 1000 + i)
    if i == 1:
        return "1\n1\n0 1 1 1\n"
    if i == 2:  # 唯一矩形贴右边界，答案 R
        return "10\n1\n9 10 1 10\n"
    if i == 3:  # 恰好平分且右侧有空隙：应延伸到下一矩形左边
        return fmt(100, [(0, 10, 10, 10), (50, 10, 10, 10)])
    if i == 4:  # 只有走过全部矩形才满足左≥右，右侧整片空白：答案 R
        return fmt(100, [(0, 1, 1, 1), (1, 3, 1, 3)])
    if i == 5:  # 直线必须切开矩形
        return fmt(100, [(10, 100, 81, 100)])
    if i == 6:  # 左边空白，矩形集中在右端
        return fmt(10 ** 6, [(999990, 10 ** 6, 10, 10 ** 6)])
    if i == 7:  # 面积达 1e12，卡 32 位整型
        return fmt(10 ** 6, [(0, 10 ** 6, 10 ** 6, 10 ** 6)])
    if i == 8:
        return fmt(10 ** 6, [(0, 10 ** 6, 400000, 10 ** 6), (400000, 10 ** 6, 600000, 10 ** 6)])
    if i <= 19:
        return old(r)
    if i <= 27:  # 小中规模网格
        R = r.choice([20, 100, 1000])
        return fmt(R, grid(r, R, r.randint(1, 8), r.randint(1, 5), keep=r.choice([0.3, 0.8, 1.0])) or [(0, R, 1, 1)])
    R = 10 ** 6
    if i == 28:  # N=10000，铺满整个大矩形，面积 1e12
        return fmt(R, grid(r, R, 100, 100, keep=1.0, shrink=0.0))
    if i == 29:  # N 接近上限，稀疏
        return fmt(R, grid(r, R, 125, 100, keep=0.8))
    if i == 30:  # 一半矩形在左边很窄的带里，右半有大空隙
        a = grid(r, R, 50, 100, keep=1.0, shrink=0.0, x0=0, x1=1000)
        return fmt(R, a + [(999000, R, 1000, R)])
    if i == 31:  # 平衡点处右侧有大空隙，答案应跳到下一矩形左边
        a = grid(r, R, 60, 80, keep=1.0, shrink=0.0, x0=0, x1=300000)
        b = [(l + 700000, t, w, h) for l, t, w, h in a]
        return fmt(R, a + b)
    if i == 32:  # 很多高度为 1 的细条
        return fmt(R, grid(r, R, 10, 1000, keep=1.0, shrink=0.3))
    return fmt(R, grid(r, R, r.randint(50, 125), r.randint(50, 80), keep=r.choice([0.5, 0.9, 1.0]), shrink=r.random()))


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
