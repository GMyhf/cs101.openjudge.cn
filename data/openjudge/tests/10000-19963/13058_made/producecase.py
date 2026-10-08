import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='N = int(input())\nheights = []\nfor _ in range(N):\n    heights.append(int(input()))\nstack = []\nans = 0\nfor i in range(N):\n    h = heights[i]\n    while stack and stack[-1][0] <= h:\n        stack.pop()\n    ans += len(stack)\n    stack.append((h, i))\nprint(ans)'
SAMPLE='6\n10\n3\n7\n4\n12\n2\n'
GENERATOR_NAME='g13058'
def g13058(r):
    n=r.randint(1,50); return f"{n}\n"+"\n".join(str(r.randint(1,100000)) for _ in range(n))+"\n"

def valid(text):
    # 题面：第 1 行 N (1<=N<=80000)；接下来 N 行每行一个整数 hi (1<=hi<=1e9)
    if not text.endswith("\n"): return False
    lines=text[:-1].split("\n")
    if not lines[0].isdigit(): return False
    n=int(lines[0])
    if not 1<=n<=80000 or len(lines)!=n+1: return False
    for s in lines[1:]:
        if not s.isdigit() or s[0]=="0" or not 1<=int(s)<=10**9: return False
    return True
NMAX=80000; HMAX=10**9
def fmt(h): return f"{len(h)}\n"+"\n".join(map(str,h))+"\n"
def designed():
    r=random.Random(13058)
    out=[]
    out.append([7])                                              # N=1
    out.append([5,5])                                            # 等高挡住
    out.append([HMAX,1])                                         # 值域上下界
    out.append([1,HMAX])
    out.append([HMAX]*NMAX)                                      # 全等高：答案 0
    out.append(list(range(HMAX,HMAX-NMAX,-1)))                   # 严格递减：答案 N(N-1)/2 > 2^31，卡 int 溢出、卡 O(N^2)
    out.append(list(range(1,NMAX+1)))                            # 严格递增：答案 0
    out.append([r.randint(1,HMAX) for _ in range(NMAX)])         # 满规模随机
    out.append([r.randint(1,HMAX) for _ in range(NMAX)])
    out.append([r.randint(1,10) for _ in range(NMAX)])           # 大量相等身高
    out.append(sorted((r.randint(1,1000) for _ in range(NMAX)),reverse=True))  # 非严格递减：等高处必须挡住
    out.append([HMAX-i//2 for i in range(NMAX)])                 # 成对等高的递减
    out.append([HMAX if i%2==0 else 1 for i in range(NMAX)])     # 锯齿
    out.append([NMAX-i if i<NMAX//2 else i for i in range(NMAX)])# 先降后升（V 形）
    out.append([i if i<NMAX//2 else NMAX-i+1 for i in range(1,NMAX+1)])  # 先升后降（山形）
    out.append([r.randint(1,HMAX) for _ in range(r.randint(1000,5000))])
    out.append(sorted((r.randint(1,HMAX) for _ in range(NMAX)),reverse=True))
    out.append([r.randint(HMAX-5,HMAX) for _ in range(NMAX)])
    out.append([1]*(NMAX-1)+[2])
    out.append([2]+[1]*(NMAX-1))                                 # 第一头能看到其余全部
    return [fmt(h) for h in out]
def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    # 第 1..19 组沿用原小规模随机（种子 1..19），第 20 组起为满规模/边界构造
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 20)]+designed()
    assert all(valid(t) for t in cases) and len(set(cases))==len(cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
