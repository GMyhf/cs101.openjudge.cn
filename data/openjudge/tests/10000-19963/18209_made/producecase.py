import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/18209 statistics, Accepted solution 38077709.\n# Source: http://cs101.openjudge.cn/practice/solution/38077709/\n# Statistics: http://cs101.openjudge.cn/practice/18209/statistics/\n# License: not declared on submission page; no license inferred\nfrom math import log\nn = int(input())\na, b = 0, 0\nlst = list(map(float, input().split()))\nlst.sort()\nfor i in range(n):\n    a -= log(lst[i], 2) * lst[i]\n    if i != 0 and i != n - 1:\n        b -= log(lst[i], 2) * lst[i]\nprint('%.3f' % a)\nprint('%.3f' % b)\n"
LANGUAGE='Python3'
SAMPLE='3\n0.2 0.7 0.1\n'
GENERATOR_NAME='g18209'
import math
from decimal import Decimal, InvalidOperation
def valid(text):
    """题面：第一行整数 n（3≤n）；第二行 n 个 0 到 1 之间的浮点数，和为 1。"""
    lines=text.split("\n")
    if len(lines)!=3 or lines[2]!="": return False
    if not lines[0].isdigit(): return False
    n=int(lines[0])
    if n<3: return False
    toks=lines[1].split(" ")
    if len(toks)!=n: return False
    tot=Decimal(0)
    for t in toks:
        try: v=Decimal(t)
        except InvalidOperation: return False
        if not v.is_finite() or v<0 or v>1: return False
        tot+=v
    return tot==1

def _near_half(x):
    y=x*1000; f=y-math.floor(y)
    return abs(f-0.5)<1e-6

def _make(r,n,digits):
    """构造 n 个正概率（以 10^digits 为分母，和恰为 1），最小值与最大值各唯一，
    避免题面「去掉最大和最小的概率」在并列时产生歧义；并避开三位小数舍入临界。"""
    D=10**digits
    while True:
        K=max(3,D//(2*(n-2)))
        lo=r.randint(1,max(1,K//3))
        mids=[r.randint(lo+1,K) for _ in range(n-2)]
        hi=D-lo-sum(mids)
        if hi<=max(mids): continue
        w=[lo]+mids+[hi]; r.shuffle(w)
        ps=[x/D for x in w]
        a=-math.fsum(x*math.log2(x) for x in ps)
        b=-math.fsum(x*math.log2(x) for x in sorted(ps)[1:-1])
        if _near_half(a) or _near_half(b): continue
        return f"{n}\n"+" ".join(f"{x:.{digits}f}" for x in ps)+"\n"

def g18209(r):
    k=r.random()
    if k<0.6: n=r.randint(3,10)
    elif k<0.85: n=r.randint(11,200)
    else: n=r.randint(201,2000)
    return _make(r,n,6 if n<=200 else 8)

# 题面样例 2、n=3 最小规模、大规模
EXTRA=['6\n0.04 0.06 0.1 0.5 0.07 0.23\n']+[_make(random.Random(1000+i),n,d) for i,(n,d) in enumerate(((3,2),(3,6),(4,6),(10000,8),(50000,9)))]

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]+EXTRA
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
