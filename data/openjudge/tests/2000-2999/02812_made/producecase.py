import random,subprocess,sys,tempfile
from pathlib import Path
def fence_counts(n):
    if n == 1:
        return 1
    count = [[[0, 0] for _ in range(n + 1)] for _ in range(n + 1)]
    count[1][1] = [1, 1]
    for size in range(2, n + 1):
        for first in range(1, size + 1):
            count[size][first][0] = sum(count[size - 1][second][1]
                                            for second in range(first, size))
            count[size][first][1] = sum(count[size - 1][second][0]
                                            for second in range(1, first))
    return sum(sum(count[n][first]) for first in range(1, n + 1))
def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    if number == 1258:
        cases = []
        for _ in range(r.randint(1, 3)):
            n = r.randint(3, 18)
            matrix = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    matrix[i][j] = matrix[j][i] = r.randint(1, 100000)
            cases.append(str(n) + "\n" + "\n".join(" ".join(map(str, row)) for row in matrix))
        return "\n".join(cases) + "\n"
    if number == 1661:
        cases = []
        for _ in range(r.randint(1, 4)):
            n = r.randint(1, 12); y = r.randint(2, 200); max_drop = y
            platforms = []
            for height in r.sample(range(1, y), min(n, y - 1)):
                left = r.randint(20, 1000); platforms.append((left, left + r.randint(1, 30), height))
            while len(platforms) < n:
                left = 1100 + len(platforms) * 40; platforms.append((left, left + 10, 1))
            cases.append(f"{n} 0 {y} {max_drop}\n" + "\n".join("%d %d %d" % p for p in platforms))
        return str(len(cases)) + "\n" + "\n".join(cases) + "\n"
    if number == 1664:
        values = [(r.randint(1, 10), r.randint(1, 10)) for _ in range(r.randint(1, 20))]
        return str(len(values)) + "\n" + "\n".join(f"{m} {n}" for m, n in values) + "\n"
    if number == 1703:
        cases = []
        for _ in range(r.randint(1, 4)):
            n = r.randint(3, 80); gangs = [0, 1] + [r.randrange(2) for _ in range(n - 2)]; ops = []
            for _ in range(r.randint(3, 100)):
                a, b = r.sample(range(n), 2)
                if r.random() < .55:
                    while gangs[a] == gangs[b]: b = r.randrange(n)
                    ops.append(f"D {a+1} {b+1}")
                else: ops.append(f"A {a+1} {b+1}")
            cases.append(f"{n} {len(ops)}\n" + "\n".join(ops))
        return str(len(cases)) + "\n" + "\n".join(cases) + "\n"
    if number == 1958:
        return ""
    if number == 2812:
        rows, cols = r.randint(5, 40), r.randint(5, 40); planted_row = r.randint(1, rows)
        points = {(planted_row, col) for col in range(1, cols + 1)}
        target = r.randint(max(3, cols), min(rows * cols, cols + 80))
        while len(points) < target: points.add((r.randint(1, rows), r.randint(1, cols)))
        points = list(points); r.shuffle(points)
        return f"{rows} {cols}\n{len(points)}\n" + "\n".join(f"{x} {y}" for x, y in points) + "\n"
    if number == 1042:
        cases = []
        for _ in range(r.randint(1, 3)):
            n = r.randint(2, 8); h = r.randint(1, 5)
            fish = [r.randint(0, 100) for _ in range(n)]; decreases = [r.randint(0, 20) for _ in range(n)]
            travel = [r.randint(1, min(12, h * 12)) for _ in range(n - 1)]
            cases.append("\n".join((str(n), str(h), " ".join(map(str, fish)),
                                     " ".join(map(str, decreases)), " ".join(map(str, travel)))))
        return "\n".join(cases) + "\n0\n"
    if number == 2226:
        rows, cols = r.randint(1, 18), r.randint(1, 18)
        grid = ["".join(r.choice("***...") for _ in range(cols)) for _ in range(rows)]
        return f"{rows} {cols}\n" + "\n".join(grid) + "\n"
    if number == 1064:
        n, k = r.randint(1, 80), r.randint(1, 500)
        lengths = [r.randint(100, 10_000_000) for _ in range(n)]
        return f"{n} {k}\n" + "\n".join(f"{x//100}.{x%100:02d}" for x in lengths) + "\n"
    if number == 1185:
        rows, cols = r.randint(1, 25), r.randint(1, 10)
        return f"{rows} {cols}\n" + "\n".join("".join(r.choice("PPPH") for _ in range(cols)) for _ in range(rows)) + "\n"
    if number == 2229:
        return f"{r.randint(1, 1_000_000)}\n"
    if number == 2533:
        values = [r.randint(0, 10000) for _ in range(r.randint(1, 200))]
        return f"{len(values)}\n" + " ".join(map(str, values)) + "\n"
    if number == 2659:
        rows, cols, count = r.randint(1, 30), r.randint(1, 30), r.randint(1, 30)
        bombs = [(r.randint(1, rows), r.randint(1, cols), r.randrange(1, 100, 2), r.randint(0, 1))
                 for _ in range(count)]
        return f"{rows} {cols} {count}\n" + "\n".join("%d %d %d %d" % b for b in bombs) + "\n"
    if number == 2946:
        value, count = r.randint(-100, 100), r.randint(1, 30); operations = []
        for _ in range(count): operations.append((r.choice(("plus", "minus", "multiply")), r.randint(-5, 5)))
        return f"{value} {count}\n" + "\n".join(f"{op} {x}" for op, x in operations) + "\n"
    if number == 1037:
        values = []
        for _ in range(r.randint(1, 8)):
            n = r.randint(1, 10); values.append((n, r.randint(1, fence_counts(n))))
        return str(len(values)) + "\n" + "\n".join(f"{n} {c}" for n, c in values) + "\n"
    if number == 1160:
        villages = sorted(r.sample(range(1, 10001), r.randint(1, 100)))
        return f"{len(villages)} {r.randint(1, min(30, len(villages)))}\n" + " ".join(map(str, villages)) + "\n"
    if number == 1944:
        n = r.randint(2, 80); all_pairs = [(a, b) for a in range(1, n + 1) for b in range(a + 1, n + 1)]
        pairs = r.sample(all_pairs, r.randint(1, min(200, len(all_pairs))))
        return f"{n} {len(pairs)}\n" + "\n".join(f"{a} {b}" for a, b in pairs) + "\n"
    if number == 2385:
        total, walks = r.randint(1, 200), r.randint(1, 30)
        return f"{total} {walks}\n" + "\n".join(str(r.randint(1, 2)) for _ in range(total)) + "\n"
    if number == 2711:
        heights = [r.randint(130, 230) for _ in range(r.randint(2, 100))]
        return f"{len(heights)}\n" + " ".join(map(str, heights)) + "\n"
    if number == 2797:
        words = set(); target = r.randint(2, 60)
        while len(words) < target:
            words.add("".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1, 20))))
        words = sorted(words); r.shuffle(words)
        return "\n".join(words) + "\n"
    raise KeyError(number)

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2812: 恼人的青蛙\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/02812/\n# License: not declared in source collection; no license is inferred.\nimport sys\nimport array\ndef is_valid(x, y):\n    return 0 < x <= R and 0 < y <= C\nR, C = map(int, input().split())\nN = int(input())\n#紧凑数组，省内存\nflag = [array.array("B", [0] * (C + 1)) for _ in range(R + 1)]\npoints = [tuple(map(int, input().split())) for _ in range(N)]\nfor x, y in points:\n    flag[x][y] = 1\n#排序，先按行升序，再按列升序\npoints.sort()\nmax_count = 2\nfor i in range(N):\n    x1, y1 = points[i]\n    for j in range(i + 1, N):\n        x2, y2 = points[j]\n        dx, dy = x2 - x1, y2 - y1\n        # x1,y1只是途径点而非起始点，跳过本次循环\n        if is_valid(x1-dx, y1-dy):\n            continue\n        # 行越界，跳出整个循环\n        if not (0 < x1 + dx * (max_count - 1) <= R):\n            break\n        # 列越界，跳出本次循环\n        if not (0< y1 + dy * (max_count - 1) <= C):\n            continue\n        cnt = 2\n        while is_valid(x2 + dx, y2 + dy):\n            x2 += dx\n            y2 += dy\n            if not flag[x2][y2]:\n                break\n            cnt += 1\n        else:\n            max_count = max(max_count, cnt)\nprint(max_count if max_count > 2 else 0)\n'
NUMBER=2812
SAMPLE='6 7\n14\n2 1\n6 6\n4 2\n2 5\n2 6\n2 7\n3 4\n6 1\n6 2\n2 3\n6 3\n6 4\n6 5\n6 7\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout.rstrip()+'\n'
import re as _re
_POS = _re.compile(r'[1-9][0-9]*\Z')
def valid(text):
    """题面契约：第 1 行 R C（1<=R,C<=5000）；第 2 行 N（3<=N<=5000）；
    其后恰 N 行 "x y"，1<=x<=R、1<=y<=C，且每棵被踩踏水稻只列出一次（坐标互异）。"""
    if not text.endswith('\n') or '\r' in text: return False
    lines = text[:-1].split('\n')
    if len(lines) < 2: return False
    a = lines[0].split(' ')
    if len(a) != 2 or not all(_POS.match(t) for t in a): return False
    R, C = map(int, a)
    if not (1 <= R <= 5000 and 1 <= C <= 5000): return False
    if not _POS.match(lines[1]): return False
    N = int(lines[1])
    if not (3 <= N <= 5000) or len(lines) != N + 2: return False
    seen = set()
    for ln in lines[2:]:
        b = ln.split(' ')
        if len(b) != 2 or not all(_POS.match(t) for t in b): return False
        x, y = map(int, b)
        if not (1 <= x <= R and 1 <= y <= C) or (x, y) in seen: return False
        seen.add((x, y))
    return True

