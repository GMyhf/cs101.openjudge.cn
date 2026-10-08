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

# ---- 题面契约与 1661 专用生成器 ----
def _solve_case(x0, y0, mx, plats, bottleneck=False):
    """独立 O(N^2) DP：返回最短时间（或 bottleneck=True 时返回整条路径上最大单次下落的最小值）；无解返回 None。"""
    INF = float('inf')
    order = sorted(range(len(plats)), key=lambda i: plats[i][2])
    ps = [plats[i] for i in order]  # 按高度升序
    n = len(ps)
    # 升序排列后从高往低找第一个高度严格更低且覆盖 x 的平台；同高平台互不相连，所以最高者唯一
    def land(x, h, upto):
        for j in range(upto - 1, -1, -1):
            a, b, hh = ps[j]
            if hh < h and a <= x <= b:
                return j
        return -1
    L = [INF] * n; R = [INF] * n
    def val(x, h, upto):
        j = land(x, h, upto)
        drop = h - (ps[j][2] if j >= 0 else 0)
        if bottleneck:
            if j < 0: return drop
            return max(drop, min(L[j], R[j]))
        if drop > mx: return INF
        if j < 0: return drop
        a, b, hh = ps[j]
        return drop + min(x - a + L[j], b - x + R[j])
    for i in range(n):
        a, b, h = ps[i]
        # 同高平台在 order 中位于 i 前后均可，land 只认严格更低者，故传 i（更低者都在 i 之前）
        L[i] = val(a, h, i); R[i] = val(b, h, i)
    res = val(x0, y0, n)
    return None if res == INF else res

def _parse(text):
    tok = text.split(); pos = 0
    t = int(tok[0]); pos = 1; cases = []
    for _ in range(t):
        n, x, y, m = map(int, tok[pos:pos + 4]); pos += 4
        pl = [tuple(map(int, tok[pos + 3 * k:pos + 3 * k + 3])) for k in range(n)]; pos += 3 * n
        cases.append((n, x, y, m, pl))
    return cases

def valid(text):
    try:
        if not text.endswith('\n') or '\r' in text: return False
        lines = text[:-1].split('\n')
        for ln in lines:
            if ln != ln.strip() or '  ' in ln: return False
        rows = [ln.split() for ln in lines]
        if len(rows[0]) != 1: return False
        t = int(rows[0][0])
        if not 0 <= t <= 20: return False
        p = 1
        for _ in range(t):
            if p >= len(rows) or len(rows[p]) != 4: return False
            n, x, y, m = map(int, rows[p]); p += 1
            if not (1 <= n <= 1000 and -20000 <= x <= 20000 and y <= 20000): return False
            pl = []
            for _ in range(n):
                if p >= len(rows) or len(rows[p]) != 3: return False
                a, b, h = map(int, rows[p]); p += 1
                if not (-20000 <= a <= b <= 20000 and 0 < h < y): return False
                pl.append((a, b, h))
            # 所有平台均不重叠或相连：同一高度的平台区间两两不相交、不相接
            byh = {}
            for a, b, h in pl: byh.setdefault(h, []).append((a, b))
            for segs in byh.values():
                segs.sort()
                for (a1, b1), (a2, b2) in zip(segs, segs[1:]):
                    if a2 <= b1: return False
            # 测试数据保证问题一定有解
            if _solve_case(x, y, m, pl) is None: return False
        return p == len(rows)
    except Exception:
        return False

def _place(r, n, y, xlo, xhi, wlo, whi, same_height_p=0.0):
    """在高度 (0,y) 内放 n 个平台，同高平台互不相连。"""
    byh = {}; out = []; tries = 0
    while len(out) < n:
        tries += 1
        if out and r.random() < same_height_p:
            h = r.choice(out)[2]
        else:
            h = r.randint(1, y - 1)
        w = r.randint(wlo, whi)
        a = r.randint(xlo, max(xlo, xhi - w)); b = min(a + w, 20000)
        if any(not (b < c or d < a) for c, d in byh.get(h, [])) or any(not (b + 1 < c or d + 1 < a) for c, d in byh.get(h, [])):
            continue
        byh.setdefault(h, []).append((a, b)); out.append((a, b, h))
    return out

