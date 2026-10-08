import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# 本题参考解（替换原外部 AC 提交）：对两块相对第一块的位移做 BFS。\n# 原提交用定长 20 的列表存冲突矩阵，相对位移为负且较大时下标回绕，会给出偏大的步数。\nimport sys\nfrom collections import deque\nL=20  # 相对位移上界：三块都在 10×10 内，分离所需位移远小于 20\ndef solve(B):\n    bb=[(min(x for x,_ in b),max(x for x,_ in b),min(y for _,y in b),max(y for _,y in b)) for b in B]\n    S=[set(b) for b in B]\n    memo={}\n    def hit(i,j,dx,dy):  # block j shifted by (dx,dy) relative to block i overlaps?\n        k=(i,j,dx,dy)\n        if k not in memo:\n            memo[k]=any((x+dx,y+dy) in S[i] for x,y in B[j])\n        return memo[k]\n    def sep(i,j,dx,dy):\n        a=bb[i]; b=bb[j]\n        return a[1]<b[0]+dx or b[1]+dx<a[0] or a[3]<b[2]+dy or b[3]+dy<a[2]\n    def ok(s):\n        a,b,c,d=s\n        return not hit(0,1,a,b) and not hit(0,2,c,d) and not hit(1,2,c-a,d-b)\n    def goal(s):\n        a,b,c,d=s\n        return sep(0,1,a,b) and sep(0,2,c,d) and sep(1,2,c-a,d-b)\n    st=(0,0,0,0)\n    if goal(st): return 0\n    dist={st:0}; q=deque([st])\n    D=((1,0),(-1,0),(0,1),(0,-1))\n    while q:\n        s=q.popleft(); a,b,c,d=s\n        for dx,dy in D:\n            for t in ((a+dx,b+dy,c,d),(a,b,c+dx,d+dy),(a-dx,b-dy,c-dx,d-dy)):\n                if t in dist or max(map(abs,t))>L: continue\n                if not ok(t): continue\n                dist[t]=dist[s]+1\n                if goal(t): return dist[t]\n                q.append(t)\n    return -1\ntok=sys.stdin.read().split(); p=0; out=[]\nwhile True:\n    n=[int(tok[p]),int(tok[p+1]),int(tok[p+2])]; p+=3\n    if n==[0,0,0]: break\n    B=[]\n    for k in n:\n        B.append([(int(tok[p+2*i]),int(tok[p+2*i+1])) for i in range(k)]); p+=2*k\n    out.append(solve(B))\nprint("\\n".join(map(str,out)))\n'
LANGUAGE='Python3'
SAMPLE='3 12 5\n2 1\n2 2\n1 2\n0 0\n0 1\n0 2\n0 3\n0 4\n1 0\n1 4\n2 0\n2 4\n3 0\n3 1\n3 4\n2 3\n3 3\n4 3\n4 4\n4 2\n1 1 1\n0 0\n1 1\n2 2\n0 0 0\n'
GENERATOR_NAME='g15291'
def valid(text):
    """题面：多组数据（不多于 12 组），以 "0 0 0" 结束。每组首行三个正整数 n1 n2 n3，
    随后 n1+n2+n3 行，每行一对 0 到 9 之间的整数（单位正方形左下角坐标）。
    三个固体块各自连通（题面「三个连通的……固体块」）；同一块内格子互异；
    块与块之间不重合（题面：平移过程中不能使任何两个固体块有重合的部分，初始状态自然也不重合）。"""
    if not text.endswith("\n"): return False
    lines=text[:-1].split("\n"); p=0; groups=0
    def ints(s,k):
        t=s.split()
        if len(t)!=k or s!=" ".join(t): raise ValueError
        return list(map(int,t))
    try:
        while True:
            n=ints(lines[p],3); p+=1
            if n==[0,0,0]: break
            if min(n)<1: return False
            groups+=1
            if groups>12: return False
            seen=set()
            for k in n:
                blk=[tuple(ints(lines[p+i],2)) for i in range(k)]; p+=k
                if any(not(0<=x<=9 and 0<=y<=9) for x,y in blk): return False
                s=set(blk)
                if len(s)!=k or s&seen: return False
                seen|=s
                st=[blk[0]]; vis={blk[0]}
                while st:
                    x,y=st.pop()
                    for c in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                        if c in s and c not in vis: vis.add(c); st.append(c)
                if len(vis)!=k: return False
    except (ValueError,IndexError):
        return False
    return p==len(lines) and groups>=1

