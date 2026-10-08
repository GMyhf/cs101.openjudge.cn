# 28750 倾斜方块 数据生成器（ICPC WF 2023 Tilting Tiles）。
# 题面约束：1<=h,w<=500；每行长度为 w，字符为 '.' 或小写字母 a-z；两个排列之间有一行空行。
# 第 0、1 组为题面样例 1、2；答案由同目录 samplecode.py 计算。
import random
import string
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = '4 4\n.r..\nrgyb\n.b..\n.yr.\n\nyrbr\n..yr\n...g\n...b\n'
SAMPLE2 = '1 7\n....x..\n\n..x....\n'
LOWER = string.ascii_lowercase
CELL = set('.' + LOWER)


def valid(text):
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    try:
        p = lines[0].split(' ')
        if len(p) != 2 or not all(x.isdigit() and x == str(int(x)) for x in p):
            return False
        h, w = map(int, p)
        if not (1 <= h <= 500 and 1 <= w <= 500) or len(lines) != 2 * h + 2:
            return False
        if lines[h + 1] != '':
            return False
        rows = lines[1:h + 1] + lines[h + 2:]
        return all(len(s) == w and set(s) <= CELL for s in rows)
    except ValueError:
        return False


# ---- 倾斜（作用于二维列表，元素为 0 表示空）；0 左 1 上 2 右 3 下 ----
def tilt(g, d):
    h, w = len(g), len(g[0])
    if d in (0, 2):
        res = []
        for row in g:
            t = [x for x in row if x]
            z = [0] * (w - len(t))
            res.append(t + z if d == 0 else z + t)
        return res
    res = [[0] * w for _ in range(h)]
    for j in range(w):
        t = [g[i][j] for i in range(h) if g[i][j]]
        off = 0 if d == 1 else h - len(t)
        for k, x in enumerate(t):
            res[off + k][j] = x
    return res


def to_grid(rows):
    return [[0 if c == '.' else c for c in s] for s in rows]


def to_rows(g):
    return [''.join(c if c else '.' for c in row) for row in g]


def fmt(a, b):
    return f"{len(a)} {len(a[0])}\n" + "\n".join(a) + "\n\n" + "\n".join(b) + "\n"


def rand_board(r, h, w, p, colors):
    return [[r.choice(colors) if r.random() < p else 0 for _ in range(w)] for _ in range(h)]


