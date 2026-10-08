import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19971 statistics, Accepted solution 43885342.\n# Source: http://cs101.openjudge.cn/practice/solution/43885342/\n# Statistics: http://cs101.openjudge.cn/practice/19971/statistics/\n# License: not declared on submission page; no license inferred\na=[[1]]\nfor i in range(1,1001):\n    a.append([1])\n    if i%2:\n        for j in range(i//2):a[-1].append(a[-2][j]+a[-2][j+1])\n    else:\n        for j in range(i//2-1):a[-1].append(a[-2][j]+a[-2][j+1])\n        a[-1].append(a[-2][-1]*2)\nfor i in range(int(input())):c,b=map(int,input().split());print(a[b][b-c]if c*2>b else a[b][c])\n'
LANGUAGE='Python3'
SAMPLE='3\n2 4\n10 34\n2 7\n'
GENERATOR_NAME='g19971'
def g19971(r):
    t=r.randint(1,12); return f"{t}\n"+"\n".join((lambda b: f"{r.randint(0,b)} {b}")(r.randint(0,100)) for _ in range(t))+"\n"

def valid(text):
    """题面契约：首行 t（t<=100000），其后恰 t 行，每行两个整数 a b，0<=a<=b<=1000。"""
    import re
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"\d+", lines[0]):
        return False
    t = int(lines[0])
    if not 1 <= t <= 100000 or len(lines) != t + 1:
        return False
    for ln in lines[1:]:
        m = re.fullmatch(r"(\d+) (\d+)", ln)
        if not m or not 0 <= int(m[1]) <= int(m[2]) <= 1000:
            return False
    return True

def gpairs(r, t, bmax, edge=()):
    """追加组：t 行，b 取 [0,bmax]，a 取 [0,b]；edge 里的固定对放在最前面。"""
    rows = [f"{a} {b}" for a, b in edge]
    while len(rows) < t:
        b = r.randint(0, bmax); rows.append(f"{r.randint(0, b)} {b}")
    return f"{t}\n" + "\n".join(rows) + "\n"

EDGE = [(0, 0), (0, 1), (1, 1), (0, 1000), (1000, 1000), (1, 1000), (999, 1000), (500, 1000), (499, 999), (33, 67)]
EXTRA = [  # (种子, t, b 上界, 是否先放边界对)
    (201, 10, 1000, True),       # 边界：a=0、a=b、b=0、b=1000、C(1000,500)
    (202, 100000, 60, False),    # t 满规模（答案仍可达 1e17，卡 int32）
    (203, 100000, 34, False),    # t 满规模、答案落在 int32 附近
    (204, 8000, 1000, True),     # b 贴上界的大数（输出 <2MB）
    (205, 8000, 1000, False),
    (206, 2000, 200, False),     # 答案超出 64 位
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
    cases+=[gpairs(random.Random(sd), t, bm, EDGE if e else ()) for sd, t, bm, e in EXTRA]
    assert len(cases) == 40 and len(set(cases)) == 40 and all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
