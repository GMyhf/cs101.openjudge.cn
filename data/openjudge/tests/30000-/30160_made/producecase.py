import random
# 原参考解（提交 50848044）只做行列推理，遇到唯一解但需要试填的盘面会死循环；
# 换成「行列推理 + 分支搜索」的完整解法，下面 valid() 也用它核唯一解。
REFERENCE="import sys\n\ndef cands(clue, n):\n    # 长度 n 的行里满足提示 clue 的所有填法（bit j 表示第 j 格涂黑）\n    res = []\n    def rec(k, start, mask):\n        if k == len(clue):\n            res.append(mask); return\n        need = sum(clue[k:]) + len(clue) - k - 1\n        for s in range(start, n - need + 1):\n            rec(k + 1, s + clue[k] + 1, mask | (((1 << clue[k]) - 1) << s))\n    rec(0, 0, 0)\n    return res\n\ndef search(rows, cols, R, C, limit, found):\n    rows = [list(x) for x in rows]; cols = [list(x) for x in cols]\n    changed = True\n    while changed:\n        changed = False\n        for i in range(R):\n            if not rows[i]: return\n            a = -1; o = 0\n            for m in rows[i]: a &= m; o |= m\n            for j in range(C):\n                if a >> j & 1:\n                    nl = [m for m in cols[j] if m >> i & 1]\n                elif not (o >> j & 1):\n                    nl = [m for m in cols[j] if not (m >> i & 1)]\n                else: continue\n                if len(nl) != len(cols[j]): cols[j] = nl; changed = True\n                if not nl: return\n        for j in range(C):\n            a = -1; o = 0\n            for m in cols[j]: a &= m; o |= m\n            for i in range(R):\n                if a >> i & 1:\n                    nl = [m for m in rows[i] if m >> j & 1]\n                elif not (o >> i & 1):\n                    nl = [m for m in rows[i] if not (m >> j & 1)]\n                else: continue\n                if len(nl) != len(rows[i]): rows[i] = nl; changed = True\n                if not nl: return\n    best = -1\n    for i in range(R):\n        if len(rows[i]) > 1 and (best < 0 or len(rows[i]) < len(rows[best])): best = i\n    if best < 0:\n        found.append([m for m in (x[0] for x in rows)]); return\n    for m in rows[best]:\n        nr = rows[:]; nr[best] = [m]\n        search(nr, cols, R, C, limit, found)\n        if len(found) >= limit: return\n\ndef solve_all(R, C, rc, cc, limit=2):\n    rows = [cands(x, C) for x in rc]; cols = [cands(x, R) for x in cc]\n    found = []\n    search(rows, cols, R, C, limit, found)\n    return found\n\ndef main():\n    data = sys.stdin.read().split(); p = 0\n    R, C = int(data[0]), int(data[1]); p = 2\n    rc = []; cc = []\n    for _ in range(R):\n        k = int(data[p]); rc.append([int(x) for x in data[p+1:p+1+k]]); p += 1 + k\n    for _ in range(C):\n        k = int(data[p]); cc.append([int(x) for x in data[p+1:p+1+k]]); p += 1 + k\n    sol = solve_all(R, C, rc, cc, 1)[0]\n    sys.stdout.write(''.join(''.join('1' if m >> j & 1 else '0' for j in range(C)) + '\\n' for m in sol))\n\nif __name__ == '__main__':\n    main()\n"
SAMPLE='5 5\n1 3\n1 2\n1 1\n2 2 1\n1 4\n1 2\n1 2\n2 1 1\n2 2 2\n1 3\n'
GENERATOR_NAME='g30160'
CPP=False
_NS = {}
exec(REFERENCE.replace("if __name__ == '__main__':", "if False:"), _NS)

def clue(line):
    out=[]; run=0
    for x in list(line) + [0]:
        if x: run += 1
        elif run: out.append(run); run=0
    return out

