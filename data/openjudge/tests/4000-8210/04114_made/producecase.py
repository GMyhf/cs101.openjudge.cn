"""04114 Segments 测试数据生成器：固定种子，重跑逐字节可复现。

第 0 组是题面样例。期望输出由 samplecode.cpp（平台 AC 解，已补「所有端点重合」的特判）
算出，并与本文件里的 Python 解逐组比对。坐标都取一位小数，避开 1e-8 量级的精度歧义。
覆盖：n=1、n=2（必 Yes）、退化成点的线段、所有端点重合（Yes）、共线、
只有经过端点（恰好擦边）的直线才可行、Yes/No 混合、n=100 的规模组。
"""
import random
import re
import subprocess
from pathlib import Path

SAMPLE_IN = ('3\n2\n1.0 2.0 3.0 4.0\n4.0 5.0 6.0 7.0\n3\n0.0 0.0 0.0 1.0\n0.0 1.0 0.0 2.0\n'
             '1.0 1.0 2.0 1.0\n3\n0.0 0.0 0.0 1.0\n0.0 2.0 0.0 3.0\n1.0 1.0 2.0 1.0\n')
SAMPLE_OUT = 'Yes!\nYes!\nNo!\n'
EPS = 1e-8
NUM = r"-?\d+(\.\d+)?"


