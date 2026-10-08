import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/19974 statistics, Accepted solution 28435155.\n# Source: http://cs101.openjudge.cn/practice/solution/28435155/\n# Statistics: http://cs101.openjudge.cn/practice/19974/statistics/\n# License: not declared on submission page; no license inferred\nt = int(input())\nlis = []\nfor T in range(t):\n    m,p,q = input().split()\n    m = int(m)\n    p = int(p)\n    q = int(q)\n    num = 0\n    if m == 0:\n        lis.append('0')\n    elif m > 0:\n        mat = [[0 for _ in range(q+1)]for _ in range(p+1)]\n        for j in range(q+1):\n            if j < m:\n                mat[0][j] = 1\n        for i in range(p+1):\n            mat[i][0] = 1\n        for j in range(1,q+1):\n            for i in range(1,p+1):\n                if j >= i+m:\n                    mat[i][j] = 0\n                else:\n                    mat[i][j] = mat[i-1][j] + mat[i][j-1]\n        lis.append(str(mat[p][q]))\n    elif m < 0:\n        m = -m\n        mat = [[0 for _ in range(q+1)]for _ in range(p+1)]\n        for i in range(p+1):\n            if i < m:\n                mat[i][0] = 1\n        for j in range(q+1):\n            mat[0][j] = 1\n        for j in range(1,q+1):\n            for i in range(1,p+1):\n                if j <= i-m:\n                    mat[i][j] = 0\n                else:\n                    mat[i][j] = mat[i-1][j] + mat[i][j-1]\n        lis.append(str(mat[p][q]))\nfor _ in lis:\n    print(_)\n"
LANGUAGE='Python3'
SAMPLE='1\n1 2 2\n'
GENERATOR_NAME='g19974'
def g19974(r):
    t=r.randint(1,8); return f"{t}\n"+"\n".join(f"{r.randint(-5,5)} {r.randint(1,15)} {r.randint(1,15)}" for _ in range(t))+"\n"

def valid(text):
    """题面契约：首行正整数 t，其后恰 t 行，每行三个整数 m p q，p、q 为正数。
    题面没给 m、p、q、t 的上界，这里只核格式与 p,q>=1。"""
    import re
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]) or len(lines) != int(lines[0]) + 1:
        return False
    for ln in lines[1:]:
        m = re.fullmatch(r"(-?\d+) (\d+) (\d+)", ln)
        if not m or int(m[2]) < 1 or int(m[3]) < 1:
            return False
    return True

def gwide(r, t, mlo, mhi, pqmax, fixed=()):
    """追加组：题面无上界，取 p+q<=60 使答案 C(60,30)≈1.2e17 仍在 64 位内，
    同时足以卡掉不带记忆化的递归（指数级）。fixed 为固定的边界行。"""
    rows = [f"{m} {p} {q}" for m, p, q in fixed]
    while len(rows) < t:
        p = r.randint(1, pqmax); q = r.randint(1, min(pqmax, 60 - p))
        rows.append(f"{r.randint(mlo, mhi)} {p} {q}")
    return f"{t}\n" + "\n".join(rows) + "\n"

FIXED = [
    (0, 1, 1), (0, 30, 30),        # m=0：起点就在边境线上
    (1, 1, 1), (-1, 1, 1),         # 一侧路径被挡，只剩 1 条
    (1, 1, 2), (-1, 2, 1),         # 终点落在边境线上：0
    (2, 1, 2), (-2, 2, 1), (1, 1, 5), (-1, 5, 1),  # 后两行终点在线另一侧：0
    (1, 30, 30), (-1, 30, 30),     # 紧贴对角线，答案是 Catalan 型
    (100, 30, 30), (-100, 30, 30), # 边境线够远：全部 C(60,30) 条路
    (31, 30, 30), (-31, 30, 30), (30, 1, 29), (-30, 29, 1),
    (5, 1, 59), (-5, 59, 1), (60, 1, 59), (-60, 59, 1),
]
EXTRA = [  # (种子, t, m 下界, m 上界, p/q 上界, 是否带固定行)
    (301, len(FIXED), 0, 0, 1, True),
    (302, 20, -10, 10, 59, False),
    (303, 20, -60, 60, 59, False),
    (304, 20, 1, 3, 30, False),
    (305, 20, -3, -1, 30, False),
    (306, 1, 2, 2, 30, False),
]

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/'main.py'
        src.write_text(REFERENCE); cmd=[sys.executable,str(src)]
        if LANGUAGE=="G++":
            exe=d/"main"; subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],check=True)
            cmd=[str(exe)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 34)]  # 尾部 6 组让给下面的定制组，总数仍为 40（catalog 按文件列组）
    cases+=[gwide(random.Random(sd), t, a, b, pq, FIXED if f else ()) for sd, t, a, b, pq, f in EXTRA]
    assert len(cases) == 40 and len(set(cases)) == 40 and all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
