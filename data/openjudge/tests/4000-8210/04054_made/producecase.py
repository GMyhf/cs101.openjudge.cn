"""4054 Cubic Eight-Puzzle 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

2026-10 审计重写：
- 原生成器每组只有 1 个数据集，目标图案只从 4 种近乎全同色的模板里挑，40 组去重后仅 24 种，
  -1 只在样例里出现，从没有多数据集（题面最多 15 个）的大组。
- 现在：单数据集组覆盖 9 个空格起点与各种答案深度（由随机滚动生成，保证可达），多数据集组
  取满 15 个，混入随机图案（多为 -1 或接近 30 步）与深度随机滚动得到的目标。
- REFERENCE_SOURCE 是原参考解（双向 BFS，7 进制状态编码）；ORACLE_SOURCE 是独立写法
  （以「顶面 / x 轴 / y 轴」颜色三元组表示朝向，按层双向 BFS），每组都与参考解对拍。
  初始朝向（顶 W、x 轴 B、y 轴 R）由题面样例 8 个答案确定（换成 x 轴 R 时样例对不上）。
- 复核调整：困难图案（-1 / 29 / 30 步）单个参考解约 1~1.3s，原先一组塞 15 个导致单组 11~19s；
  现改为每组至多 3 个困难图案 + 12 个随机滚动目标，共 9 组，混合组相应减为 3 组，总数仍 40。
"""
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path

NUMBER = 4054
SAMPLE_IN = '1 2 \nW W W \nE W W \nW W W \n2 1 \nR B W \nR W W \nE W W \n3 3 \nW B W \nB R E \nR B R \n3 3 \nB W R \nB W R \nB E R \n2 1 \nB B B \nB R B \nB R E \n1 1 \nR R R \nW W W \nR R E \n2 1 \nR R R \nB W B \nR R E \n3 2 \nR R R \nW E W \nR R R\n0 0\n'
SAMPLE_OUT = '0\n3\n13\n23\n29\n30\n-1\n-1\n'

REFERENCE_SOURCE = "import sys\nfrom collections import deque\ndef solve(s):\n  a=s.split()\n  directions=((1,0),(0,1),(-1,0),(0,-1));rotates=((5,2,1,4,3,0),(3,4,5,0,1,2));colors={'E':(6,),'W':(0,1),'R':(2,3),'B':(4,5)};p=0;out=[]\n  def possible(target):\n   vals=[6]*9;ans=[]\n   def dfs(i):\n    if i==9:ans.append(sum(7**j*vals[j] for j in range(9)));return\n    for z in colors[target[i]]:vals[i]=z;dfs(i+1)\n   dfs(0);return target.index('E'),ans\n  def solve_one(sx,sy,target):\n   start=3*sx+sy;cur=7**start*6;q1=deque([cur]);start_sum=0\n   for _ in range(9):start_sum+=cur%7;cur//=7\n   s1={start};blank,goals=possible(target);q2=deque();\n   for z in goals:\n    v=z;sm=0\n    for _ in range(9):sm+=v%7;v//=7\n    if (sm-start_sum-blank+start)&1==0:q2.append(z)\n   s2=set(q2)\n   for depth in range(31):\n    if len(q2)<len(q1):q1,q2=q2,q1;s1,s2=s2,s1\n    for _ in range(len(q1)):\n     state=q1.popleft()\n     if state in s2:return depth\n     if depth==30:continue\n     cur=[];v=state;bx=by=pos=-1\n     for i in range(9):\n      z=v%7;v//=7;cur.append(z)\n      if z==6:bx,by,pos=i//3,i%3,i\n     for dx,dy in directions:\n      nx,ny=bx+dx,by+dy\n      if not(0<=nx<3 and 0<=ny<3):continue\n      j=nx*3+ny;new=cur[:];new[pos]=rotates[dx][cur[j]];new[j]=6;z=sum(7**i*new[i] for i in range(9))\n      if z not in s1:s1.add(z);q1.append(z)\n   return -1\n  while p<len(a):\n   sy,sx=int(a[p])-1,int(a[p+1])-1;p+=2\n   if sx==sy==-1:break\n   target=a[p:p+9];p+=9;out.append(str(solve_one(sx,sy,target)))\n  return '\\n'.join(out)+'\\n'\nsys.stdout.write(solve(sys.stdin.read()))\n"

