"""Codeforces 2195H checker (answers are not unique).

Written for this repository as a hand-off artifact; no external license.
python3 -I checker.py <input> <contestant_output> <reference_answer>; exit 0 = AC, 42 = WA.

The optimum is recomputed from n (the reference file is not read): 2 for n = 1
(exhaustive search), 3n^2 for n >= 2 (3n^2 is the point-count bound 9n^2/3 and the
reference construction reaches it).  Per test the contestant must print m equal to the
optimum and then m triangles of 6 integers in [1, 3n] with |cross| = 1 (area 1/2), all
3m vertices pairwise distinct.  Nothing may follow the last test.

Disjointness.  A unit-area lattice triangle contains no lattice point besides its
vertices, and all vertices are distinct, so every triangle has integer vertex rows and
intersects each horizontal strip c <= y <= c+1 it spans in a trapezoid given by its
bottom interval [Lb, Rb] on y = c and top interval [Lt, Rt] on y = c+1.  Two closed
triangles intersect iff in some strip their trapezoids intersect (touching on a strip
line lies in the strip of both, or is at a lattice point, already excluded).  Sorted by
Lb, the trapezoids of a strip are pairwise disjoint iff every consecutive pair has
Rb < Lb' and Rt < Lt' (by linear interpolation in between).  Crossing x-coordinates are
p/q with q <= 497; int/int true division is correctly rounded, so equal rationals give
equal floats and distinct ones differ by >= 1/497^2, far above float error.
Work is the total row span of the triangles (the square is transposed first if the
column span is smaller); memory is the triangles plus one strip at a time.
"""
import sys


def wa(msg):
    print(msg)
    sys.exit(42)


def to_int(tok):
    if not 0 < len(tok) <= 12:
        return None
    s = tok[1:] if tok[:1] == b"-" else tok
    if not s or not s.isdigit():
        return None
    return int(tok)


def check_test(case, n, out, p, total):
    s = 3 * n
    best = 2 if n == 1 else 3 * n * n
    if p >= total:
        wa(f"第 {case} 组测试：输出不完整")
    m = to_int(out[p]); p += 1
    if m is None:
        wa(f"第 {case} 组测试：三角形个数不是整数")
    if m != best:
        wa(f"第 {case} 组测试：三角形个数不是最大值")
    if p + 6 * m > total:
        wa(f"第 {case} 组测试：三角形数量少于给出的 m")
    used = bytearray(s * s)
    tris = []
    spany = spanx = 0
    for _ in range(m):
        v = [to_int(out[p + k]) for k in range(6)]
        p += 6
        for c in v:
            if c is None or not 1 <= c <= s:
                wa(f"第 {case} 组测试：顶点坐标不是 [1, 3n] 内的整数")
        x1, y1, x2, y2, x3, y3 = v
        cr = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        if cr != 1 and cr != -1:
            wa(f"第 {case} 组测试：有三角形面积不是 1/2")
        for x, y in ((x1, y1), (x2, y2), (x3, y3)):
            k = (x - 1) * s + (y - 1)
            if used[k]:
                wa(f"第 {case} 组测试：有两个三角形共用顶点")
            used[k] = 1
        spany += max(y1, y2, y3) - min(y1, y2, y3)
        spanx += max(x1, x2, x3) - min(x1, x2, x3)
        tris.append(v)
    if spanx < spany:
        tris = [(y1, x1, y2, x2, y3, x3) for x1, y1, x2, y2, x3, y3 in tris]
    # strips are swept bottom to top; only triangles spanning the current strip are held
    starts = [[] for _ in range(s + 1)]
    for x1, y1, x2, y2, x3, y3 in tris:
        (ya, xa), (yb, xb), (yc, xc) = sorted(((y1, x1), (y2, x2), (y3, x3)))
        starts[ya].append((yc, yb, xa, xb, xc, xc - xa, yc - ya))
    del tris
    active = []
    for c in range(1, s):
        if starts[c]:
            active.extend(starts[c])
        if not active:
            continue
        row = []
        keep = []
        for tri in active:
            yc, yb, xa, xb, xc, dxl, dyl = tri
            # long edge A-C at y = c and y = c + 1 (exact numerators, one division)
            l0 = (xa * dyl + dxl * (c - yc + dyl)) / dyl
            l1 = (xa * dyl + dxl * (c + 1 - yc + dyl)) / dyl
            if c < yb:
                d = yb - yc + dyl          # yb - ya
                e = xb - xa
                o0 = (xa * d + e * (c - yc + dyl)) / d
                o1 = (xa * d + e * (c + 1 - yc + dyl)) / d
            else:
                d = yc - yb
                e = xc - xb
                o0 = (xb * d + e * (c - yb)) / d
                o1 = (xb * d + e * (c + 1 - yb)) / d
            if l0 < o0:
                if l1 < o1:
                    row.append((l0, o0, l1, o1))
                else:
                    row.append((l0, o0, o1, l1))
            elif l1 < o1:
                row.append((o0, l0, l1, o1))
            else:
                row.append((o0, l0, o1, l1))
            if yc > c + 1:
                keep.append(tri)
        active = keep
        if len(row) > 1:
            row.sort()
            prev = row[0]
            for cur in row[1:]:
                if not (prev[1] < cur[0] and prev[3] < cur[2]):
                    wa(f"第 {case} 组测试：有两个三角形相交")
                prev = cur
    return p


def main():
    inp = open(sys.argv[1], "rb").read().split()
    with open(sys.argv[2], "rb") as f:
        out = f.read().split()
    total = len(out)
    p = 0
    for case in range(1, int(inp[0]) + 1):
        p = check_test(case, int(inp[case]), out, p, total)
    if p != total:
        wa("输出里有多余的内容")
    sys.exit(0)


main()