def _fmt(R, C, pts, r):
    pts = list(pts); r.shuffle(pts)
    return f"{R} {C}\n{len(pts)}\n" + "\n".join(f"{x} {y}" for x, y in pts) + "\n"

def _line(R, C, x, y, dx, dy):
    """从 (x,y) 起按步长 (dx,dy) 走到出界为止的全部格点。"""
    out = []
    while 1 <= x <= R and 1 <= y <= C:
        out.append((x, y)); x += dx; y += dy
    return out

def _entry(R, C, r, dx, dy):
    """随机取一条从田外跳入、贯穿到田外的完整青蛙路径（长度>=3 时返回）。"""
    for _ in range(1000):
        x, y = r.randint(1, R), r.randint(1, C)
        while 1 <= x - dx <= R and 1 <= y - dy <= C: x -= dx; y -= dy
        path = _line(R, C, x, y, dx, dy)
        if len(path) >= 3: return path
    return []

def _noise(R, C, pts, target, r):
    while len(pts) < target: pts.add((r.randint(1, R), r.randint(1, C)))
    return pts

def cases():
    r = random.Random(2812_2026)
    out = []
    # 最小规模与边界：单行/单列刚好 3 棵、贯穿成路径
    out.append(_fmt(1, 3, {(1, 1), (1, 2), (1, 3)}, r))
    out.append(_fmt(3, 1, {(1, 1), (2, 1), (3, 1)}, r))
    # 3 棵等距共线但起点前一跳仍在田内 -> 不是路径，答案 0
    out.append(_fmt(5, 5, {(2, 2), (3, 3), (4, 4)}, r))
    # 共线但间距不等 -> 0
    out.append(_fmt(1, 6, {(1, 1), (1, 2), (1, 4), (1, 6)}, r))
    # 等距共线贯穿，但终点后一跳落在田内未踩踏的水稻上 -> 不算；另有短路径
    out.append(_fmt(7, 7, {(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (1, 7), (2, 7), (3, 7)}, r))
    # 只有 2 棵的贯穿直线不算（N=3）
    out.append(_fmt(2, 2, {(1, 1), (2, 2), (1, 2)}, r))
    # 小规模随机，供暴力核对
    for _ in range(18):
        R, C = r.randint(1, 12), r.randint(1, 12)
        if R * C < 3: R, C = 3, 4
        cells = [(i, j) for i in range(1, R + 1) for j in range(1, C + 1)]
        k = r.randint(3, len(cells))
        pts = set(r.sample(cells, k))
        if r.random() < .6:
            pts |= set(_entry(R, C, r, r.randint(-3, 3) or 1, r.randint(-3, 3)))
        out.append(_fmt(R, C, pts, r))
    # 中规模：多条方向各异的路径 + 噪声
    for _ in range(8):
        R, C = r.randint(50, 600), r.randint(50, 600)
        pts = set()
        for _ in range(r.randint(1, 4)):
            dx, dy = r.randint(0, 9), r.randint(-9, 9)
            if dx == 0 and dy <= 0: dy = r.randint(1, 9)
            pts |= set(_entry(R, C, r, dx, dy))
        out.append(_fmt(R, C, _noise(R, C, pts, min(R * C, len(pts) + r.randint(50, 1500)), r), r))
    # 满规模：5000x5000，N=5000，斜向长路径 + 一条间隔一跳的“断路”
    R = C = 5000
    p1 = set(_line(R, C, 1, 1, 4, 3))           # 1250 棵的贯穿路径
    p2 = set(_line(R, C, 1, 5000, 3, -3)); p2.discard((301, 4700))  # 断开的长线
    out.append(_fmt(R, C, _noise(R, C, p1 | p2, 5000, r), r))
    # 单列 / 单行（参考解在这类退化形状上接近 O(N^2)，规模取 Python 时限一半以内能跑完的）
    out.append(_fmt(3000, 1, {(i, 1) for i in range(1, 3001)}, r))
    out.append(_fmt(1, 2200, {(1, j) for j in range(1, 2201) if j != 1100}, r))  # 步长 1 断开，步长 2 奇数列贯穿 -> 1100
    # 稠密满格 70x70=4900
    out.append(_fmt(70, 70, {(i, j) for i in range(1, 71) for j in range(1, 71)}, r))
    # 稀疏随机、无长路径：在 Python 时限内能跑的最大规模
    out.append(_fmt(5000, 5000, _noise(5000, 5000, set(), 2200, r), r))
    out.append(_fmt(100, 5000, _noise(100, 5000, set(_line(100, 5000, 1, 7, 1, 50)), 4000, r), r))
    # 竖直长路径 + 噪声
    out.append(_fmt(5000, 300, _noise(5000, 300, set(_line(5000, 300, 2, 150, 2, 0)), 5000, r), r))
    return out

def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+cases()):
  assert valid(x),i
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
