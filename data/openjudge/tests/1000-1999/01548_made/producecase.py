import random, subprocess, sys, tempfile
from pathlib import Path

def valid(text):
    # 题面：若干张图，每张一行或多行垃圾坐标 "r c"（单个空格分隔），以 "0 0" 结束一张图；
    # 全部以 "-1 -1" 结束；坐标按行优先顺序给出；行列都不超过 24（编号从 1 起）。
    lines = text.split("\n")
    if lines and lines[-1] == "": lines.pop()
    if not lines or lines[-1] != "-1 -1": return False
    body = lines[:-1]; cur = []; maps = 0
    for ln in body:
        p = ln.split(" ")
        if len(p) != 2 or not all(t.isdigit() for t in p): return False
        a, b = map(int, p)
        if ln != f"{a} {b}": return False
        if (a, b) == (0, 0):
            if not cur: return False
            maps += 1; cur = []; continue
        if not (1 <= a <= 24 and 1 <= b <= 24): return False
        if cur and cur[-1] >= (a, b): return False
        cur.append((a, b))
    return maps >= 1 and not cur

def fmt(maps):
    return "".join("".join(f"{a} {b}\n" for a, b in sorted(m)) + "0 0\n" for m in maps) + "-1 -1\n"

ALL = [(a, b) for a in range(1, 25) for b in range(1, 25)]

def rnd_map(r, rows=24, cols=24, k=None):
    cells = [(a, b) for a in range(1, rows + 1) for b in range(1, cols + 1)]
    k = k or r.randint(1, len(cells))
    return r.sample(cells, min(k, len(cells)))

def build_cases():
    r = random.Random(1548)
    cases = []
    # 边界：单点、(1,1)/(24,24) 角、一行、一列、反对角线（答案 24）、满格
    cases.append(fmt([[(1, 1)], [(24, 24)], [(1, 24)], [(24, 1)], [(1, 24), (24, 1)]]))
    cases.append(fmt([[(5, b) for b in range(1, 25)], [(a, 7) for a in range(1, 25)],
                      [(a, a) for a in range(1, 25)]]))
    cases.append(fmt([[(a, 25 - a) for a in range(1, 25)]]))
    cases.append(fmt([ALL]))
    cases.append(fmt([[(a, b) for a, b in ALL if a + b in (25, 26)], [(a, b) for a, b in ALL if (a + b) % 2 == 0]]))
    # 小规模随机（原数据那样的 12x12 以内）
    for _ in range(10):
        cases.append(fmt([rnd_map(r, r.randint(1, 12), r.randint(1, 12), r.randint(1, 20)) for _ in range(r.randint(1, 4))]))
    # 全尺寸随机，不同密度
    for dens in (0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.7, 0.9):
        cases.append(fmt([rnd_map(r, k=max(1, int(576 * dens))) for _ in range(r.randint(2, 6))]))
    # 阶梯 / 多条反链的结构化图，答案大
    for _ in range(4):
        m = set()
        for _ in range(r.randint(2, 6)):
            off = r.randint(-8, 8)
            m |= {(a, b) for a, b in ALL if a + b == 25 + off and r.random() < 0.8}
        m |= set(rnd_map(r, k=r.randint(1, 60)))
        cases.append(fmt([sorted(m)]))
    # 很多张图
    cases.append(fmt([rnd_map(r, k=r.randint(1, 576)) for _ in range(40)]))
    cases.append(fmt([rnd_map(r, r.randint(1, 24), r.randint(1, 24), r.randint(1, 5)) for _ in range(200)]))
    while len(cases) < 39:
        cases.append(fmt([rnd_map(r, r.randint(10, 24), r.randint(10, 24)) for _ in range(r.randint(1, 10))]))
    return cases

REFERENCE='# External reference: http://cs101.openjudge.cn/practice/01548/statistics/\n# Accepted submission: 41540671\n# Source: http://cs101.openjudge.cn/practice/solution/41540671/\n# License: not declared on the submission page; no license is inferred.\n\nwhile True:\n\tgar, ret = [], 0\n\twhile True:\n\t\tix, iy = map(int, input().split())\n\t\tif ix < 0:\n\t\t\texit(0)\n\t\tif not ix:\n\t\t\tbreak\n\t\tgar.append((ix, iy))\n\twhile gar:\n\t\tret += 1\n\t\tcy = 1\n\t\tfor i in range(len(gar)):\n\t\t\tx,y = gar[i]\n\t\t\tif y >= cy:\n\t\t\t\tcy = y\n\t\t\t\tgar[i] = None\n\t\tgar = list(filter(lambda x : x,gar))\n\tprint(ret)\n'
LANGUAGE='Python3'
SAMPLE='1 2\n1 4\n2 4\n2 6\n4 4\n4 7\n6 6\n0 0\n1 1\n2 2\n4 4\n0 0\n-1 -1\n'

def run_all(cases):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); src = tmp/('s.py' if LANGUAGE == 'Python3' else 's.cpp'); src.write_text(REFERENCE)
        cmd = [sys.executable, '-I', str(src)]
        if LANGUAGE != 'Python3':
            exe = tmp/'s'; subprocess.run(['g++', '-std=c++20', '-O2', '-pipe', str(src), '-o', str(exe)], check=True); cmd = [str(exe)]
        outs = []
        for x in cases:
            q = subprocess.run(cmd, input=x, text=True, capture_output=True, timeout=120, check=True)
            outs.append('\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines()) + '\n')
        return outs

def main():
    cases = [SAMPLE] + build_cases()
    for i, x in enumerate(cases):
        assert valid(x), f"第 {i} 组不满足题面约束"
    outs = run_all(cases)
    out = Path('data'); out.mkdir(exist_ok=True)
    for p in out.glob('*'): p.unlink()
    for i, (x, y) in enumerate(zip(cases, outs)):
        (out/f'{i}.in').write_text(x); (out/f'{i}.out').write_text(y)

if __name__ == '__main__':
    main()
