import random,subprocess,sys,tempfile
from pathlib import Path
# 参考解：按子集枚举可达值（加、减、乘、整除），独立于 samplecode 的「排列 + 相邻合并」写法。
# 原内嵌参考解用 ''.join(str) 去重排列，[1,12,11,2] 与 [11,2,1,12] 会被视为同一排列而跳过，换成这份。
REFERENCE='''import sys
def main():
    t=sys.stdin.read().split(); n=int(t[0]); a=list(map(int,t[1:1+n]))
    vals={}
    for m in range(1,1<<n):
        if m&(m-1)==0:
            vals[m]={a[m.bit_length()-1]}; continue
        s=set(); sub=(m-1)&m
        while sub:
            o=m^sub
            if sub<o:
                for x in vals[sub]:
                    for y in vals[o]:
                        s.add(x+y); s.add(x-y); s.add(y-x); s.add(x*y)
                        if y and x%y==0: s.add(x//y)
                        if x and y%x==0: s.add(y//x)
            sub=(sub-1)&m
        vals[m]=s
    print('YES' if 42 in vals[(1<<n)-1] else 'NO')
main()
'''
SAMPLE='6\n1 5 2 6 4 7\n'
GENERATOR_NAME='g10715'
def valid(text):
    # 题面：第一行 n，1<=n<=6；第二行 n 个 [1,13] 内的整数
    lines=text.split("\n")
    if lines[-1]!="": return False
    lines=lines[:-1]
    if len(lines)!=2: return False
    a=lines[0].split(); b=lines[1].split()
    if len(a)!=1 or not a[0].isdigit(): return False
    n=int(a[0])
    if not 1<=n<=6 or len(b)!=n: return False
    if not all(x.isdigit() and 1<=int(x)<=13 for x in b): return False
    return True
# 固定覆盖：n=1（必 NO）、n=2、各规模 NO、截断除法会误判 YES 的陷阱、必须用到除法/减法才能 YES 的组
FIXED=[
    [1],[7],[13],
    [6,7],[7,6],[3,13],[13,13],
    [13,13,4],[2,3,7],[1,1,1],[9,2,6],
    [10,7,7,12],[6,2,2,1],[10,13,8,2],[7,12,2,12],[6,3,10,11],
    [9,5,4,9,13],[12,13,13,6,12],[1,2,1,1,9],[9,9,9,8,13],[2,13,9,10,13],
    [1,1,1,1,1,1],[1,4,4,4,4,4],[12,12,12,12,12,13],[1,1,12,12,13,13],[8,8,8,8,9,9],
    [11,13,13,13,13,13],[5,5,5,5,5,5],[3,3,3,3,3,3],[13,13,13,13,13,13],[2,2,2,2,2,2],
]
def fmt(a): return f"{len(a)}\n"+" ".join(map(str,a))+"\n"
def g10715(r):
    n=r.randint(4,6); return fmt([r.randint(1,13) for _ in range(n)])

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[fmt(a) for a in FIXED]
    r=random.Random(10715)
    while len(cases)<40:
        t=g10715(r)
        if t not in cases: cases.append(t)
    assert all(valid(t) for t in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
