import random,subprocess,sys,tempfile
from pathlib import Path
import re
def valid(text):
    """题面契约：首行 t（1..10）；每组一行 W H n（1 ≤ W,H ≤ 100），随后两行各 n 对坐标
    0 ≤ x < W、0 ≤ y < H。棋子落在格点上，同一块棋盘上的坐标互不相同（故 n ≤ W*H）。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    num = re.compile(r'(0|[1-9][0-9]*)$')
    def ints(line, cnt):
        toks = line.split(' ')
        if len(toks) != cnt or not all(num.match(x) for x in toks):
            return None
        return list(map(int, toks))
    head = ints(lines[0], 1) if lines else None
    if head is None or not 1 <= head[0] <= 10 or len(lines) != 1 + 3 * head[0]:
        return False
    for c in range(head[0]):
        whn = ints(lines[1 + 3 * c], 3)
        if whn is None:
            return False
        W, H, n = whn
        if not (1 <= W <= 100 and 1 <= H <= 100 and 1 <= n <= W * H):
            return False
        for line in lines[2 + 3 * c:4 + 3 * c]:
            v = ints(line, 2 * n)
            if v is None:
                return False
            pts = list(zip(v[::2], v[1::2]))
            if len(set(pts)) != n or not all(x < W and y < H for x, y in pts):
                return False
    return True
_TRANS = [lambda x, y: (x, y), lambda x, y: (y, -x), lambda x, y: (-x, -y), lambda x, y: (-y, x),
          lambda x, y: (-x, y), lambda x, y: (y, x), lambda x, y: (x, -y), lambda x, y: (-y, -x)]
def _grow(r, size):
    """随机生长一个 size 格的四连通块，返回归一化坐标集合。"""
    cells = {(0, 0)}; frontier = [(0, 0)]
    while len(cells) < size:
        x, y = r.choice(frontier)
        dx, dy = r.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        c = (x + dx, y + dy)
        if c not in cells:
            cells.add(c); frontier.append(c)
    return _norm(cells)
def _norm(cells):
    mx = min(x for x, _ in cells); my = min(y for _, y in cells)
    return {(x - mx, y - my) for x, y in cells}
def _place(r, shapes, W, H, tries=400):
    """把若干块放进 W×H，块与块之间不四连通相邻；失败返回 None。"""
    occ = set(); pts = []
    for sh in shapes:
        w = max(x for x, _ in sh) + 1; h = max(y for _, y in sh) + 1
        if w > W or h > H:
            return None
        for _ in range(tries):
            ox = r.randrange(W - w + 1); oy = r.randrange(H - h + 1)
            cur = [(x + ox, y + oy) for x, y in sh]
            if all((a, b) not in occ and (a + 1, b) not in occ and (a - 1, b) not in occ
                   and (a, b + 1) not in occ and (a, b - 1) not in occ for a, b in cur):
                occ.update(cur); pts += cur; break
        else:
            return None
    return pts
def _shape_key(sh):
    best = None
    for t in _TRANS:
        k = tuple(sorted(_norm({t(x, y) for x, y in sh})))
        best = k if best is None or k < best else best
    return best
def _fmt(pts, r):
    pts = list(pts); r.shuffle(pts)
    return ' '.join(f'{x} {y}' for x, y in pts)
def _case(r, W, H, kind, budget):
    """kind: yes / no_shape（同尺寸不同形）/ no_split（总数相同、块划分不同）。
    放不下就重抽，连续失败 20 次把总格数减半（确定性，只依赖种子）。"""
    if kind == 'no_shape' and (budget < 4 or min(W, H) == 1):
        kind = 'no_split'                    # 太少的格子或一条线的棋盘造不出「同尺寸不同形」
    fails = 0
    while True:
        fails += 1
        if fails % 20 == 0:
            budget = max({'yes': 1, 'no_split': 2, 'no_shape': 4}[kind], budget // 2)
        if fails >= 200:
            kind = 'yes'                     # 兜底，保证必然终止
        shapes = []; total = 0
        while total < budget:
            s = min(budget - total, r.choice([1, 1, 2, 3, 4, 5, 6, 8, 12, 20, 40]))
            shapes.append(_grow(r, s)); total += s
        if kind == 'no_shape':
            cand = [i for i, s in enumerate(shapes) if len(s) >= 4]
            if not cand:
                continue
            i = r.choice(cand)
            for _ in range(50):
                other = _grow(r, len(shapes[i]))
                if _shape_key(other) != _shape_key(shapes[i]):
                    break
            else:
                continue
            shapes2 = shapes[:i] + [other] + shapes[i + 1:]
        elif kind == 'no_split':
            cand = [i for i, s in enumerate(shapes) if len(s) >= 2]
            if not cand:
                continue
            i = r.choice(cand); s = len(shapes[i]); a = r.randint(1, s - 1)
            shapes2 = shapes[:i] + [_grow(r, a), _grow(r, s - a)] + shapes[i + 1:]
        else:
            shapes2 = list(shapes)
        shapes2 = [_norm({t(x, y) for x, y in sh}) for sh, t in ((sh, r.choice(_TRANS)) for sh in shapes2)]
        r.shuffle(shapes2)
        b1 = _place(r, shapes, W, H); b2 = _place(r, shapes2, W, H)
        if b1 is None or b2 is None:
            continue
        if r.random() < 0.5:
            b1, b2 = b2, b1
        return f"{W} {H} {len(b1)}\n{_fmt(b1, r)}\n{_fmt(b2, r)}"
def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    cases = []
    if seed == 1:
        cases = ["1 1 1\n0 0\n0 0", "2 1 1\n0 0\n1 0", "2 2 2\n0 0 1 1\n0 0 0 1",
                 "2 2 2\n0 1 1 0\n1 1 0 0", "3 3 3\n0 0 1 0 2 0\n1 0 1 1 1 2", "3 3 3\n0 0 2 0 1 1\n0 0 1 1 2 2"]
    elif seed == 2:
        full = ' '.join(f'{x} {y}' for x in range(100) for y in range(100))
        rev = ' '.join(f'{x} {y}' for x in reversed(range(100)) for y in range(100))
        cases = [f"100 100 10000\n{full}\n{rev}"]
    elif seed == 3:
        line = ' '.join(f'{x} 0' for x in range(100)); col = ' '.join(f'0 {y}' for y in range(100))
        cases = [f"100 100 100\n{line}\n{col}", f"100 1 100\n{line}\n{line}", f"1 100 100\n{col}\n{col}"]
    else:
        t = 10 if seed % 3 else r.randint(1, 10)
        big = seed >= 28
        for _ in range(t):
            W = r.randint(60, 100) if big else r.randint(1, 30)
            H = r.randint(60, 100) if big else r.randint(1, 30)
            cap = W * H // (6 if big else 5)
            budget = r.randint(1, max(1, cap if big else min(cap, 60)))
            kind = r.choice(['yes', 'yes', 'no_shape', 'no_split'])
            if budget < 2:
                kind = 'yes'
            cases.append(_case(r, W, H, kind, budget))
    return f"{len(cases)}\n" + "\n".join(cases) + "\n"
NO_INPUT={3225, 2698}
REFERENCE='# External reference: http://cs101.openjudge.cn/practice/01021/statistics/\n# Accepted submission: 48421084\n# Source: http://cs101.openjudge.cn/practice/solution/48421084/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nfrom collections import deque\n\ndef find_clusters(points):\n    visited = set()\n    clusters = []\n    points = set(points)\n    for point in points:\n        if point not in visited:\n            queue = deque()\n            queue.append(point)\n            visited.add(point)\n            cluster = []\n            while queue:\n                x, y = queue.popleft()\n                cluster.append((x, y))\n                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n                    neighbor = (x + dx, y + dy)\n                    if neighbor in points and neighbor not in visited:\n                        visited.add(neighbor)\n                        queue.append(neighbor)\n            clusters.append(cluster)\n    return clusters\n\ndef get_feature(cluster):\n    transforms = [\n        lambda x, y: (x, y),\n        lambda x, y: (y, -x),\n        lambda x, y: (-x, -y),\n        lambda x, y: (-y, x),\n        lambda x, y: (-x, y),\n        lambda x, y: (y, x),\n        lambda x, y: (x, -y),\n        lambda x, y: (-y, -x),\n    ]\n    min_feature = None\n    for t in transforms:\n        transformed = [t(x, y) for x, y in cluster]\n        min_x = min(p[0] for p in transformed)\n        min_y = min(p[1] for p in transformed)\n        normalized = [(p[0] - min_x, p[1] - min_y) for p in transformed]\n        normalized.sort()\n        feature = tuple(normalized)\n        if (min_feature is None) or (feature < min_feature):\n            min_feature = feature\n    return min_feature\n\ndef main():\n    t = int(sys.stdin.readline())\n    for _ in range(t):\n        W, H, n = map(int, sys.stdin.readline().split())\n        points1 = list(map(int, sys.stdin.readline().split()))\n        points1 = [(points1[i], points1[i+1]) for i in range(0, 2*n, 2)]\n        points2 = list(map(int, sys.stdin.readline().split()))\n        points2 = [(points2[i], points2[i+1]) for i in range(0, 2*n, 2)]\n        clusters1 = find_clusters(points1)\n        clusters2 = find_clusters(points2)\n        features1 = [get_feature(cluster) for cluster in clusters1]\n        features2 = [get_feature(cluster) for cluster in clusters2]\n        features1.sort()\n        features2.sort()\n        print("YES" if features1 == features2 else "NO")\n\nif __name__ == "__main__":\n    main()\n'
LANGUAGE='Python3'
NUMBER=1021
SAMPLE='2\n8 5 11\n0 0 1 0 2 0 5 0 7 0 1 1 2 1 5 1 3 3 5 2 4 4\n0 4 0 3 0 2 1 1 1 4 1 3 3 3 5 2 6 2 7 2 7 4\n8 5 11\n0 0 1 0 2 0 5 0 7 0 1 1 2 1 5 1 3 3 6 1 4 4\n0 4 0 3 0 2 1 1 1 4 1 3 3 3 5 2 6 2 7 2 7 4\n'
def main():
 with tempfile.TemporaryDirectory() as d:
  d=Path(d);src=d/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE);cmd=[sys.executable,'-I',str(src)]
  if LANGUAGE!='Python3':
   exe=d/'s';subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]
  out=Path('data');out.mkdir(exist_ok=True)
  for p in out.glob('*'):p.unlink()
  cases=([SAMPLE] if SAMPLE or NUMBER in (2698,3225) else [])+([] if NUMBER in (2698,3225) else [generate(NUMBER,s) for s in range(1, 40)])
  for i,x in enumerate(cases):
   q=subprocess.run(cmd,input=x,text=True,capture_output=True,timeout=120,check=True);(out/f'{i}.in').write_text(x);(out/f'{i}.out').write_text(q.stdout.rstrip()+'\n')
if __name__=='__main__':main()
