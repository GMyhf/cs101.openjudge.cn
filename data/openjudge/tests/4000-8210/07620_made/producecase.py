import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n=int(input())\nintervals=[]\nfor i in range(n):\n    intervals.append(tuple(int(i) for i in input().split()))\nintervals.sort()\ncleft=intervals[0][0]\ncright=intervals[0][1]\nfor left,right in intervals:\n    if left>cright:\n        print("no")\n        break\n    else:\n        cright=max(right,cright)\nelse:\n    print(cleft,cright)'
SAMPLE='5\n5 6\n1 5\n10 10\n6 9\n8 10\n'
GENERATOR_NAME='g7620'
def valid(text):
    """题面：第一行 n（3≤n≤50000）；随后 n 行「a b」单空格分隔，1≤a≤b≤10000。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines or not re.fullmatch(r"[1-9][0-9]*", lines[0]):
        return False
    n = int(lines[0])
    if not 3 <= n <= 50000 or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        m = re.fullmatch(r"([1-9][0-9]*) ([1-9][0-9]*)", line)
        if not m:
            return False
        a, b = int(m.group(1)), int(m.group(2))
        if not 1 <= a <= b <= 10000:
            return False
    return True


W=10000
def chain(r,n,lo,hi):
    # 生成 n 个能合并成 [lo,hi] 的区间：先铺一条首尾相接（共享端点）的链，再补随机子区间
    k=min(n,max(1,(hi-lo)//r.choice([1,2,5,50]) or 1))
    cuts=sorted(r.sample(range(lo+1,hi),min(k-1,hi-lo-1))) if hi-lo>1 else []
    pts=[lo]+cuts+[hi]
    iv=[(pts[i],pts[i+1]) for i in range(len(pts)-1)] or [(lo,hi)]
    while len(iv)<n:
        a=r.randint(lo,hi); b=r.randint(a,min(hi,a+r.choice([0,1,10,500])))
        iv.append((a,b))
    return iv[:n] if len(iv)>n else iv

def g7620(r,seed):
    if seed<=4: n=3
    elif seed<=24: n=r.randint(4,200)
    elif seed<=30: n=r.randint(1000,20000)
    else: n=50000                                   # 题面：3 ≤ n ≤ 50000
    mode=seed%6
    lo=r.choice([1,r.randint(1,5000)]); hi=r.choice([W,r.randint(lo,W)])
    if mode==0:          # 可合并，乱序给出
        iv=chain(r,n,lo,hi)
    elif mode==1:        # 只差一个整数（[x;y] 与 [y+1;z]）不能合并 → no
        g=r.randint(lo,max(lo,hi-1)) if hi>lo else lo
        if g>=W: g=W-1
        lo=min(lo,g); hi=max(hi,g+1)
        left=chain(r,max(1,n//2),lo,g); right=chain(r,n-len(left),g+1,hi)
        iv=left+right
    elif mode==2:        # 有一个大区间罩住后面的小区间（cright 必须取 max）
        iv=[(lo,hi)]+[(a,min(hi,a+r.randint(0,3))) for a in (r.randint(lo,hi) for _ in range(n-1))]
    elif mode==3:        # 中间有较大空隙 → no
        g1=r.randint(1,W-3); g2=r.randint(g1+2,min(W,g1+r.choice([2,50,3000])))
        left=chain(r,max(1,n//3),r.randint(1,g1),g1); right=chain(r,n-len(left),g2,r.randint(g2,W))
        iv=left+right
    elif mode==4:        # 点区间与相同区间大量重复
        a=r.randint(1,W-5); iv=[r.choice([(a,a),(a,a+1),(a+1,a+1),(a+1,a+3)]) for _ in range(n)]
        if r.random()<.5: iv.append((a+5,a+5)); iv=iv[1:]
    else:                # 完全随机
        iv=[]
        for _ in range(n):
            a=r.randint(1,W); iv.append((a,min(W,a+r.randint(0,r.choice([0,5,100,3000])))))
    r.shuffle(iv)
    return f"{len(iv)}\n"+"\n".join(f"{a} {b}" for a,b in iv)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g7620(random.Random(seed),seed) for seed in range(1, 40)]
    assert all(valid(t) for t in cases), "有数据越出题面约束"
    assert len(set(cases))==len(cases), "有重复数据"
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
