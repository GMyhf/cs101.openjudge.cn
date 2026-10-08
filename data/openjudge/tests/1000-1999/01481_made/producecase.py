import random, subprocess, sys, tempfile
from pathlib import Path

def _components(grid, h, w, ok):
    seen = [[False] * w for _ in range(h)]; comps = []
    for i in range(h):
        for j in range(w):
            if ok(grid[i][j]) and not seen[i][j]:
                seen[i][j] = True; st = [(i, j)]; comp = []
                while st:
                    y, x = st.pop(); comp.append((y, x))
                    for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= yy < h and 0 <= xx < w and not seen[yy][xx] and ok(grid[yy][xx]):
                            seen[yy][xx] = True; st.append((yy, xx))
                comps.append(comp)
    return comps

def picture_dice(grid):
    # 返回每个骰子的点数列表（4 连通）
    h, w = len(grid), len(grid[0])
    dot_id = {}
    for k, comp in enumerate(_components(grid, h, w, lambda c: c == "X")):
        for p in comp: dot_id[p] = k
    res = []
    for comp in _components(grid, h, w, lambda c: c != "."):
        res.append(len({dot_id[p] for p in comp if p in dot_id}))
    return res

def valid(text):
    # 题面：每张图 w h（5<=w,h<=50），随后 h 行各 w 个字符，只含 . * X；至少一个骰子；
    # 每个骰子点数在 1..6；以 w=h=0 结束（其后不再有内容）。
    lines = text.split("\n")
    if lines and lines[-1] == "": lines.pop()
    i = 0
    while True:
        if i >= len(lines): return False
        p = lines[i].split()
        if len(p) != 2 or not all(t.isdigit() for t in p): return False
        w, h = map(int, p); i += 1
        if w == 0 and h == 0:
            return i == len(lines)
        if not (5 <= w <= 50 and 5 <= h <= 50): return False
        rows = lines[i:i + h]; i += h
        if len(rows) != h or any(len(r) != w or set(r) - set(".*X") for r in rows): return False
        dice = picture_dice(rows)
        if not dice or any(not 1 <= d <= 6 for d in dice): return False

DOT_SHAPES = [[(0, 0)], [(0, 0), (0, 1)], [(0, 0), (1, 0)], [(0, 0), (0, 1), (1, 0), (1, 1)],
              [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)], [(0, 0), (1, 0), (1, 1)]]

def free4(grid, h, w, cells):
    cs = set(cells)
    for y, x in cells:
        if not (0 <= y < h and 0 <= x < w) or grid[y][x] != ".": return False
        for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if (yy, xx) not in cs and 0 <= yy < h and 0 <= xx < w and grid[yy][xx] != ".": return False
    return True

def add_die(r, grid, h, w, dh, dw, k):
    for _ in range(60):
        y0, x0 = r.randint(0, h - dh), r.randint(0, w - dw)
        cells = [(y0 + a, x0 + b) for a in range(dh) for b in range(dw)]
        if dh >= 3 and dw >= 3 and r.random() < 0.5:  # 光学畸变：去掉几个角
            corners = [(y0, x0), (y0, x0 + dw - 1), (y0 + dh - 1, x0), (y0 + dh - 1, x0 + dw - 1)]
            for c in r.sample(corners, r.randint(1, 4)): cells.remove(c)
        if r.random() < 0.3:  # 边上鼓出一块
            side = r.choice(["t", "b"]); xx = r.randint(x0, x0 + dw - 1)
            cells.append((y0 - 1, xx) if side == "t" else (y0 + dh, xx))
        if not free4(grid, h, w, cells): continue
        local = {c: "*" for c in cells}
        placed = 0
        for _ in range(400):
            if placed == k: break
            shape = r.choice(DOT_SHAPES if dh * dw > 30 else DOT_SHAPES[:3])
            cy, cx = r.choice(cells)
            dot = [(cy + a, cx + b) for a, b in shape]
            if any(local.get(p) != "*" for p in dot): continue
            bad = False
            for y, x in dot:
                for nb in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                    if nb not in dot and local.get(nb) == "X": bad = True
            if bad: continue
            for p in dot: local[p] = "X"
            placed += 1
        if placed != k or "*" not in local.values(): continue
        for (y, x), c in local.items(): grid[y][x] = c
        return True
    return False