def cycle_target(r, g, q, mode):
    """g 先倾斜两次进入角落形态，再按 q（1 顺时针 / 3 逆时针）循环倾斜。
    求 4 次倾斜的置换，按环旋转 k 步造目标。
    mode='yes'：所有环同一个 k（必可达）；mode='crt'：挑两条长度不互素的环，旋转步数模 gcd 不同。"""
    h, w = len(g), len(g[0])
    d0 = r.randrange(4)
    d1 = (d0 + q) % 4
    s = tilt(tilt(g, d0), d1)
    d = (d1 + q) % 4
    lab = [[(i * w + j + 1) if s[i][j] else 0 for j in range(w)] for i in range(h)]
    t = lab
    dd = d
    for _ in range(4):
        t = tilt(t, dd)
        dd = (dd + q) % 4
    # t[i][j] = 原位置标号：位置 src 经过一轮后到达 (i,j)
    nxt = {}
    for i in range(h):
        for j in range(w):
            if t[i][j]:
                nxt[t[i][j] - 1] = i * w + j
    seen, cycles = set(), []
    for v in nxt:
        if v not in seen:
            c = []
            while v not in seen:
                seen.add(v)
                c.append(v)
                v = nxt[v]
            cycles.append(c)
    k = r.randint(0, 10 ** 9)
    shift = {id(c): k for c in cycles}
    if mode == 'crt':
        from math import gcd
        long_c = [c for c in cycles if len(c) > 1]
        pairs = [(a, b) for ai, a in enumerate(long_c[:60]) for b in long_c[ai + 1:60] if gcd(len(a), len(b)) > 1]
        if pairs:
            a, b = r.choice(pairs)
            shift[id(b)] = k + r.randint(1, gcd(len(a), len(b)) - 1)
    res = [[0] * w for _ in range(h)]
    for c in cycles:
        L = len(c)
        for idx, v in enumerate(c):
            u = c[(idx + shift[id(c)]) % L]
            res[u // w][u % w] = s[v // w][v % w]
    for _ in range(r.randint(0, 3)):
        res = tilt(res, d)
        d = (d + q) % 4
    return res


def swap_two(r, g):
    cells = [(i, j) for i, row in enumerate(g) for j, x in enumerate(row) if x]
    g = [row[:] for row in g]
    if len(cells) >= 2:
        for _ in range(20):
            (a, b), (c, e) = r.sample(cells, 2)
            if g[a][b] != g[c][e]:
                g[a][b], g[c][e] = g[c][e], g[a][b]
                break
    return g


def random_walk(r, g, steps):
    for _ in range(steps):
        g = tilt(g, r.randrange(4))
    return g


def gen(r, h, w, kind):
    colors = list(LOWER[:r.choice([1, 2, 3, 26])])
    g = rand_board(r, h, w, r.choice([0.05, 0.3, 0.6, 0.9]), colors)
    if kind == 0:
        b = random_walk(r, g, r.randint(0, 30))
    elif kind == 1:
        b = swap_two(r, random_walk(r, g, r.randint(2, 30)))
    elif kind == 2:
        b = cycle_target(r, g, r.choice([1, 3]), 'yes')
    elif kind == 3:
        b = cycle_target(r, g, r.choice([1, 3]), 'crt')
    else:
        b = rand_board(r, h, w, 0.3, colors)
    return fmt(to_rows(g), to_rows(b))


def cases():
    r = random.Random(28750)
    out = [SAMPLE, SAMPLE2]
    N = 500
    # 满规模
    g = rand_board(r, N, N, 0.6, list(LOWER))
    out.append(fmt(to_rows(g), to_rows(cycle_target(r, g, 1, 'yes'))))
    g = rand_board(r, N, N, 0.5, list(LOWER))
    out.append(fmt(to_rows(g), to_rows(cycle_target(r, g, 3, 'crt'))))
    g = rand_board(r, N, N, 0.95, list('ab'))
    out.append(fmt(to_rows(g), to_rows(swap_two(r, random_walk(r, g, 7)))))
    g = rand_board(r, N, N, 0.3, list(LOWER))
    out.append(fmt(to_rows(g), to_rows(cycle_target(r, g, 3, 'yes'))))
    out.append(fmt(['.' * N] * N, ['.' * N] * N))                               # 全空
    # 边界形状
    out.append(fmt(['a'], ['a']))
    out.append(fmt(['.'], ['z']))
    out.append(fmt(['ca.'], ['.ac']))                                            # 原参考解误判的反例
    row = ''.join(r.choice('ab.') for _ in range(N))
    out.append(fmt([row], [''.join(sorted(row, key=lambda c: c != '.'))]))     # 1x500 右靠
    col = [r.choice('xy.') for _ in range(N)]
    out.append(fmt(col, [c for c in col if c != '.'] + ['.'] * col.count('.')))   # 500x1 上靠
    out.append(fmt(['ab', 'ba'], ['ba', 'ab']))                                  # 满格不能动
    out.append(fmt(['ab', '..'], ['..', 'ba']))
    # 中等规模
    for k in range(8):
        h, w = r.randint(30, 120), r.randint(30, 120)
        out.append(gen(r, h, w, [2, 3, 1, 0, 2, 3, 3, 1][k]))
    # 小规模（可暴力搜索核对）
    for k in range(19):
        h, w = r.randint(1, 7), r.randint(1, 7)
        out.append(gen(r, h, w, k % 5))
    return out


def run(text):
    x = subprocess.run([sys.executable, str(HERE / 'samplecode.py')], input=text,
                       text=True, capture_output=True, timeout=120)
    if x.returncode:
        raise SystemExit(x.stderr)
    return x.stdout


def main():
    d = HERE / 'data'
    d.mkdir(exist_ok=True)
    cs = cases()
    assert len(cs) == 41 and len(set(cs)) == len(cs), len(cs)
    for i, c in enumerate(cs):
        assert valid(c), i
        (d / f'{i}.in').write_text(c)
        (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__':
    main()
