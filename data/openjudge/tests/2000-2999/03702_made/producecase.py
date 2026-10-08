import random, re, subprocess
from pathlib import Path
ROOT = Path(__file__).parent
SAMPLE = '4\n0 0 0 1 0 0 1 1 0 1 1 1\n'


def valid(text):
    """题面契约：两行；第一行 n（不超过 10 个点），第二行 3n 个 0..100 的整数坐标，点互不相同。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2 or not re.fullmatch(r"\d+", lines[0]):
        return False
    n = int(lines[0])
    toks = lines[1].split()
    if not 1 <= n <= 10 or len(toks) != 3 * n:
        return False
    if not all(re.fullmatch(r"\d+", t) and int(t) <= 100 for t in toks):
        return False
    pts = {tuple(toks[3 * i:3 * i + 3]) for i in range(n)}
    return len(pts) == n


def fmt(pts):
    return str(len(pts)) + '\n' + ' '.join(map(str, sum((list(p) for p in pts), []))) + '\n'


def distinct_points(rng, n, hi):
    pts = []; used = set()
    while len(pts) < n:
        p = tuple(rng.randrange(hi + 1) for _ in range(3))
        if p not in used: used.add(p); pts.append(p)
    return pts


# 题面提示里的几组：同距离按输入先后、点对内按输入先后
HINT_CASES = [
    fmt([(0, 0, 0), (1, 1, 1)]),
    fmt([(1, 1, 1), (0, 0, 0)]),
    fmt([(0, 0, 0), (0, 0, 1), (0, 0, 2)]),
    fmt([(0, 0, 2), (0, 0, 1), (0, 0, 0)]),
]


def case(i):
    if i == 0: return SAMPLE
    if i < 40:
        rng = random.Random(370200 + i); n = 2 + i % 9
        return fmt(distinct_points(rng, n, 100))
    if i < 44: return HINT_CASES[i - 40]
    rng = random.Random(370200 + i)
    if i == 44:  # 立方体 8 个顶点 + 2 点，取值上下界 0/100，大量等距
        pts = [(x, y, z) for x in (0, 100) for y in (0, 100) for z in (0, 100)] + [(50, 50, 50), (0, 0, 50)]
        rng.shuffle(pts); return fmt(pts)
    if i == 45:  # 等距但分量不同：(3,4,0) 与 (0,0,5) 一类，浮点不同算法也必须判成相等
        pts = [(0, 0, 0), (3, 4, 0), (0, 0, 5), (4, 0, 3), (0, 5, 0), (5, 0, 0), (0, 3, 4), (1, 2, 2), (2, 1, 2), (2, 2, 1)]
        return fmt(pts)
    if i == 46:  # 两个坐标相同只差一维的点：距离为整数
        return fmt([(100, 100, z) for z in (100, 0, 37, 63, 1, 99, 50, 2, 98, 3)])
    # 小网格上取满 10 个点：同距离点对极多，排序必须稳定
    return fmt(distinct_points(rng, 10, 2 if i < 50 else 3))


def oracle(inp):
    v = list(map(int, inp.split())); n = v[0]; p = [tuple(v[1+3*i:4+3*i]) for i in range(n)]
    pairs = [(-sum((a - b) ** 2 for a, b in zip(p[i], p[j])), i, j) for i in range(n) for j in range(i + 1, n)]
    pairs.sort()  # 整数平方距离降序，再按 (i, j) 字典序 = 冒泡稳定顺序
    return ''.join(f'({p[i][0]},{p[i][1]},{p[i][2]})-({p[j][0]},{p[j][1]},{p[j][2]})={(-d) ** 0.5:.2f}\n' for d, i, j in pairs)


def main():
    for i in range(52):
        inp=case(i); assert valid(inp), i
        out=subprocess.run(['python3',str(ROOT/'samplecode.py')],input=inp,text=True,capture_output=True,check=True).stdout
        assert out == oracle(inp), i
        (ROOT/'data'/f'{i}.in').write_text(inp); (ROOT/'data'/f'{i}.out').write_text(out)


if __name__ == "__main__":
    main()
