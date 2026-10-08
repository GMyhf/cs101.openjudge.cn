import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19164 statistics, Accepted solution 51285327.\n# Source: http://cs101.openjudge.cn/practice/solution/51285327/\n# Statistics: http://cs101.openjudge.cn/practice/19164/statistics/\n# License: not declared on submission page; no license inferred\nT, M = map(int, input().split())\np = []\nn = []\nfor _ in range(T):\n    P, N = map(int, input().split())\n    p.append(P)\n    n.append(N)\nnow_p, now_n = p[0], n[0]\nfor i in range(1, T):\n    last_p, last_n = now_p, now_n\n    now_p = max(last_p+p[i], last_n+p[i]-M)\n    now_n = max(last_n+n[i], last_p+n[i]-M)\nprint(max(now_p, now_n))\n'
LANGUAGE='Python3'
SAMPLE='4 3\n10 9\n2 8\n9 5\n8 2\n'
GENERATOR_NAME='g19164'
def valid(text):
    """题面：第一行 T M（1<=T<=100, 1<=M<=100）；接下来 T 行每行两个 1..100 的整数。"""
    lines=text.split("\n")
    if lines[-1]!="": return False
    lines=lines[:-1]
    def ints(line):
        t=line.split(" ")
        if len(t)!=2 or not all(x.isdigit() and str(int(x))==x for x in t): return None
        return list(map(int,t))
    if not lines: return False
    h=ints(lines[0])
    if h is None: return False
    T,M=h
    if not (1<=T<=100 and 1<=M<=100) or len(lines)!=T+1: return False
    for line in lines[1:]:
        v=ints(line)
        if v is None or not all(1<=x<=100 for x in v): return False
    return True

def _big(seed):
    """补充：T、M 取到上限 100 / 下限 1，营业额取满 1..100，含频繁小幅交替（贪心逐月取大者会错）。"""
    r=random.Random(seed); out=[]
    def mk(t,m,f): return f"{t} {m}\n"+"\n".join(f(i) for i in range(t))+"\n"
    out.append(mk(100,100,lambda i:f"{r.randint(1,100)} {r.randint(1,100)}"))
    out.append(mk(100,1,lambda i:f"{r.randint(1,100)} {r.randint(1,100)}"))
    out.append(mk(100,50,lambda i:f"{r.randint(1,100)} {r.randint(1,100)}"))
    out.append(mk(100,100,lambda i:"100 1" if i%2==0 else "1 100"))   # 每月都换收益最高，但交通费 100 抵掉
    out.append(mk(100,1,lambda i:"100 1" if i%2==0 else "1 100"))     # 每月都换最优
    out.append(mk(100,10,lambda i:("60 52" if i%2==0 else "52 60")))  # 差 8 < M，应留在一地
    out.append(mk(100,100,lambda i:"100 100"))
    out.append(mk(100,100,lambda i:"1 1"))
    out.append(mk(1,100,lambda i:"1 100"))
    out.append(mk(1,1,lambda i:"100 1"))
    out.append(mk(2,5,lambda i:("10 1" if i==0 else "1 10")))          # 换一次值得
    out.append(mk(2,50,lambda i:("10 1" if i==0 else "1 10")))         # 不换
    out.append(mk(100,30,lambda i:(f"{r.randint(70,100)} {r.randint(1,30)}" if (i//10)%2==0 else f"{r.randint(1,30)} {r.randint(70,100)}")))
    for _ in range(4):
        t=r.randint(10,16); m=r.randint(1,100)
        out.append(mk(t,m,lambda i:f"{r.randint(1,100)} {r.randint(1,100)}"))
    return out

def g19164(r):
    t=r.randint(1,20); return f"{t} {r.randint(1,30)}\n"+"\n".join(f"{r.randint(1,100)} {r.randint(1,100)}" for _ in range(t))+"\n"

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]+_big(19164)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