def valid(text):
    """题面契约：首行正整数 T；随后 T 组，每组首行正整数 n（n<=100），接着恰 n 行，
    每行 4 个实数 x1 y1 x2 y2。不允许多余内容。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    t = int(lines[0])
    pos = 1
    for _ in range(t):
        if pos >= len(lines) or not re.fullmatch(r"[1-9]\d*", lines[pos]):
            return False
        n = int(lines[pos])
        if n > 100 or pos + 1 + n > len(lines):
            return False
        for line in lines[pos + 1:pos + 1 + n]:
            parts = line.split(" ")
            if len(parts) != 4 or not all(re.fullmatch(NUM, x) for x in parts):
                return False
        pos += 1 + n
    return pos == len(lines)


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def one(segs):
    pts = [p for s in segs for p in s]
    distinct = False
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            a, b = pts[i], pts[j]
            if abs(a[0] - b[0]) < EPS and abs(a[1] - b[1]) < EPS:
                continue
            distinct = True
            if all(cross(a, b, p) * cross(a, b, q) < EPS for p, q in segs):
                return True
    return not distinct  # 所有端点重合：投影后都是同一点


def solve(text):
    a = text.split()
    pos = 1
    out = []
    for _ in range(int(a[0])):
        n = int(a[pos]); pos += 1
        segs = []
        for _ in range(n):
            x1, y1, x2, y2 = map(float, a[pos:pos + 4]); pos += 4
            segs.append(((x1, y1), (x2, y2)))
        out.append("Yes!" if one(segs) else "No!")
    return "\n".join(out) + "\n"


def f(v):
    return "%.1f" % v


def fmt(tests):
    out = [str(len(tests))]
    for segs in tests:
        out.append(str(len(segs)))
        out += [" ".join(f(c) for p in s for c in p) for s in segs]
    return "\n".join(out) + "\n"


def rp(r, lo=-100, hi=100):
    return (r.randint(lo * 10, hi * 10) / 10, r.randint(lo * 10, hi * 10) / 10)


def random_segs(r, n, length):
    segs = []
    for _ in range(n):
        p = rp(r)
        q = (round(p[0] + r.uniform(-length, length), 1), round(p[1] + r.uniform(-length, length), 1))
        segs.append((p, q))
    return segs


def stabbed(r, n, touch=0.3):
    """先取一条直线（过两个格点），再造与它相交的线段；部分线段只用端点擦到这条线。"""
    a = (float(r.randint(-50, 50)), float(r.randint(-50, 50)))
    b = (a[0] + r.randint(-20, 20), a[1] + r.randint(1, 20))
    dx, dy = b[0] - a[0], b[1] - a[1]
    segs = []
    for _ in range(n):
        k = r.randint(-5, 5)
        on = (a[0] + k * dx, a[1] + k * dy)      # 直线上的格点
        if r.random() < touch:
            p = on
        else:
            t = r.random()
            ex, ey = r.uniform(-30, 30), r.uniform(-30, 30)
            p = (round(on[0] + t * ex, 1), round(on[1] + t * ey, 1))
            q = (round(on[0] - (1 - t) * ex, 1), round(on[1] - (1 - t) * ey, 1))
            segs.append((p, q) if r.random() < .5 else (q, p))
            continue
        q = (round(on[0] + r.uniform(-30, 30), 1), round(on[1] + r.uniform(-30, 30), 1))
        segs.append((p, q) if r.random() < .5 else (q, p))
    r.shuffle(segs)
    return segs


def build_cases(r):
    P = lambda x, y: (float(x), float(y))
    cases = [SAMPLE_IN]
    cases.append(fmt([[(P(0, 0), P(1, 1))]]))                                        # n=1
    cases.append(fmt([[(P(0, 0), P(0, 0))]]))                                        # n=1 退化为点
    cases.append(fmt([[(P(0, 0), P(1, 0)), (P(100, 100), P(-100, 37))]]))           # n=2 必 Yes
    cases.append(fmt([[(P(3, 3), P(3, 3))] * 3, [(P(1.5, 2), P(1.5, 2))] * 100]))    # 全部端点重合 -> Yes
    cases.append(fmt([[(P(0, 0), P(0, 0)), (P(1, 1), P(1, 1)), (P(2, 2), P(2, 2))],  # 三点共线 -> Yes
                      [(P(0, 0), P(0, 0)), (P(1, 1), P(1, 1)), (P(2, 2.1), P(2, 2.1))]]))  # 不共线 -> No
    cases.append(fmt([[(P(0, 0), P(1, 0)), (P(2, 0), P(3, 0)), (P(4, 0), P(5, 0))],  # 同一直线上互不重叠
                      [(P(0, 0), P(0, 1)), (P(1, 1), P(1, 2)), (P(2, 2), P(2, 3)), (P(3, 3), P(3, 4.1))]]))
    # 只有擦着端点的直线可行：三条竖线段端点恰在 y=x 上
    cases.append(fmt([[(P(0, 0), P(0, -5)), (P(1, 1), P(1, 6)), (P(2, 2), P(2, -3)), (P(3, 3), P(3, 9))],
                      [(P(0, 0), P(0, -5)), (P(1, 1.1), P(1, 6)), (P(2, 2), P(2, -3)), (P(3, 3), P(3, 9))]]))
    cases.append(fmt([[(P(0, 0), P(10, 0)), (P(0, 1), P(10, 1)), (P(0, 2), P(10, 2))],  # 平行线段
                      [(P(0, 0), P(1, 0)), (P(5, 0), P(6, 0)), (P(0, 5), P(1, 5)), (P(5, 5), P(6, 5)),
                       (P(2.5, 10), P(3.5, 10)), (P(2.5, -5), P(3.5, -5))]]))
    for _ in range(8):
        cases.append(fmt([random_segs(r, 3, 20) for _ in range(r.randint(3, 10))]))
    for _ in range(6):
        cases.append(fmt([stabbed(r, r.randint(3, 20)) if r.random() < .5 else random_segs(r, r.randint(3, 20), 60)
                          for _ in range(r.randint(3, 10))]))
    for _ in range(5):
        cases.append(fmt([stabbed(r, r.randint(10, 60), 0.6) for _ in range(r.randint(2, 5))]))
    # 规模组：n=100；No 组要枚举全部点对，Python 每组约 2e6 次叉积
    cases.append(fmt([stabbed(r, 100), stabbed(r, 100, 0.9), random_segs(r, 100, 150)]))
    cases.append(fmt([random_segs(r, 100, 3), random_segs(r, 100, 200)]))
    cases.append(fmt([stabbed(r, 100, 0.5) for _ in range(3)]))
    # n=100 且仅最后一条线段把 Yes 变成 No
    s = stabbed(r, 99, 0.5)
    cases.append(fmt([s + [((150.0, 150.0), (150.0, 150.1))], s + [(s[0][0], s[0][0])]]))
    while len(cases) < 40:
        cases.append(fmt([stabbed(r, r.randint(3, 8)) if r.random() < .5 else random_segs(r, r.randint(3, 8), 30)
                          for _ in range(r.randint(1, 6))]))
    return cases


def main():
    root = Path(__file__).parent
    binary = root / "reference"
    subprocess.run(["g++", "-std=c++17", "-O2", str(root / "samplecode.cpp"), "-o", str(binary)], check=True)
    try:
        cases = build_cases(random.Random(4114))
        assert cases[0] == SAMPLE_IN and solve(SAMPLE_IN) == SAMPLE_OUT
        assert len(cases) == 40 and len(set(cases)) == len(cases)
        (root / "data").mkdir(exist_ok=True)
        for i, c in enumerate(cases):
            assert valid(c), i
            p = subprocess.run([str(binary)], input=c, text=True, capture_output=True, check=True)
            assert p.stdout.split() == solve(c).split(), i
            (root / "data" / f"{i}.in").write_text(c)
            (root / "data" / f"{i}.out").write_text(p.stdout)
    finally:
        binary.unlink()


if __name__ == "__main__":
    main()
