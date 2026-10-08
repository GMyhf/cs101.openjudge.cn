import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/19493 statistics, Accepted solution 43122575.\n# Source: http://cs101.openjudge.cn/practice/solution/43122575/\n# Statistics: http://cs101.openjudge.cn/practice/19493/statistics/\n# License: not declared on submission page; no license inferred\nm=int(input())\nfor _ in range(m):\n    l=list(map(float,input().split()))\n    t=str(l[0])\n    if t[-2]=='.':\n        flag=1\n    else:\n        flag=2\n    ans=[]\n    for i in range(len(l)-4):\n        c=sum(l[i:i+5])/5\n        ans.append(round(c,flag))\n    print(*ans)\n"
LANGUAGE='Python3'
SAMPLE='2\n1.0 2.0 3.0 4.0 5.0 6.0 7.0\n4.97 4.99 5.08 5.03 4.98 4.95 5.02\n'
GENERATOR_NAME='g19493'
# 题面只说「小数点后有一位或者两位」并按 round 保留位数，没说同一行精度混杂时保留几位；
# 参考解按 str(首个数) 决定位数。为避开歧义：每行统一精度（整行都写一位或整行都写两位），
# 两位小数行的首个数百分位非零（保证 str 后仍是两位）。统一精度下 5 项和除以 5 的结果
# 是保留单位的 0.2 倍数，永远不会落在 .5 舍入临界上，与求和方式无关。
NUM=re.compile(r"[0-9]+\.([0-9]{1,2})")
def valid(text):
    lines=text.split("\n")
    if lines[-1]!="": return False
    lines=lines[:-1]
    if not lines or not re.fullmatch(r"[1-9][0-9]*",lines[0]): return False
    m=int(lines[0])
    if len(lines)!=m+1: return False
    for ln in lines[1:]:
        toks=ln.split(" ")
        if len(toks)<5: return False
        digs=set()
        for t in toks:
            mt=NUM.fullmatch(t)
            if not mt or float(t)<=0: return False
            if len(t.split(".")[0])>1 and t[0]=="0": return False
            digs.add(len(mt.group(1)))
        if len(digs)!=1: return False
        if digs=={2} and toks[0][-1]=="0": return False
    return True

def row(r,n,prec,lo=1,hi=99999,kind="rand"):
    sc=10**prec
    vals=[]
    base=r.randint(lo,hi)
    for i in range(n):
        if kind=="rand": v=r.randint(lo,hi)
        elif kind=="walk":
            base=min(hi,max(lo,base+r.randint(-sc,sc))); v=base
        elif kind=="const": v=base
        elif kind=="inc": v=min(hi,lo+i)
        vals.append(v)
    if prec==2:
        while vals[0]%10==0: vals[0]=r.randint(lo,hi)
    return " ".join(f"{v//sc}.{v%sc:0{prec}d}" for v in vals)

def g19493(r,m=None,nlo=5,nhi=15,kind=None):
    if m is None: m=r.randint(1,8)
    out=[]
    for _ in range(m):
        prec=r.choice((1,2)); sc=10**prec
        k=kind or r.choice(("rand","walk","walk"))
        hi=r.choice((10*sc,100*sc,1000*sc))
        out.append(row(r,r.randint(nlo,nhi),prec,1,hi-1,k))
    return f"{m}\n"+"\n".join(out)+"\n"

def special(r):
    cs=[]
    cs.append("1\n1.0 2.0 3.0 4.0 5.0\n")                        # 恰 5 天，只出 1 个值
    cs.append("1\n0.01 0.01 0.01 0.01 0.01 0.02\n")               # 最小价格
    cs.append("2\n9999.9 9999.9 9999.9 9999.9 9999.9 9999.9\n9999.99 9999.98 9999.97 9999.96 9999.95\n")
    cs.append("3\n1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8\n1.11 1.12 1.13 1.14 1.15 1.16\n5.0 5.0 5.0 5.0 5.0\n")  # 平均为整数/一位小数时 round 后的输出形态
    cs.append("2\n4.01 4.99 5.00 5.00 5.00 5.01 4.99\n3.0 3.1 3.2 3.3 3.4\n")
    return cs

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
    cases=[SAMPLE]+special(random.Random(19493))
    seed=1
    while len(cases)<34:
        cases.append(g19493(random.Random(seed))); seed+=1
    R=random.Random(1949300)
    cases.append(g19493(R,m=1,nlo=5,nhi=5))
    cases.append(g19493(R,m=50,nlo=5,nhi=8))
    cases.append(g19493(R,m=1,nlo=20000,nhi=20000,kind="walk"))   # 单行长序列
    cases.append(g19493(R,m=100,nlo=300,nhi=600))
    cases.append(g19493(R,m=1000,nlo=60,nhi=100))                  # 满规模组 1
    cases.append(g19493(R,m=10,nlo=8000,nhi=10000))                # 满规模组 2
    assert len(cases)==40 and len(set(cases))==40
    for c in cases: assert valid(c), c[:80]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