def picture(r, w, h, ndice, size=(2, 9)):
    while True:
        grid = [["."] * w for _ in range(h)]
        counts = []
        for _ in range(ndice):
            dh, dw = r.randint(*size), r.randint(*size)
            dh, dw = min(dh, h), min(dw, w)
            k = r.randint(1, 6) if dh * dw >= 12 else r.randint(1, max(1, min(6, dh * dw // 3)))
            if add_die(r, grid, h, w, dh, dw, k): counts.append(k)
        rows = ["".join(x) for x in grid]
        if counts and sorted(picture_dice(rows)) == sorted(counts):
            return f"{w} {h}\n" + "\n".join(rows) + "\n"

def serpentine(w, h):
    # 一条蛇形的单宽骰子，路径很长；两端各一个点
    grid = [["."] * w for _ in range(h)]
    for y in range(0, h, 2):
        for x in range(w): grid[y][x] = "*"
        if y + 1 < h: grid[y + 1][w - 1 if (y // 2) % 2 == 0 else 0] = "*"
    grid[0][0] = "X"; grid[0][2] = "X"; grid[h - 1 - (h - 1) % 2][w // 2] = "X"
    return f"{w} {h}\n" + "\n".join("".join(x) for x in grid) + "\n"

def build_cases():
    r = random.Random(1481)
    cases = []
    # 最小图 5x5、单骰子
    cases.append("5 5\n.....\n.***.\n.*X*.\n.***.\n.....\n5 5\nXXX**\n*****\nX*X*X\n*****\n**X**\n0 0\n")
    # 斜角相接的两个骰子 / 斜角相接的两个点 / 点贴着骰子边缘
    cases.append("6 6\n***...\n*X*...\n***...\n...***\n...*XX\n...***\n"
                 "7 5\n*******\n*X*X***\n**X*X**\n*X*****\n*******\n"
                 "8 5\nX*****X.\n******..\n..**....\n.*X*X*..\n.*****..\n0 0\n")
    for _ in range(12):
        pics = []
        for _ in range(r.randint(1, 4)):
            w, h = r.randint(5, 25), r.randint(5, 25)
            pics.append(picture(r, w, h, r.randint(1, 5)))
        cases.append("".join(pics) + "0 0\n")
    for _ in range(10):
        pics = []
        for _ in range(r.randint(2, 6)):
            w, h = r.randint(30, 50), r.randint(30, 50)
            pics.append(picture(r, w, h, r.randint(5, 30)))
        cases.append("".join(pics) + "0 0\n")
    # 满规模 50x50：很多小骰子 / 一个大骰子 / 蛇形长骰子
    cases.append("".join(picture(r, 50, 50, 80, size=(2, 5)) for _ in range(5)) + "0 0\n")
    cases.append(picture(r, 50, 50, 1, size=(40, 50)) + picture(r, 50, 50, 3, size=(15, 25)) + "0 0\n")
    cases.append(serpentine(50, 50) + serpentine(49, 50) + serpentine(5, 5) + "0 0\n")
    cases.append("".join(picture(r, 50, 50, 40) for _ in range(20)) + "0 0\n")
    while len(cases) < 39:
        pics = [picture(r, r.randint(5, 50), r.randint(5, 50), r.randint(1, 20)) for _ in range(r.randint(1, 8))]
        cases.append("".join(pics) + "0 0\n")
    return cases

REFERENCE="# External reference: statistics page /practice/01481/\n# Accepted submission: 42325727\n# Source: http://cs101.openjudge.cn/practice/solution/42325727/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nsys.setrecursionlimit(10**8)\ndx=[0,0,1,-1]\ndy=[1,-1,0,0]\ndef ddfs(s,e):\n    mmap[s][e]='*'\n    for i in range(4):\n        xx=s+dx[i]\n        yy=e+dy[i]\n        if 0<=xx<h and 0<=yy<w and mmap[xx][yy]=='X':\n            ddfs(xx,yy)\n\ndef dfs(s,e):\n    mmap[s][e]='.'\n    for i in range(4):\n        xx=s+dx[i]\n        yy=e+dy[i]\n        if not (0<=xx<h and 0<=yy<w) or mmap[xx][yy]=='.':\n            continue\n        if mmap[xx][yy]=='X':\n            ddfs(xx,yy)\n            num[l]+=1\n        if mmap[xx][yy]=='*':\n            dfs(xx,yy)\n\nk=1\nwhile True:\n    w,h=map(int,input().split())\n    if w==0 and h==0:\n        break\n    mmap=[]\n    for _ in range(h):\n        row=list(input().strip())\n        mmap.append(row)\n    num=[0]*1000\n    l=0\n    for i in range(h):\n        for j in range(w):\n            if mmap[i][j]=='*':\n                dfs(i,j)\n                l+=1\n    print(f'Throw {k}')\n    k+=1\n    sorted_nums=sorted(num[:l])\n    print(' '.join(map(str,sorted_nums)))\n    print()\n"
SAMPLE='30 15\n..............................\n..............................\n...............*..............\n...*****......****............\n...*X***.....**X***...........\n...*****....***X**............\n...***X*.....****.............\n...*****.......*..............\n..............................\n........***........******.....\n.......**X****.....*X**X*.....\n......*******......******.....\n.....****X**.......*X**X*.....\n........***........******.....\n..............................\n0 0\n'
LANGUAGE='Python3'

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
