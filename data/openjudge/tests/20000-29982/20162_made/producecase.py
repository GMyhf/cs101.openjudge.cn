import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20162 statistics, Accepted solution 51463351.\n# Source: http://cs101.openjudge.cn/practice/solution/51463351/\n# Statistics: http://cs101.openjudge.cn/practice/20162/statistics/\n# License: not declared on submission page; no license inferred\nt = int(input())\nfor _ in range(t):\n    a, b, c, r = map(int, input().split())\n    a, b = min(a, b), max(a, b)\n    if b <= c-r or a >= c+r:\n        print(b-a)\n    else:\n        print(b-a-min(b, c+r)+max(a, c-r))\n'
SAMPLE='9\n1 10 7 1\n3 3 3 0\n8 2 10 4\n8 2 10 100\n-10 20 -17 2\n-3 2 2 0\n-3 1 2 0\n2 3 2 3\n-1 3 -2 2\n'
GENERATOR_NAME='g20162'

# 题面：1<=t<=1000；每组一行 a b c r，-10^8<a,b,c<10^8，0<r<10^8。
# 但题面样例里出现了 r=0（"3 3 3 0"、"-3 2 2 0"、"-3 1 2 0"），valid() 对 r 放宽到 0<=r，
# 生成的数据仍只取 r>=1。
LIM = 10 ** 8


def valid(text):
    import re
    if not text.endswith("\n") or text.endswith("\n\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    t = int(lines[0])
    if not 1 <= t <= 1000 or len(lines) != t + 1:
        return False
    for line in lines[1:]:
        toks = line.split(" ")
        if len(toks) != 4 or not all(re.fullmatch(r"-?(0|[1-9]\d*)", x) for x in toks):
            return False
        a, b, c, r = map(int, toks)
        if not all(-LIM < v < LIM for v in (a, b, c)) or not 0 <= r < LIM:
            return False
    return True


def _edge_rows(r, scale):
    """覆盖各种相对位置：区间在覆盖区左/右/内部/包住覆盖区/恰好端点相接/a==b/a>b。"""
    rows = []
    for _ in range(40):
        c = r.randint(-scale, scale)
        rad = r.randint(1, scale)
        kind = r.randrange(9)
        lo, hi = c - rad, c + rad
        if kind == 0:                       # 区间完全在左侧，右端点恰好碰到 c-r
            a, b = lo - r.randint(0, scale), lo
        elif kind == 1:                     # 完全在右侧，左端点恰好碰到 c+r
            a, b = hi, hi + r.randint(0, scale)
        elif kind == 2:                     # 完全在覆盖区内
            a, b = r.randint(lo, hi), r.randint(lo, hi)
        elif kind == 3:                     # 区间包住覆盖区
            a, b = lo - r.randint(0, scale), hi + r.randint(0, scale)
        elif kind == 4:                     # 跨左边界
            a, b = lo - r.randint(1, scale), r.randint(lo, hi)
        elif kind == 5:                     # 跨右边界
            a, b = r.randint(lo, hi), hi + r.randint(1, scale)
        elif kind == 6:                     # a==b
            a = b = r.choice((r.randint(lo - scale, hi + scale), lo, hi, c))
        elif kind == 7:                     # 端点恰为覆盖区端点
            a, b = lo, hi
        else:                               # 完全不相交、离得远
            a, b = hi + r.randint(1, scale), hi + r.randint(1, 2 * scale)
        if r.random() < .5:
            a, b = b, a
        vals = (a, b, c)
        if all(-LIM < v < LIM for v in vals) and 0 < rad < LIM:
            rows.append(f"{a} {b} {c} {rad}")
    return rows


def _rand_row(r, span):
    return f"{r.randint(-span, span)} {r.randint(-span, span)} {r.randint(-span, span)} {r.randint(1, span)}"


def g20162(r, seed):
    big = LIM - 1
    if seed == 1:      # t=1 最小
        return "1\n" + _rand_row(r, 20) + "\n"
    if seed == 2:      # 取值触到上下界：|b-a| 接近 2*10^8，c±r 接近 ±2*10^8
        rows = [f"{-big} {big} 0 1", f"{big} {-big} {big} {big}", f"{-big} {big} {-big} {big}",
                f"{-big} {-big} {big} {big}", f"{big} {big} {-big} {big}", f"{-big} {big} {big} 1",
                f"0 0 0 {big}", f"{-big} {big} 0 {big}", f"{big} {-big} 1 {big}", f"{-big} {big} {-big} 1"]
        return f"{len(rows)}\n" + "\n".join(rows) + "\n"
    if seed <= 10:     # 小值域、各种相对位置
        rows = _edge_rows(r, r.choice((3, 5, 10, 100)))[: r.randint(10, 40)]
    elif seed <= 20:   # 原来的随机形状（±1000），组数加大
        rows = [_rand_row(r, 1000) for _ in range(r.randint(5, 300))]
    elif seed <= 30:   # 大值域
        rows = _edge_rows(r, r.choice((10 ** 6, 5 * 10 ** 7, big)))
        rows += [_rand_row(r, big) for _ in range(r.randint(50, 200))]
        r.shuffle(rows)
    else:              # 满规模 t=1000
        rows = []
        while len(rows) < 1000:
            rows += _edge_rows(r, r.choice((10, 1000, 10 ** 6, big)))
            rows.append(_rand_row(r, big))
        rows = rows[:1000]
    return f"{len(rows)}\n" + "\n".join(rows) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g20162(random.Random(seed), seed) for seed in range(1, 40)]
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