def valid(text):
    # 题面：第一行 R C（R,C<=10）；接着 R 行行提示、C 行列提示，每行首个数为提示个数 k，后跟 k 个正整数；保证唯一解
    if not text.endswith('\n'): return False
    lines = text[:-1].split('\n')
    try:
        head = [int(x) for x in lines[0].split(' ')]
        if len(head) != 2: return False
        R, C = head
        if not (1 <= R <= 10 and 1 <= C <= 10) or len(lines) != 1 + R + C: return False
        clues = []
        for idx, ln in enumerate(lines[1:]):
            t = [int(x) for x in ln.split(' ')]
            k = t[0]
            if k < 0 or len(t) != 1 + k or any(x < 1 for x in t[1:]): return False
            n = C if idx < R else R
            if k and sum(t[1:]) + k - 1 > n: return False
            clues.append(t[1:])
    except ValueError: return False
    return len(_NS['solve_all'](R, C, clues[:R], clues[R:], 2)) == 1

def board_case(b):
    R, C = len(b), len(b[0])
    rows = [clue(x) for x in b]; cols = [clue([b[i][j] for i in range(R)]) for j in range(C)]
    return f"{R} {C}\n" + "\n".join(" ".join(map(str, [len(x)] + x)) for x in rows + cols) + "\n"

def line_solvable(text):
    # 只靠行列推理（不分支）能否解出：原参考解只能处理这一类
    d = [int(x) for x in text.split()]; R, C = d[0], d[1]; p = 2; cl = []
    for _ in range(R + C): k = d[p]; cl.append(d[p+1:p+1+k]); p += 1 + k
    rows = [_NS['cands'](x, C) for x in cl[:R]]; cols = [_NS['cands'](x, R) for x in cl[R:]]
    found = []
    s = _NS['search']
    # 把分支禁掉：只推理一次，看是否每行只剩一种
    import types
    rows2 = [list(x) for x in rows]; cols2 = [list(x) for x in cols]
    changed = True
    while changed:
        changed = False
        for i in range(R):
            a=-1; o=0
            for m in rows2[i]: a&=m; o|=m
            for j in range(C):
                if a>>j&1: nl=[m for m in cols2[j] if m>>i&1]
                elif not (o>>j&1): nl=[m for m in cols2[j] if not (m>>i&1)]
                else: continue
                if len(nl)!=len(cols2[j]): cols2[j]=nl; changed=True
        for j in range(C):
            a=-1; o=0
            for m in cols2[j]: a&=m; o|=m
            for i in range(R):
                if a>>i&1: nl=[m for m in rows2[i] if m>>j&1]
                elif not (o>>i&1): nl=[m for m in rows2[i] if not (m>>j&1)]
                else: continue
                if len(nl)!=len(rows2[i]): rows2[i]=nl; changed=True
    return all(len(x) == 1 for x in rows2)

def unique_board(r, R, C, p, need_search=None):
    while True:
        b = [[1 if r.random() < p else 0 for _ in range(C)] for _ in range(R)]
        t = board_case(b)
        if not valid(t): continue
        if need_search is not None and line_solvable(t) == need_search: continue
        return t

def all_cases():
    r = random.Random(30160)
    out = [SAMPLE]
    out.append(board_case([[0]])); out.append(board_case([[1]]))
    out.append(board_case([[1] * 10 for _ in range(10)]))
    out.append(board_case([[0] * 10 for _ in range(10)]))
    out.append(board_case([[1, 0, 1, 1, 0, 1, 1, 1, 0, 1]]))          # 1 x 10
    out.append(board_case([[x] for x in [1, 1, 0, 1, 0, 0, 1, 1, 1, 1]]))  # 10 x 1
    out.append(board_case([[1 if (i == j or i + j == 9) else 0 for j in range(10)] for i in range(10)][:1] + [[1]*10]))
    for (R, C, p) in [(1, 7, .5), (7, 1, .5), (2, 3, .5), (3, 2, .6), (4, 4, .6), (5, 5, .5), (6, 8, .6),
                      (8, 6, .7), (9, 10, .6), (10, 9, .7), (10, 10, .6), (10, 10, .7), (10, 10, .5),
                      (10, 10, .3), (10, 10, .8), (3, 10, .5), (10, 3, .5)]:
        out.append(unique_board(r, R, C, p))
    for _ in range(12):
        out.append(unique_board(r, 10, 10, r.choice([.5, .6, .7]), need_search=False))
    for _ in range(5):                # 唯一解但光靠推理解不出、必须试填
        out.append(unique_board(r, 10, 10, r.choice([.5, .6]), need_search=True))
    for _ in range(4):
        out.append(unique_board(r, r.randint(1, 10), r.randint(1, 10), r.random()))
    return out

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=all_cases()
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
