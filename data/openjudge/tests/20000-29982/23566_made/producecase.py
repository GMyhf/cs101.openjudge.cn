import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23566/\n# Accepted submission: 52178654\n# Source: http://cs101.openjudge.cn/practice/solution/52178654/\n# License: not declared on the submission page; no license is inferred.\n\nn,m=map(int,input().split())\nlis=[0 for i in range(m)]\ntotal=0\nfor i in range(n):\n    x,y=map(int,input().split())\n    lis[x-1]+=y\ntotal=sum(lis)\ntotal-=(total//200)*30\nfor i in range(m):\n    s=input()\n    ptr=0\n    while "0"<=s[ptr]<="9":\n        ptr+=1\n    if lis[i]>=int(s[0:ptr]):\n        total-=int(s[ptr+1:len(s)])\nprint(total)'
SAMPLE='2 2\n1 100\n2 100\n100-20\n200-50\n'
GENERATOR_NAME='g23566'
def g23566(r):
    n,m=r.randint(2,20),r.randint(2,8); items=[(r.randint(1,m),r.randint(1,300)) for _ in range(n)]
    coupons=[(q,r.randint(1,q)) for q in [r.randint(1,1000) for _ in range(m)]]
    return f"{n} {m}\n"+"\n".join(f"{a} {b}" for a,b in items)+"\n"+"\n".join(f"{a}-{b}" for a,b in coupons)+"\n"

def valid(text):
    """题面契约：首行 n m（1<n<10000，1<m<100）；接着 n 行 "si pi"（1<=si<=m，pi 为整数）；
    最后 m 行 "qj-xj"（qj>=xj）。题面没给 pi、qj、xj 的上限，这里只要求非负整数。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    h = lines[0].split(" ")
    if len(h) != 2 or not all(t.isdigit() for t in h):
        return False
    n, m = map(int, h)
    if not (1 < n < 10000 and 1 < m < 100) or len(lines) != 1 + n + m:
        return False
    for line in lines[1:1 + n]:
        t = line.split(" ")
        if len(t) != 2 or not all(x.isdigit() for x in t) or not 1 <= int(t[0]) <= m:
            return False
    for line in lines[1 + n:]:
        t = line.split("-")
        if len(t) != 2 or not all(x.isdigit() for x in t) or int(t[0]) < int(t[1]):
            return False
    return True


# 2026-10 补强：原 39 组 n<=20、m<=8，离上限 n=9999、m=99 很远；店铺金额恰好等于门槛 q、
# 总价恰好是 200 的整数倍这两个 >= 边界也只靠随机碰运气。末 8 组换成下面这些。
EXTRA_KINDS = ["max", "max", "eq", "eq", "mult200", "below200", "nocoupon", "allcoupon"]


def g23566_extra(r, kind):
    if kind == "max":
        n, m = 9999, 99
    elif kind in ("eq", "mult200", "allcoupon"):
        n, m = r.randint(30, 300), r.randint(10, 60)
    else:
        n, m = r.randint(2, 6), r.randint(2, 5)
    items = [(r.randint(1, m), r.randint(1, 300 if kind != "below200" else 30)) for _ in range(n)]
    if kind == "below200":
        items = [(r.randint(1, m), r.randint(1, 199 // n)) for _ in range(n)]
    if kind == "mult200":        # 把最后一件商品的价格调到总价恰为 200 的倍数
        rest = sum(p for _, p in items[:-1])
        need = (-rest) % 200 or 200
        items[-1] = (items[-1][0], need)
    store = [0] * (m + 1)
    for a, b in items:
        store[a] += b
    coupons = []
    for j in range(1, m + 1):
        if kind in ("eq", "allcoupon", "max") and store[j] and (kind != "max" or j % 3):
            q = store[j] if kind != "allcoupon" else r.randint(1, store[j])     # 恰好等于门槛
        elif kind == "nocoupon":
            q = store[j] + 1                                                       # 差 1 用不了
        else:
            q = r.randint(1, 1000)
        coupons.append((q, r.randint(1, q)))
    return f"{n} {m}\n"+"\n".join(f"{a} {b}" for a,b in items)+"\n"+"\n".join(f"{a}-{b}" for a,b in coupons)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40-len(EXTRA_KINDS))]
    cases+=[g23566_extra(random.Random(23566*7+k), kind) for k, kind in enumerate(EXTRA_KINDS)]
    assert len(cases)==40 and len(set(cases))==40 and all(valid(c) for c in cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