def gen_case(r, kind, n=None):
    if kind == 'tiny':
        y = r.randint(2, 6); n = 1
        a = r.randint(-3, 3); b = a + r.randint(0, 3)
        pl = [(a, b, r.randint(1, y - 1))]
        x = r.randint(-5, 5)
    elif kind == 'chain':
        # 一条长链：每层平台都接住上一层的边缘，深度 n
        n = n or 1000; y = 20000
        x = r.randint(-100, 100); pl = []; cx = x
        for h in sorted(r.sample(range(1, y), n), reverse=True):
            w = r.randint(0, 30)
            a = cx - r.randint(0, w); b = a + w
            pl.append((a, b, h)); cx = a if r.random() < .5 else b
        n = len(pl)
    elif kind == 'narrow':
        # 窄平台、大跨度：很多平台挤在同一条竖线附近，需反复判断落点
        n = n or 1000; y = r.randint(n + 2, 20000)
        pl = _place(r, n, y, -300, 300, 0, 40, .3); x = r.randint(-50, 50)
    elif kind == 'wide':
        n = n or r.randint(50, 1000); y = r.randint(2, 20000)
        pl = _place(r, n, y, -20000, 20000, 0, 8000, .4); x = r.randint(-20000, 20000)
    else:  # random 中等
        n = n or r.randint(2, 60); y = r.randint(2, 300)
        span = r.randint(5, 200)
        pl = _place(r, n, y, -span, span, 0, r.randint(1, 60), .3); x = r.randint(-span, span)
    pl = [(a, b, h) for a, b, h in pl]; r.shuffle(pl)
    bott = _solve_case(x, y, 10 ** 9, pl, bottleneck=True)
    mode = r.random()
    if mode < .45: m = bott                      # 恰好够：卡掉对 MAX 判断用 < / <= 写反的
    elif mode < .75: m = bott + r.randint(0, max(1, y // 10))
    else: m = r.randint(bott, max(bott, y))
    return f"{len(pl)} {x} {y} {m}\n" + "\n".join("%d %d %d" % q for q in pl)

def gen_file(seed):
    r = random.Random(1661 * 1_000_003 + seed)
    if seed <= 6:      # 小规模、多组
        kinds = ['tiny'] * 3 + ['rand'] * 10
        cs = [gen_case(r, r.choice(kinds)) for _ in range(r.randint(1, 20))]
    elif seed <= 24:
        cs = [gen_case(r, r.choice(['rand', 'rand', 'wide', 'narrow']), r.randint(1, 120)) for _ in range(r.randint(1, 20))]
    elif seed <= 30:
        cs = [gen_case(r, 'chain', r.randint(200, 1000)) for _ in range(r.randint(1, 4))]
    elif seed <= 35:
        cs = [gen_case(r, 'narrow', 1000) for _ in range(r.randint(1, 3))]
    else:
        cs = [gen_case(r, r.choice(['wide', 'narrow', 'chain']), 1000) for _ in range(20)]
    return f"{len(cs)}\n" + "\n".join(cs) + "\n"

REFERENCE="# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1661: Help Jimmy\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01661/\n# License: not declared in source collection; no license is inferred.\nimport sys\nimport sys\nfrom functools import lru_cache\n\n# 优化1：增加递归深度限制，防止 N=1000 时爆栈\nsys.setrecursionlimit(2000)\n\ndef solve():\n    # 优化2：使用 sys.stdin.read 快速读取所有输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    iterator = iter(input_data)\n\n    try:\n        num_test_cases = int(next(iterator))\n    except StopIteration:\n        return\n\n    for _ in range(num_test_cases):\n        try:\n            N = int(next(iterator))\n            ini_x = int(next(iterator))\n            ini_y = int(next(iterator))\n            MaxVal = int(next(iterator))\n\n            p = []\n            for _ in range(N):\n                p.append((int(next(iterator)), int(next(iterator)), int(next(iterator))))\n\n            # 按高度从大到小排序\n            p.sort(key=lambda x: -x[2])\n\n            @lru_cache(None)\n            def dfs(x, y, parent_idx):\n                # parent_idx: 刚离开的平台索引（如果是起点则为 -1）\n                # 需要在 p[parent_idx+1 ... N] 中寻找接住我们的平台\n\n                for i in range(parent_idx + 1, N):\n                    px1, px2, ph = p[i]\n\n                    # 剪枝：因为 p 是按高度从大到小排的\n                    # 如果当前平台的高度差已经超过 MaxVal，那后面更低的平台肯定也接不住，直接死掉\n                    if y - ph > MaxVal:\n                        return float('inf')\n\n                    # 判断横坐标是否在平台范围内\n                    if px1 <= x <= px2:\n                        # 找到了接住的平台 i\n                        # 递归计算：(当前位置到平台左/右端的水平距离) + dfs(下一层)\n                        # 注意：题目求时间，垂直时间恒为 total_Y，这里 dfs 只负责计算最小水平距离\n\n                        dist_left = x - px1 + dfs(px1, ph, i)\n                        dist_right = px2 - x + dfs(px2, ph, i)\n                        return min(dist_left, dist_right)\n\n                # 如果循环结束都没 break，说明落到了地面 (y=0)\n                if y <= MaxVal:\n                    return 0\n                else:\n                    return float('inf')\n\n            # 初始调用：从 (ini_x, ini_y) 开始，父节点索引传 -1，\n            # 这样循环会从 0 (第一个平台) 开始搜索\n            min_horizontal_dist = dfs(ini_x, ini_y, -1)\n\n            if min_horizontal_dist == float('inf'):\n                # 理论上题目保证有解，不会进这里\n                pass\n            else:\n                # 总时间 = 垂直下落距离(ini_y) + 最小水平移动距离\n                print(ini_y + min_horizontal_dist)\n\n        except StopIteration:\n            break\n\nif __name__ == '__main__':\n    solve()\n"
NUMBER=1661
SAMPLE='1\n3 8 17 20\n0 10 8\n0 10 13\n4 14 3\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout.rstrip()+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[gen_file(s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
