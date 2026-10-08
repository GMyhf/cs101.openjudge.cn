import random,subprocess,sys,tempfile
from pathlib import Path
def valid(text):
    """题面契约：第 1 行 N L（1<=N<=1000，1<=L<=1000000，L 为偶数）；第 2 行 A B（1<=A<=B<=1000）；
    随后恰 N 行，每行 S E（0<=S<E<=L）。"""
    try:
        if not text.endswith("\n"):return False
        lines=text[:-1].split("\n")
        def ints(ln):
            t=ln.split(" ")
            if len(t)!=2 or not all(x.isdigit() for x in t):raise ValueError
            return int(t[0]),int(t[1])
        n,L=ints(lines[0]);a,b=ints(lines[1])
        if not (1<=n<=1000 and 1<=L<=1000000 and L%2==0 and 1<=a<=b<=1000):return False
        if len(lines)!=n+2:return False
        for ln in lines[2:]:
            s_,e=ints(ln)
            if not 0<=s_<e<=L:return False
        return True
    except Exception:
        return False

def gen2373(r,seed):
    def fmt(L,a,b,cows):
        r.shuffle(cows);return f"{len(cows)} {L}\n{a} {b}\n"+"\n".join(f"{x} {y}" for x,y in cows)+"\n"
    def planned(L,a,b,n,maxlen=None):
        # 先切出一组合法喷头，再在各段内部放牛区间，保证有解
        half=L//2;segs=[];pos=0
        feas=lambda m:m==0 or (m+b-1)//b<=m//a
        assert feas(half)
        while pos<half:
            rem=half-pos
            while True:
                rd=r.randint(a,min(b,rem))
                if feas(rem-rd):break
            segs.append((2*pos,2*(pos+rd)));pos+=rd
        cows=[]
        for _ in range(n):
            x,y=r.choice(segs);
            if maxlen:y=min(y,x+maxlen)
            s_,e=sorted(r.sample(range(x,y+1),2));cows.append((s_,e))
        return cows
    def rnd(L,n,maxlen):
        cows=[]
        for _ in range(n):
            ln=r.randint(1,min(maxlen,L));s_=r.randint(0,L-ln);cows.append((s_,s_+ln))
        return cows
    M=1000000
    if seed==1:return fmt(2,1,1,[(0,2)])                     # 最小规模，答案 1
    if seed==2:return fmt(2,2,5,[(0,1)])                     # 2A>L，-1
    if seed==3:return fmt(2000,1000,1000,[(0,2000)])         # 一个喷头恰好覆盖全程
    if seed==4:return fmt(2002,1000,1000,[(0,1)])            # L 不是 2A..2B 的和，-1
    if seed==5:return fmt(M,1000,1000,planned(M,1000,1000,1000))   # 唯一划分，答案 500
    if seed==6:return fmt(M,1,1,planned(M,1,1,1000))         # 半径固定为 1，答案 500000
    if seed==7:return fmt(M,1,1000,planned(M,1,1000,1000))
    if seed==8:return fmt(M,1,1000,planned(M,1,1000,1000,50))
    if seed==9:return fmt(M,500,1000,planned(M,500,1000,1000))
    if seed==10:return fmt(M,999,1000,planned(M,999,1000,1000))
    if seed==11:return fmt(M,1,2,planned(M,1,2,1000))
    if seed==12:return fmt(M,1,1000,rnd(M,1000,3000))        # 随机牛区间，可能 -1
    if seed==13:return fmt(M,1,1000,rnd(M,1000,30))
    if seed==14:return fmt(M,1,1000,[(0,M)]*1000)            # 整段被一头牛要求，-1
    if seed==15:return fmt(M,1,1000,planned(M,1,1000,999)+[(1000,3001)])  # 一个超长区间，-1
    if seed==16:return fmt(M,7,13,planned(M,7,13,1000))
    if seed==17:return fmt(M,1,1000,rnd(M,1000,2000))
    if seed==18:return fmt(M-2,333,777,planned(M-2,333,777,1000))
    if seed<=30:
        L=2*r.randint(1,40);a=r.randint(1,max(1,L//4));b=r.randint(a,min(1000,a+r.randint(0,8)))
        n=r.randint(1,8)
        return fmt(L,a,b,planned(L,a,b,n) if seed%2 and (L//2+b-1)//b<=L//2//a else rnd(L,n,r.randint(1,L)))
    L=2*r.randint(500,50000);a=r.randint(1,100);b=r.randint(a,a+r.randint(0,900))
    if seed%2:return fmt(L,a,b,rnd(L,r.randint(1,1000),r.randint(1,3*b)))
    if (L//2+b-1)//b>L//2//a:a=1
    return fmt(L,a,b,planned(L,a,b,r.randint(1,1000)))


def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    letters = "abcdefghijklmnopqrstuvwxyz"
    word = lambda a=2,b=8: "".join(r.choice(letters) for _ in range(r.randint(a,b)))
    if number==2184:
        a=[(r.randint(-20,30),r.randint(-20,30)) for _ in range(r.randint(2,14))];return f"{len(a)}\n"+"\n".join(f"{x} {y}" for x,y in a)+"\n"
    if number==2313:
        a=[r.randint(-10000,10000) for _ in range(r.randint(1,40))];return f"{len(a)}\n"+"\n".join(map(str,a))+"\n"
    if number==2755:
        a=[r.randint(1,40) for _ in range(r.randint(1,18))];return f"{len(a)}\n"+"\n".join(map(str,a))+"\n"
    if number==1837:
        c=r.randint(2,8);g=r.randint(2,8);p=sorted(r.sample(range(-15,16),c));w=sorted(r.sample(range(1,26),g));return f"{c} {g}\n"+" ".join(map(str,p))+"\n"+" ".join(map(str,w))+"\n"
    if number==2373:return gen2373(r,seed)
    if number==1204:
        h,w=8+r.randrange(5),8+r.randrange(5);grid=[[r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(w)] for _ in range(h)];words=[]
        for y in range(min(6,h)):
            x=r.randrange(0,w-3);s="".join(grid[y][x:x+4]);words.append(s)
        return f"{h} {w} {len(words)}\n"+"\n".join("".join(x) for x in grid)+"\n"+"\n".join(words)+"\n"
    if number==2992:
        n=r.randint(2,16);a=[[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i):a[i][j],a[j][i]=(3,r.randrange(3)) if r.randrange(2) else (r.randrange(3),3)
        return f"{n}\n"+"\n".join(" ".join(map(str,row)) for row in a)+"\n"
    if number==1084:
        rows=[]
        for _ in range(r.randint(1,3)):
            n=r.randint(1,3);total=2*n*(n+1);gone=sorted(r.sample(range(1,total+1),r.randint(0,min(total,5))));rows.append(f"{n}\n{len(gone)}"+(" "+" ".join(map(str,gone)) if gone else ""))
        return f"{len(rows)}\n"+"\n".join(rows)+"\n"
    if number==1251:
        n=r.randint(2,12);rows=[]
        for i in range(n-1):
            edges=[(j,r.randint(1,100)) for j in range(i+1,n) if j==i+1 or r.random()<.25];rows.append(chr(65+i)+f" {len(edges)} "+" ".join(f"{chr(65+j)} {c}" for j,c in edges))
        return f"{n}\n"+"\n".join(x.rstrip() for x in rows)+"\n0\n"
    if number==1390:
        cases=[]
        for _ in range(r.randint(1,3)):
            n=r.randint(1,20);cases.append(f"{n}\n"+" ".join(str(r.randint(1,n)) for _ in range(n)))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number==2191:return f"{r.randint(2,63)}\n"
    if number==2503:
        foreign=[word() for _ in range(5)];rows=[f"{word()} {x}" for x in foreign];queries=foreign[:3]+[word()];return "\n".join(rows)+"\n\n"+"\n".join(queries)+"\n"
    if number==2724:
        n=r.randint(3,20);rows=[f"s{seed}_{i} {r.randint(1,12)} {r.randint(1,28)}" for i in range(n)];return f"{n}\n"+"\n".join(rows)+"\n"
    if number==1273:
        n=r.randint(2,10);edges=[(i,i+1,r.randint(1,1000)) for i in range(1,n)];edges += [(r.randint(1,n-1),r.randint(2,n),r.randint(0,1000)) for _ in range(r.randint(0,8))];return f"{len(edges)} {n}\n"+"\n".join(f"{a} {b} {c}" for a,b,c in edges)+"\n"
    if number==1835:
        cases=[];cmds="forward back left right up down".split()
        for _ in range(r.randint(1,4)):
            a=[f"{r.choice(cmds)} {r.randint(1,10000)}" for _ in range(r.randint(1,20))];cases.append(f"{len(a)}\n"+"\n".join(a))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number==1905:
        rows=[f"{r.randint(1,10000)} {r.random()*20:.3f} {r.random()/10000:.7f}" for _ in range(r.randint(1,6))];return "\n".join(rows)+"\n-1 -1 -1\n"
    if number==1922:
        n=r.randint(1,15);rows=[(r.randint(1,40),r.randint(-200,500)) for _ in range(n)];rows[0]=(rows[0][0],r.randint(0,500));return f"{n}\n"+"\n".join(f"{a} {b}" for a,b in rows)+"\n0\n"
    if number==1936:return "\n".join(f"{word()} {word(5,18)}" for _ in range(r.randint(1,8)))+"\n"
    if number==2538:
        chars="1234567890-=WERTYUIOP[]\\SDFGHJKL;'XCVBNM,./ ";return "\n".join("".join(r.choice(chars) for _ in range(r.randint(1,60))) for _ in range(r.randint(1,6)))+"\n"
    if number==2982:
        base="534678912 672195348 198342567 859761423 426853791 713924856 961537284 287419635 345286179".split();shift=seed%9;grid=[row[shift:]+row[:shift] for row in base];
        for _ in range(12+seed%20):
            y,x=r.randrange(9),r.randrange(9);grid[y]=grid[y][:x]+"0"+grid[y][x+1:]
        return "1\n"+"\n".join(grid)+"\n"
    if number in NO_INPUT:return ""
    if number==1006:return "\n".join(" ".join(str(r.randint(0,365)) for _ in range(4)) for _ in range(r.randint(1,5)))+"\n-1 -1 -1 -1\n"
    if number==2159:
        n=r.randint(2,100);a="".join(r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(n));b="".join(r.sample(list(a),len(a))) if seed%2 else a[:-1]+("A" if a[-1]!="A" else "B");return a+"\n"+b+"\n"
    if number==1113:
        w,h=r.randint(2,200),r.randint(2,200);x,y=r.randint(-100,100),r.randint(-100,100);return f"4 {r.randint(1,100)}\n{x} {y}\n{x} {y+h}\n{x+w} {y+h}\n{x+w} {y}\n"
    if number==2381:
        m=r.randint(2,20000);a=r.randint(0,min(10000,(2**32-2)//m));c=r.randint(0,10000);return f"{a} {c} {m} {r.randrange(m)}\n"
    if number==2186:
        n=r.randint(2,20);edges={(i,i+1) for i in range(1,n)}|{(n,1)}
        for _ in range(r.randint(0,30)):edges.add((r.randint(1,n),r.randint(1,n)))
        return f"{n} {len(edges)}\n"+"\n".join(f"{a} {b}" for a,b in sorted(edges))+"\n"
    if number==1236:
        n=r.randint(2,18);rows=[]
        for i in range(1,n+1):
            a=sorted({j for j in range(1,n+1) if j!=i and r.random()<.2});rows.append((" ".join(map(str,a))+" " if a else "")+"0")
        return f"{n}\n"+"\n".join(rows)+"\n"
    if number==1062:
        n=r.randint(1,12);rows=[f"{r.randint(1,10000)} {r.randint(1,20)} 0" for _ in range(n)];return f"{r.randint(1,10)} {n}\n"+"\n".join(rows)+"\n"
    if number==1067:return "\n".join(f"{r.randint(0,10**9)} {r.randint(0,10**9)}" for _ in range(r.randint(1,10)))+"\n"
    if number==1091:return f"{r.randint(1,15)} {r.randint(1,100000000)}\n"
    if number==1154:
        h,w=r.randint(1,7),r.randint(1,7);return f"{h} {w}\n"+"\n".join("".join(r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(w)) for _ in range(h))+"\n"
    if number==1183:return f"{r.randint(1,60000)}\n"
    if number==1184:return f"{r.randint(0,999999):06d} {r.randint(0,999999):06d}\n"
    if number==2001:
        a={word(2,15) for _ in range(12)}
        while len(a)<8:a.add(word(2,15))
        return "\n".join(sorted(a))+"\n"
    if number==2141:
        key=list(letters);r.shuffle(key);msg="".join(r.choice(letters+letters.upper()+" ") for _ in range(r.randint(1,80)));return "".join(key)+"\n"+msg+"\n"
    if number==1164:
        h,w=1+(seed-1)%8,2+(seed-1)//8;return f"{h}\n{w}\n"+"\n".join(" ".join(["15"]*w) for _ in range(h))+"\n"
    if number==1166:return "\n".join(" ".join(str(r.randrange(4)) for _ in range(3)) for _ in range(3))+"\n"
    if number==1193:
        N=r.randint(5,100);rows=[];t=0
        for _ in range(r.randint(2,20)):t+=r.randint(0,4);rows.append(f"{t} {r.randint(1,N)} {r.randint(1,30)}")
        return f"{N}\n"+"\n".join(rows)+"\n0 0 0\n"
    if number==2002:
        pts=set()
        while len(pts)<r.randint(2,30):pts.add((r.randint(-30,30),r.randint(-30,30)))
        if seed%2:pts.update({(0,0),(0,seed),(seed,0),(seed,seed)})
        return f"{len(pts)}\n"+"\n".join(f"{x} {y}" for x,y in sorted(pts))+"\n0\n"
    if number==2000:return "\n".join(str(r.randint(1,10000)) for _ in range(r.randint(1,10)))+"\n0\n"
    if number==1324:
        L=2+(seed-1)%6;n,m=10,12;row=2+(seed-1)%5;col=2+(seed-1)//5;body=[(row,col+i) for i in range(L)];return f"{n} {m} {L}\n"+"\n".join(f"{a} {b}" for a,b in body)+"\n0\n\n0 0 0\n"
    if number==2318:
        n=r.randint(1,8);m=r.randint(1,15);xs=sorted(r.sample(range(5,95),n));toys=[(r.randint(1,99),r.randint(1,9)) for _ in range(m)];return f"{n} {m} 0 10 100 0\n"+"\n".join(f"{x} {x}" for x in xs)+"\n"+"\n".join(f"{x} {y}" for x,y in toys)+"\n0\n"
    if number==3129:
        cases=[f"{r.randint(1,10000)}\n"+" ".join(str(r.randint(1,10000)) for _ in range(5)) for _ in range(r.randint(1,4))];return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number==1001:return "\n".join(f"{r.randint(1,999999)/10000:.4f} {r.randint(1,25)}" for _ in range(r.randint(1,6)))+"\n"
    if number==1004:return "\n".join(f"{r.randint(1,100000000)/100:.2f}" for _ in range(12))+"\n"
    if number==1005:
        rows=[]
        for _ in range(r.randint(1,8)):
            x,y=r.uniform(-100,100),r.uniform(0,100);rows.append(f"{x:.3f} {y:.3f}")
        return f"{len(rows)}\n"+"\n".join(rows)+"\n"
    if number==1021:
        cases=[]
        for _ in range(r.randint(1,3)):
            w=h=r.randint(4,12);n=r.randint(1,min(12,w*h));p=r.sample([(x,y) for x in range(w) for y in range(h)],n);q=p[:] if r.random()<.5 else r.sample([(x,y) for x in range(w) for y in range(h)],n);cases.append(f"{w} {h} {n}\n"+" ".join(f"{x} {y}" for x,y in p)+"\n"+" ".join(f"{x} {y}" for x,y in q))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number==2251:
        R,C=3+(seed-1)%7,3+(seed-1)//7;grid=[["."]*C for _ in range(R)];grid[0][0]="S";grid[-1][-1]="E";return f"1 {R} {C}\n"+"\n".join("".join(x) for x in grid)+"\n0 0 0\n"
    if number==2663:return "\n".join(str(r.randint(0,30)) for _ in range(r.randint(1,10)))+"\n-1\n"
    if number==2745:return "\n".join(f"{r.randint(1,10)} {r.randint(0,99999999)}" for _ in range(r.randint(1,5)))+"\n0 0\n"
    if number==2977:return " ".join(str(r.randint(0,365)) for _ in range(4))+"\n"
    if number==2352:
        pts=sorted({(r.randint(0,100),r.randint(0,100)) for _ in range(30)},key=lambda p:(p[1],p[0]));return f"{len(pts)}\n"+"\n".join(f"{x} {y}" for x,y in pts)+"\n"
    if number==2599:
        n=r.randint(2,40);edges=[(i,r.randint(1,i-1)) for i in range(2,n+1)];return f"{n} {r.randint(1,n)}\n"+"\n".join(f"{a} {b}" for a,b in edges)+"\n"
    if number==2937:
        n=r.randint(3,12);return f"{n}\n"+"\n".join(" ".join(str(r.randint(0,255)) for _ in range(n)) for _ in range(n))+"\n"
    if number==2943:
        n=r.randint(1,20);weights=r.sample(range(1,1001),n);return f"{n}\n"+"\n".join(f"{x} c{i}" for i,x in enumerate(weights))+"\n"
    if number==1007:
        n,m=r.randint(1,30),r.randint(1,30);return f"{n} {m}\n"+"\n".join("".join(r.choice("ACGT") for _ in range(n)) for _ in range(m))+"\n"
    if number==1836:
        n=r.randint(2,50);return f"{n}\n"+" ".join(f"{r.uniform(.5,2.5):.5f}" for _ in range(n))+"\n"
    raise KeyError(number)

NO_INPUT={3225, 2698}
REFERENCE='# 参考解：差分标记牛区间内部 + 单调队列 DP，O(N+L)。\n# 原 AC 提交（43079895，见 samplecode.py）逐格标记牛区间，最坏 O(N*L)，大数据下过慢，改用本实现，原提交仍作交叉核对。\nimport sys\nfrom collections import deque\ndef main():\n    d=sys.stdin.buffer.read().split();n,L,a,b=int(d[0]),int(d[1]),int(d[2]),int(d[3])\n    diff=[0]*(L+2)\n    for i in range(n):\n        s_,e=int(d[4+2*i]),int(d[5+2*i]);diff[s_+1]+=1;diff[e]-=1\n    bad=[False]*(L+1);c=0\n    for i in range(L+1):c+=diff[i];bad[i]=c>0\n    INF=10**9;dp=[INF]*(L+1);dp[0]=0;q=deque()\n    for i in range(2*a,L+1,2):\n        j=i-2*a\n        if dp[j]<INF:\n            while q and dp[q[-1]]>=dp[j]:q.pop()\n            q.append(j)\n        while q and q[0]<i-2*b:q.popleft()\n        if not bad[i] and q:dp[i]=dp[q[0]]+1\n    print(dp[L] if dp[L]<INF else -1)\nmain()\n'
LANGUAGE='Python3'
NUMBER=2373
SAMPLE='2 8\n1 2\n6 7\n3 6\n'
def main():
 with tempfile.TemporaryDirectory() as d:
  d=Path(d);src=d/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE);cmd=[sys.executable,'-I',str(src)]
  if LANGUAGE!='Python3':
   exe=d/'s';subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]
  out=Path('data');out.mkdir(exist_ok=True)
  for p in out.glob('*'):p.unlink()
  cases=([SAMPLE] if SAMPLE or NUMBER in (2698,3225) else [])+([] if NUMBER in (2698,3225) else [generate(NUMBER,s) for s in range(1, 40)])
  for i,x in enumerate(cases):
   q=subprocess.run(cmd,input=x,text=True,capture_output=True,timeout=120,check=True);(out/f'{i}.in').write_text(x);(out/f'{i}.out').write_text(q.stdout.rstrip()+'\n')
if __name__=='__main__':main()
