import random,subprocess,tempfile
from pathlib import Path
# 参考解：按题意从大到小贪心，每个 N 用小根堆找当前负荷最小的集合，O(K^2 log K)。
# 原内嵌参考每步用 q.index(min(q)) 线性找最小，K=1000 时为 O(K^3)，满规模跑不动，故替换。
REFERENCE_SOURCE='''import sys,heapq
a=list(map(int,sys.stdin.read().split()))
k=a[0];v=sorted(a[1:1+k],reverse=True);M=v[0]
best=None
for n in range(1,k+1):
    h=[0]*n
    for y in v:
        heapq.heapreplace(h,h[0]+y)
    dev=sum(abs(s-M) for s in h)
    if best is None or dev<=best[0]:
        best=(dev,n)
print(best[1])
'''
SAMPLE_IN='8\n2  4  9\n12  16\n80  28\n72\n'


def valid(text):
    """题面：共 K+1 个整数，第一个是 K（K 不超过 1000），后面 K 个正整数。"""
    if not text.endswith("\n"):
        return False
    try:
        a=[int(x) for x in text.split()]
    except ValueError:
        return False
    if not a or not 1<=a[0]<=1000:
        return False
    if len(a)!=a[0]+1:
        return False
    return all(x>=1 for x in a[1:])


def layout(a,r):
    """把 K 个数排成不同的行布局（题面样例就是跨多行、双空格分隔）。"""
    mode=r.randrange(3)
    if mode==0:
        body=" ".join(map(str,a))+"\n"
    elif mode==1:
        body="".join(f"{x}\n" for x in a)
    else:
        rows=[];i=0
        while i<len(a):
            w=r.randint(1,8);rows.append("  ".join(map(str,a[i:i+w])));i+=w
        body="\n".join(rows)+"\n"
    return f"{len(a)}\n"+body


def g3725(index,r):
    if index==1: a=[r.randint(1,100)]                        # K=1
    elif index==2: a=[7,7]
    elif index==3: a=[1]*1000                                # 全相等，答案应为 K
    elif index==4: a=[100000]+[1]*999                        # 一个极大值
    elif index==5: a=[r.randint(1,100000) for _ in range(1000)]
    elif index==6: a=[r.randint(1,100) for _ in range(1000)]
    elif index==7: a=[r.randint(90000,100000) for _ in range(1000)]
    elif index==8: a=[r.choice([1,2,3,50000]) for _ in range(1000)]
    elif index==9: a=[r.randint(1,1000) for _ in range(r.randint(900,1000))]
    elif index==10: a=[r.randint(1,10) for _ in range(1000)]
    elif index<=20: a=[r.randint(1,100) for _ in range(r.randint(2,15))]
    elif index<=30: a=[r.randint(1,r.choice([5,100,10000])) for _ in range(r.randint(16,200))]
    else: a=[r.randint(1,r.choice([3,1000,100000])) for _ in range(r.randint(200,1000))]
    r.shuffle(a)
    return layout(a,r)


def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as h:
        h.write(REFERENCE_SOURCE);h.flush();root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for i in range(40):
            if i==0:c=SAMPLE_IN
            else:
                for j in range(100):
                    c=g3725(i,random.Random(3725+i+j*1000))
                    if c not in seen:break
                else:raise AssertionError("diversity")
                seen.append(c)
            assert valid(c),i
            p=subprocess.run(["python3",h.name],input=c,text=True,capture_output=True,check=True)
            (root/f"{i}.in").write_text(c,encoding="utf-8");(root/f"{i}.out").write_text(p.stdout,encoding="utf-8")


if __name__=="__main__":
    main()