ORACLE_SOURCE = 'import sys\n# 独立实现：每个立方体记为 (顶面色, 沿 x 方向的轴色, 沿 y 方向的轴色)；对面同色，所以 3 轴各一色。\n# 沿 x 方向滚动交换「顶」与「x 轴」，沿 y 方向滚动交换「顶」与「y 轴」。\n# 初始朝向：顶 W、x 轴 B、y 轴 R（由题面样例八组答案唯一确定）。\ndef solve(x0, y0, pat):\n    # 格子 (x,y) -> 下标 (y-1)*3+(x-1)；pat[j][i] 为第 j 行第 i 个字符 = F_{i+1, j+1}\n    start = [(\'W\', \'B\', \'R\')] * 9\n    e0 = (y0 - 1) * 3 + (x0 - 1)\n    start[e0] = None\n    start = tuple(start)\n    target = [pat[j][i] for j in range(3) for i in range(3)]\n    ge = target.index(\'E\')\n    others = {\'W\': \'BR\', \'B\': \'WR\', \'R\': \'WB\'}\n    goals = []\n    def build(i, cur):\n        if i == 9:\n            goals.append(tuple(cur)); return\n        if i == ge:\n            build(i + 1, cur + [None]); return\n        t = target[i]; a, b = others[t]\n        build(i + 1, cur + [(t, a, b)]); build(i + 1, cur + [(t, b, a)])\n    build(0, [])\n    def nbrs(s):\n        e = s.index(None); ex, ey = e % 3, e // 3\n        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n            nx, ny = ex + dx, ey + dy\n            if 0 <= nx < 3 and 0 <= ny < 3:\n                j = ny * 3 + nx; t, ax, ay = s[j]\n                c = (ax, t, ay) if dx else (ay, ax, t)\n                z = list(s); z[e] = c; z[j] = None\n                yield tuple(z)\n    da = {start: 0}; db = {g: 0 for g in goals}\n    if start in db:\n        return 0\n    fa = [start]; fb = list(goals); la = lb = 0\n    while la + lb < 30:\n        if len(fa) <= len(fb):\n            side, other, front = da, db, fa; la += 1; d = la\n        else:\n            side, other, front = db, da, fb; lb += 1; d = lb\n        new = []; best = None\n        for s in front:\n            for z in nbrs(s):\n                if z not in side:\n                    side[z] = d; new.append(z)\n                    if z in other:\n                        v = d + other[z]\n                        best = v if best is None or v < best else best\n        if side is da: fa = new\n        else: fb = new\n        if best is not None:\n            return best if best <= 30 else -1\n    return -1\na = sys.stdin.read().split(); p = 0; out = []\nwhile True:\n    x, y = int(a[p]), int(a[p + 1]); p += 2\n    if x == 0 and y == 0: break\n    pat = [a[p:p + 3], a[p + 3:p + 6], a[p + 6:p + 9]]; p += 9\n    out.append(str(solve(x, y, pat)))\nprint("\\n".join(out))\n'


def valid(text):
    """题面：若干数据集，以一行「0 0」结束，数据集个数 < 16。每个数据集：一行 x y（取 1..3），
    接着 3 行、每行 3 个用空格分隔的字符，取自 B/W/R/E，且恰有一个 E。"""
    lines = text.split("\n")
    while lines and lines[-1].strip() == "":
        lines.pop()
    rows = [ln.split() for ln in lines]
    p = 0; cnt = 0
    while True:
        if p >= len(rows) or len(rows[p]) != 2:
            return False
        if rows[p] == ["0", "0"]:
            p += 1
            break
        if rows[p][0] not in ("1", "2", "3") or rows[p][1] not in ("1", "2", "3"):
            return False
        if p + 3 >= len(rows):
            return False
        cells = []
        for q in range(p + 1, p + 4):
            if len(rows[q]) != 3 or any(ch not in ("B", "W", "R", "E") for ch in rows[q]):
                return False
            cells += rows[q]
        if cells.count("E") != 1:
            return False
        cnt += 1; p += 4
    return p == len(rows) and 1 <= cnt <= 15


# ---- 生成：从初始状态随机滚动，得到保证可达的目标 ----
def _start(x, y):
    s = [("W", "B", "R")] * 9
    s[(y - 1) * 3 + (x - 1)] = None
    return s


def _roll(s, r, prev):
    e = s.index(None); ex, ey = e % 3, e // 3
    opts = []
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = ex + dx, ey + dy
        if 0 <= nx < 3 and 0 <= ny < 3 and ny * 3 + nx != prev:
            opts.append((dx, dy, ny * 3 + nx))
    dx, dy, j = r.choice(opts)
    t, ax, ay = s[j]
    s = list(s); s[e] = (ax, t, ay) if dx else (ay, ax, t); s[j] = None
    return s, e


def walk_case(r, steps):
    x, y = r.randint(1, 3), r.randint(1, 3)
    s = _start(x, y); prev = -1
    for _ in range(steps):
        s, prev = _roll(s, r, prev)
    tops = ["E" if c is None else c[0] for c in s]
    return (x, y, tops)


def rand_case(r):
    x, y = r.randint(1, 3), r.randint(1, 3)
    tops = [r.choice("BWR") for _ in range(9)]
    tops[r.randrange(9)] = "E"
    return (x, y, tops)


