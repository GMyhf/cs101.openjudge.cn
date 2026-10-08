import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/21577/\n# Accepted submission: 52726677\n# Source: http://cs101.openjudge.cn/practice/solution/52726677/\n# License: not declared on the submission page; no license is inferred.\n\n\ndef max_area(line,c):\n    stack=[-1]\n    m=-114514\n    line.append(0)\n    for i in range(c+1):\n        while stack[-1]!=-1 and line[i]<line[stack[-1]]:\n            idx=stack.pop()\n            now_area=line[idx]*(i-stack[-1]-1)\n            if now_area>m:\n                m=now_area\n        stack.append(i)\n    return m\n\nans=float("-inf")\nr,c=map(int,input().split())\ntrees=[]\nfor i in range(r):\n    trees.append(list(map(int,input().split())))\nmatrix=[[0 for _ in range(c)] for _ in range(r)]\nfor i in range(c):\n    if trees[0][i]==0:\n        matrix[0][i]=1\nfor i in range(c):\n    for j in range(1,r):\n        if trees[j][i]==0:\n            matrix[j][i]=matrix[j-1][i]+1\n        else:\n            matrix[j][i]=0\nfor line in matrix:\n    ans=max(ans,max_area(line,c))\nprint(ans)\n'
SAMPLE='4 5\n0 1 0 1 1\n0 1 0 0 1\n0 0 0 0 0\n0 1 1 0 1\n'
GENERATOR_NAME='g21577'
def valid(text):
    """题面：第一行正整数 m n（长宽都 <=20）；接着 m 行、每行 n 个 0/1。
    输出保证为正整数，即矩阵中至少有一个 0。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    head = lines[0].split(" ")
    if len(head) != 2 or not all(t.isdigit() and t[0] != "0" for t in head):
        return False
    m, n = map(int, head)
    if not (1 <= m <= 20 and 1 <= n <= 20) or len(lines) != m + 1:
        return False
    zero = False
    for line in lines[1:]:
        toks = line.split(" ")
        if len(toks) != n or any(t not in ("0", "1") for t in toks):
            return False
        zero = zero or "0" in toks
    return zero

def _fmt(g):
    return f"{len(g)} {len(g[0])}\n" + "".join(" ".join(map(str, row)) + "\n" for row in g)

def g21577(r, s):
    k = s - 1
    if k == 0:
        g = [[0]]
    elif k == 1:
        g = [[0] * 20 for _ in range(20)]                      # 全空地，答案 400
    elif k == 2:
        g = [[0] * 20]                                          # 1 行
    elif k == 3:
        g = [[0] for _ in range(20)]                            # 1 列
    elif k == 4:
        g = [[0] * 20 for _ in range(20)]; g[10][10] = 1        # 中间一棵树
    elif k == 5:
        g = [[1] * 20 for _ in range(20)]; g[19][0] = 0         # 只有一个角是空地，答案 1
    elif k == 6:
        # 细长矩形 1x20 比任何正方形都大
        g = [[1 if (i + j) % 2 else 0 for j in range(20)] for i in range(20)]
        g[7] = [0] * 20
    elif k == 7:
        # 2x10 与 4x4 竞争：最大的不是正方形
        g = [[1] * 20 for _ in range(20)]
        for i in range(2, 6):
            for j in range(2, 6): g[i][j] = 0
        for i in range(12, 14):
            for j in range(5, 15): g[i][j] = 0
    elif k == 8:
        # 1 x 20 的一行树把场地分成上下两块
        g = [[0] * 20 for _ in range(20)]
        g[6] = [1] * 20
    elif k == 9:
        g = [[1] * 20 for _ in range(20)]
        for i in range(20): g[i][3] = 0                          # 20x1 的空列
    else:
        m = r.choice([20, 20, r.randint(1, 20)])
        n = r.choice([20, 20, r.randint(1, 20)])
        dens = [0.03, 0.08, 0.15, 0.3, 0.5, 0.7][k % 6]
        g = [[1 if r.random() < dens else 0 for _ in range(n)] for _ in range(m)]
        if all(v for row in g for v in row):
            g[r.randrange(m)][r.randrange(n)] = 0
    return _fmt(g)

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[g21577(random.Random(s), s) for s in range(1, 40)]
    for i,c in enumerate(cases):
        assert valid(c), i
        (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
