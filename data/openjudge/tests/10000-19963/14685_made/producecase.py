import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="k, n = map(int, input().split())\nmoney = []\nfor _ in range(n):\n    money.append(int(input()))\n\n# 使用集合加快查找速度\nmoney_set = set(money)\n# 使用集合去重\nfound = set()\nresult = []\n\nfor a in money:\n    b = k - a\n    if b in money_set:\n        # 确保不是同一个元素（当a=b时，需要有两个相同的数）\n        if a != b or money.count(a) > 1:\n            # 标准化组合：较小的在前\n            pair = (min(a, b), max(a, b))\n            if pair not in found:\n                found.add(pair)\n                result.append(pair)\n\n# 排序输出\nresult.sort(key=lambda x: x[0])\nif result:\n    for a, b in result:\n        print(f'{a} {b}')\nelse:\n    print('No Solution')"
SAMPLE='8 9\n-1\n6\n5\n3\n4\n2\n9\n0\n8\n'
GENERATOR_NAME='g14685'
def valid(text):
    # 题面：第 1 行 K N（2<=N<=50000，-1e9<=K<=1e9）；接下来 N 行每行一个钱数 A[i]（-1e9<=A[i]<=1e9）；
    # 描述明说“身上都带着各不相同的钱”，故 A[i] 两两不同。
    if not text.endswith("\n"): return False
    lines=text[:-1].split("\n")
    def isint(s): return re.fullmatch(r"-?(0|[1-9][0-9]*)",s) is not None and s!="-0"
    h=lines[0].split(" ")
    if len(h)!=2 or not all(isint(x) for x in h): return False
    k,n=map(int,h)
    if not (2<=n<=50000 and -10**9<=k<=10**9) or len(lines)!=n+1: return False
    if not all(isint(s) for s in lines[1:]): return False
    a=list(map(int,lines[1:]))
    if not all(-10**9<=x<=10**9 for x in a): return False
    return len(set(a))==n
def fmt(k,a): return f"{k} {len(a)}\n"+"\n".join(map(str,a))+"\n"
def g14685(r):
    # 小规模：钱数从 [-50,50] 中不放回抽取（保证互不相同）
    n=r.randint(2,30); k=r.randint(-50,50); z=r.sample(range(-50,51),n)
    return fmt(k,z)
M=10**9
def planted(r,n,k,pairs,lo=-M,hi=M):
    """n 个互异值，其中埋 pairs 对和为 k 的组合，其余随机（可能偶然再成对）。"""
    s=set(); a=[]
    while len(a)<2*pairs:
        x=r.randint(max(lo,k-hi),min(hi,k-lo))
        y=k-x
        if x!=y and x not in s and y not in s:
            s.add(x); s.add(y); a+=[x,y]
    while len(a)<n:
        x=r.randint(lo,hi)
        if x not in s: s.add(x); a.append(x)
    r.shuffle(a); return a
def designed():
    r=random.Random(14685)
    out=[]
    out.append(fmt(5,[2,3]))                                    # N=2 有解
    out.append(fmt(5,[2,4]))                                    # N=2 无解
    out.append(fmt(10,[5,0,7,3,-5,15]))                         # K/2=5 在场但只有一个，不能自配
    out.append(fmt(M,[M,0,-M,1,M-1]))                           # 值域边界
    out.append(fmt(-M,[-M,0,M,-1,1-M,5]))                       # K-A 超 int32（-1e9-1e9）
    out.append(fmt(0,[3,-3,-1,1,0,7,-7,2]))                     # K=0、负数在前
    out.append(fmt(-7,[-10,3,-4,-3,100,-107]))                  # 负 K
    n=50000
    out.append(fmt(49999,r.sample(range(50000),n)))             # 满规模、25000 对全部配上
    out.append(fmt(1,[2*x for x in r.sample(range(-M//2,M//2),n)]))   # 全偶数 + 奇 K：No Solution
    out.append(fmt(0,planted(r,n,0,20000)))
    out.append(fmt(123456789,planted(r,n,123456789,15000)))
    out.append(fmt(-M,planted(r,n,-M,10000)))
    out.append(fmt(M,planted(r,n,M,10000)))
    out.append(fmt(7,planted(r,n,7,1)))                          # 满规模只有一对
    out.append(fmt(1,r.sample([2*x for x in range(-30000,30000)],n-2)+[M-1,2-M]))   # 偶数里混入唯一一对奇数
    out.append(fmt(0,[x for x in range(-25000,25000)]))         # 有序输入、0 与自身不配
    return out
def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 25)]+designed()
    assert all(valid(t) for t in cases) and len(set(cases))==len(cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