def fmt(ds):
    out = []
    for x, y, tops in ds:
        out.append(f"{x} {y}")
        for j in range(3):
            out.append(" ".join(tops[3 * j:3 * j + 3]))
    out.append("0 0")
    return "\n".join(out) + "\n"


HARD_NEG = [(1, 2, 'RRRRRERRR'), (1, 3, 'BWBBEBBWB'), (2, 1, 'BBBBBBBEB'), (2, 2, 'BBBBBBBEB'),
            (2, 2, 'BEBBBBBBB'), (2, 2, 'RRRERRRRR'), (2, 2, 'RRRRRERRR'), (2, 3, 'BEBBBBBBB'),
            (3, 1, 'RRRERBRRR'), (3, 2, 'BRBBEBBBB'), (3, 2, 'BWBBBBBEB'), (3, 2, 'RRRERRRRR'),
            (3, 2, 'RRRRRBERR')]
HARD_DEEP = [(1, 2, 'RRRERRRRR'), (1, 2, 'RRRRERRRR'), (1, 2, 'RRRRRBRRE'), (2, 1, 'BBBBEBBBB'),
             (2, 1, 'BBBEBBBRB'), (2, 1, 'BEBBBBBBB'), (2, 1, 'BWBBBBEBB'), (2, 2, 'RREBRRRRR'),
             (2, 3, 'BBBBBBBEB'), (2, 3, 'BBBBEBBBB'), (2, 3, 'BBEBBBBWB'), (3, 1, 'RRRRBERRR'),
             (3, 2, 'RRRRERRRR'), (3, 2, 'RRRRRERRR')]


def build_cases():
    cases = [SAMPLE_IN]
    r = random.Random(NUMBER)
    # 9 个空格起点各一组，目标即初始图案（答案 0）
    for x in (1, 2, 3):
        for y in (1, 2, 3):
            tops = ["W"] * 9; tops[(y - 1) * 3 + (x - 1)] = "E"
            cases.append(fmt([(x, y, tops)]))
    # 单数据集：随机滚动若干步得到的可达目标，答案从小到 30 附近
    for steps in (1, 2, 3, 5, 8, 12, 16, 20, 24, 28, 32, 40, 60):
        cases.append(fmt([walk_case(r, steps)]))
    # 单数据集：随机图案（多为 -1）
    for _ in range(3):
        cases.append(fmt([rand_case(r)]))
    # 多数据集（取满 15 个）：混合
    for _ in range(3):
        ds = []
        for i in range(15):
            ds.append(rand_case(r) if i % 3 == 0 else walk_case(r, r.randint(10, 80)))
        cases.append(fmt(ds))
    # 多数据集：困难组。随机图案几乎总在 30 步内可达（实测 180 个里只有 1 个 -1），
    # 故用离线扫描（同色/近同色图案 × 9 个起点，参考解求值）得到的 -1 与 29/30 步图案；
    # 每次生成仍由参考解与独立实现双双重算对拍，不依赖扫描时的结论。
    # 每组至多 3 个困难图案（单个约 1~1.3s），再补 12 个随机滚动目标凑满 15 个数据集。
    # 不再把 15 个困难图案塞进一组：那样参考解单组 11~19s，超过判题机单组上限（CASE_CAP_S=20s）的一半。
    hard = [(x, y, list(t)) for x, y, t in HARD_NEG + HARD_DEEP]
    r.shuffle(hard)
    for g in range(0, len(hard), 3):
        ds = hard[g:g + 3] + [walk_case(r, r.randint(10, 80)) for _ in range(12)]
        r.shuffle(ds)
        cases.append(fmt(ds))
    # 多数据集：深度随机滚动
    for _ in range(2):
        cases.append(fmt([walk_case(r, r.randint(25, 200)) for _ in range(r.randint(10, 15))]))
    return cases


def _run(source, content, limit=900):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8", delete=False) as fh:
        fh.write(source)
        path = fh.name
    try:
        return subprocess.run([sys.executable, path], input=content, text=True,
                              capture_output=True, timeout=limit, check=True).stdout
    finally:
        os.unlink(path)


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert len(set(cases)) == len(cases), "组间不得重复"
    for i, c in enumerate(cases):
        assert valid(c), f"第 {i} 组越出题面约束"
    assert _run(REFERENCE_SOURCE, SAMPLE_IN) == SAMPLE_OUT, "参考解跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for old in list(root.glob("*.in")) + list(root.glob("*.out")):
        old.unlink()
    for i, c in enumerate(cases):
        out = _run(REFERENCE_SOURCE, c)
        assert _run(ORACLE_SOURCE, c).split() == out.split(), f"第 {i} 组参考解与独立实现不一致"
        (root / f"{i}.in").write_text(c, encoding="utf-8")
        (root / f"{i}.out").write_text(out, encoding="utf-8")
    print(f"generated {len(cases)} cases")


if __name__ == "__main__":
    main()