def grow(r,total,box=10):
    """三个种子同时在 box×box 棋盘内随机长大，得到互不重叠的连通块。"""
    while True:
        cells=r.sample([(x,y) for x in range(box) for y in range(box)],3)
        owner={c:i for i,c in enumerate(cells)}; B=[[c] for c in cells]
        target=[1,1,1]
        for _ in range(total-3): target[r.randrange(3)]+=1
        stuck=0
        while any(len(B[i])<target[i] for i in range(3)) and stuck<2000:
            i=r.randrange(3)
            if len(B[i])>=target[i]: continue
            x,y=r.choice(B[i]); dx,dy=r.choice(((1,0),(-1,0),(0,1),(0,-1)))
            c=(x+dx,y+dy)
            if 0<=c[0]<box and 0<=c[1]<box and c not in owner:
                owner[c]=i; B[i].append(c); stuck=0
            else: stuck+=1
        if all(len(B[i])==target[i] for i in range(3)): return B
def ring(r):
    """一个（可能留缺口的）方框把另一块围在里面，第三块在外面。"""
    x0,y0=r.randint(0,3),r.randint(0,3); w,h=r.randint(3,9-x0),r.randint(3,9-y0)
    fr=[(x,y) for x in range(x0,x0+w+1) for y in range(y0,y0+h+1) if x in (x0,x0+w) or y in (y0,y0+h)]
    gap=r.random()<0.5
    if gap:
        side=[c for c in fr if c not in ((x0,y0),(x0+w,y0),(x0,y0+h),(x0+w,y0+h))]
        fr.remove(r.choice(side))
        # 去掉一格后仍需连通：方框去掉非角上的一格仍是连通的
    inner=[(x,y) for x in range(x0+1,x0+w) for y in range(y0+1,y0+h)]
    k=r.randint(1,len(inner)); 
    # 内部块：从一个格子长出的连通块
    s=[r.choice(inner)]; ss=set(s)
    while len(s)<k:
        x,y=r.choice(s); dx,dy=r.choice(((1,0),(-1,0),(0,1),(0,-1))); c=(x+dx,y+dy)
        if c in inner and c not in ss: s.append(c); ss.add(c)
    used=set(fr)|ss
    free=[(x,y) for x in range(10) for y in range(10) if (x,y) not in used]
    t=[r.choice(free)]
    B=[fr,s,t]; r.shuffle(B); return B
def fmt(B):
    out=[f"{len(B[0])} {len(B[1])} {len(B[2])}"]
    for b in B:
        for x,y in b: out.append(f"{x} {y}")
    return out
def g15291(r,kind):
    groups=r.randint(1,12) if kind!="full" else 12
    lines=[]
    for _ in range(groups):
        t=r.random()
        if t<0.2: B=ring(r)
        elif t<0.45: B=grow(r,r.randint(3,12))
        elif t<0.75: B=grow(r,r.randint(12,40))
        else: B=grow(r,r.randint(40,100))
        for b in B: r.shuffle(b)
        lines+=fmt(B)
    return "\n".join(lines)+"\n0 0 0\n"

FIXED=["1 1 1\n0 0\n1 1\n2 2\n0 0 0\n"]

def build_cases():
    cases=[SAMPLE]+list(FIXED)
    for seed in range(1,39):
        for attempt in range(100):
            t=g15291(random.Random(seed*1000+attempt),"full" if seed%5==0 else "mixed")
            if t not in cases: cases.append(t); break
        else: raise AssertionError("生成器多样性不足")
    return cases

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
    cases=build_cases()
    assert len(cases)==40 and all(valid(t) for t in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
