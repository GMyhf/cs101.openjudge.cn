import random,subprocess,sys,tempfile
from pathlib import Path
def generate(n, seed):
    r=random.Random(seed)
    if n==2694:
        return f"+ * {r.randint(-20,20)} {r.randint(-20,20)} / {r.randint(-20,20)} {r.randint(1,20)}\n"
    if n==2945:
        k=r.randint(3,25);return f"{k}\n"+' '.join(str(r.randint(1,500)) for _ in range(k))+'\n'
    if n==2746:
        return '\n'.join(f"{r.randint(1,80)} {r.randint(1,80)}" for _ in range(r.randint(1,5)))+'\n0 0\n'
    if n==2773:
        T=r.randint(20,300);m=r.randint(2,20);return f"{T} {m}\n"+'\n'.join(f"{r.randint(1,100)} {r.randint(1,100)}" for _ in range(m))+'\n'
    if n==2734:return f"{r.randint(1,65535)}\n"
    if n==2488:
        z=[(r.randint(1,6),r.randint(1,6)) for _ in range(r.randint(1,4))];return str(len(z))+'\n'+'\n'.join(f'{a} {b}' for a,b in z)+'\n'
    if n==2810:return f"{r.randint(2,45)}\n"
    if n==2299:
        a=[r.randint(0,10**9) for _ in range(r.randint(2,40))];return f"{len(a)}\n"+'\n'.join(map(str,a))+'\n0\n'
    if n==2775:return f"file{seed}\ndir{seed}\nfileA\n]\nfileZ\n*\n#\n"
    if n==2815:
        rows,cols=r.randint(2,7),r.randint(2,7);g=[[0]*cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if j==0:g[i][j]|=1
                if i==0:g[i][j]|=2
                if j==cols-1:g[i][j]|=4
                if i==rows-1:g[i][j]|=8
                if j+1<cols and r.random()<.35:g[i][j]|=4;g[i][j+1]|=1
                if i+1<rows and r.random()<.35:g[i][j]|=8;g[i+1][j]|=2
        return f"{rows}\n{cols}\n"+'\n'.join(' '.join(map(str,x)) for x in g)+'\n'
    if n==2524:
        out=[]
        for _ in range(r.randint(1,3)):
            a=r.randint(2,30);edges={(r.randint(1,a),r.randint(1,a)) for _ in range(r.randint(0,a))};edges={(x,y) for x,y in edges if x!=y};out.append(f'{a} {len(edges)}');out += [f'{x} {y}' for x,y in edges]
        return '\n'.join(out)+'\n0 0\n'
    if n==1088:
        a,b=r.randint(2,12),r.randint(2,12);return f'{a} {b}\n'+'\n'.join(' '.join(str(r.randint(0,500)) for _ in range(b)) for _ in range(a))+'\n'
    if n==1182:
        N=r.randint(3,50);k=r.randint(2,70);return f'{N} {k}\n'+'\n'.join(f'{r.randint(1,2)} {r.randint(1,N+3)} {r.randint(1,N+3)}' for _ in range(k))+'\n'
    if n==1760:
        paths=[]
        for i in range(r.randint(2,20)):paths.append('\\'.join(f'D{r.randint(1,8)}' for _ in range(r.randint(1,5))))
        return str(len(paths))+'\n'+'\n'.join(paths)+'\n'
    if n==2386:
        a,b=r.randint(2,15),r.randint(2,15);return f'{a} {b}\n'+'\n'.join(''.join(r.choice('W..') for _ in range(b)) for _ in range(a))+'\n'
    if n==2456:
        N=r.randint(3,30);C=r.randint(2,N);x=sorted(r.sample(range(1,10000),N));return f'{N} {C}\n'+'\n'.join(map(str,x))+'\n'
    if n==2808:
        L=r.randint(10,1000);m=r.randint(1,15);return f'{L} {m}\n'+'\n'.join(f'{(a:=r.randint(0,L))} {r.randint(a,L)}' for _ in range(m))+'\n'
    if n==2995:
        N=r.randint(2,80);return f'{N}\n'+' '.join(str(r.randint(1,1000)) for _ in range(N))+'\n'
    if n==2760:
        N=r.randint(2,20);return f'{N}\n'+'\n'.join(' '.join(str(r.randint(0,100)) for _ in range(i)) for i in range(1,N+1))+'\n'
    if n==3151:
        A,B=r.randint(2,30),r.randint(2,30);C=r.randint(1,max(A,B));return f'{A} {B} {C}\n'
    if n==2733:return f'{r.randint(1,2999)}\n'
    if n==2774:
        N=r.randint(2,30);K=r.randint(1,100);return f'{N} {K}\n'+'\n'.join(str(r.randint(1,10000)) for _ in range(N))+'\n'
    if n==2806:
        return '\n'.join(f"{''.join(r.choice('abcd') for _ in range(r.randint(1,20)))} {''.join(r.choice('abcd') for _ in range(r.randint(1,20)))}" for _ in range(r.randint(1,6)))+'\n'
    if n==1426:return '\n'.join(str(r.randint(1,200)) for _ in range(r.randint(1,6)))+'\n0\n'
    if n==1852:
        out=[str(r.randint(1,4))]
        for _ in range(int(out[0])):
            L=r.randint(10,1000);x=sorted(r.sample(range(1,L),r.randint(1,min(20,L-1))));out += [f'{L} {len(x)}',' '.join(map(str,x))]
        return '\n'.join(out)+'\n'
    if n==2039:
        c=r.randint(2,20);s=''.join(r.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(c*r.randint(1,10)));return f'{c}\n{s}\n'
    if n==2754:
        q=[r.randint(1,92) for _ in range(r.randint(1,8))];return str(len(q))+'\n'+'\n'.join(map(str,q))+'\n'
    if n==2783:
        N=r.randint(2,30);return f'{N}\n'+'\n'.join(f'{r.randint(1,10000)} {r.randint(1,10000)}' for _ in range(N))+'\n0\n'
    if n==1094:
        N=r.randint(3,10);rels=[]
        for _ in range(r.randint(1,20)):
            a,b=r.sample(range(N),2);rels.append(f'{chr(65+a)}<{chr(65+b)}')
        return f'{N} {len(rels)}\n'+'\n'.join(rels)+'\n0 0\n'
    if n==1376:
        a,b=r.randint(5,12),r.randint(5,12);g=[[0]*b for _ in range(a)];sx,sy=1,1;tx,ty=a-2,b-2
        return f'{a} {b}\n'+'\n'.join(' '.join(map(str,x)) for x in g)+f'\n{sx} {sy} {tx} {ty} east\n0 0\n'
    if n==1833:
        out=[str(r.randint(1,4))]
        for _ in range(int(out[0])):
            N=r.randint(2,30);p=list(range(1,N+1));r.shuffle(p);out += [f'{N} {r.randint(1,min(20,N))}',' '.join(map(str,p))]
        return '\n'.join(out)+'\n'
    if n==1961:
        out=[]
        for _ in range(r.randint(1,4)):
            s=''.join(r.choice('abc') for _ in range(r.randint(2,100)));out += [str(len(s)),s]
        return '\n'.join(out)+'\n0\n'
    if n==2255:
        def traversals(vals):
            if not vals:return '',''
            k=r.randrange(len(vals));a,b=traversals(vals[:k]);c,d=traversals(vals[k+1:]);return vals[k]+a+c,a+vals[k]+d
        rows=[]
        for _ in range(r.randint(1,4)):
            s=''.join(r.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ',r.randint(1,12)));rows.append(' '.join(traversals(s)))
        return '\n'.join(rows)+'\n'
    if n==2811:return '\n'.join(' '.join(str(r.randint(0,1)) for _ in range(6)) for _ in range(5))+'\n'
    if n==3248:return '\n'.join(f'{r.randint(1,2**31-1)} {r.randint(1,2**31-1)}' for _ in range(r.randint(1,8)))+'\n'
    if n==2692:
        coins=list('ABCDEFGHIJKL');coin=r.choice(coins);heavy=r.choice([True,False]);normal=[x for x in coins if x!=coin];r.shuffle(normal);x=normal[0]
        state='down' if heavy else 'up'
        a,b,c,d=map(''.join,(normal[:4],normal[4:8],normal[3:7],normal[7:11]))
        return f'1\n{coin} {x} {state}\n{a} {b} even\n{c} {d} even\n'
    if n==3143:return f'{r.randint(4,2000)}\n'
    if n==1860:return gen1860(r,seed)
    if n==1035:
        words=['cat','dog','apple','word'+chr(97+seed%26)];queries=[words[-1],words[-1][:-1]+'z','dogs'];return '\n'.join(words+['#']+queries+['#'])+'\n'
    if n==2431:
        N=r.randint(1,20);L=r.randint(20,500);stops=sorted({r.randint(1,L-1):r.randint(1,100) for _ in range(N)}.items(),reverse=True);return str(len(stops))+'\n'+'\n'.join(f'{d} {f}' for d,f in stops)+f'\n{L} {r.randint(1,100)}\n'
    if n==2756:return f'{r.randint(1,1000)} {r.randint(1,1000)}\n'
    if n==2757:
        N=r.randint(1,80);return f'{N}\n'+' '.join(str(r.randint(0,10000)) for _ in range(N))+'\n'
    if n==1159:
        N=r.randint(3,100);s=''.join(r.choice('abcXYZ09') for _ in range(N));return f'{N}\n{s}\n'
    if n==1724:
        N=r.randint(2,12);K=r.randint(0,50);edges=[]
        for i in range(1,N):edges.append((i,i+1,r.randint(1,30),r.randint(0,10)))
        for _ in range(r.randint(0,20)):
            a,b=r.sample(range(1,N+1),2);edges.append((a,b,r.randint(1,50),r.randint(0,15)))
        return f'{K}\n{N}\n{len(edges)}\n'+'\n'.join(' '.join(map(str,e)) for e in edges)+'\n'
    if n==2706:return f"{1000+seed}\n"
    if n==2996:
        N=r.randint(2,80);p=list(range(1,N+1));r.shuffle(p);return f'{N}\n{r.randint(1,min(30,N))}\n'+' '.join(map(str,p))+'\n'
    if n==3254:return '\n'.join(f'{r.randint(2,100)} {r.randint(1,100)} {r.randint(1,100)}' for _ in range(r.randint(1,5)))+'\n0 0 0\n'
    if n==2502:
        hx,hy,sx,sy=[r.randint(0,10000) for _ in range(4)];return f'{hx} {hy} {sx} {sy}\n{r.randint(0,10000)} {r.randint(0,10000)} {r.randint(0,10000)} {r.randint(0,10000)} -1 -1\n'
    if n==2748:return ''.join(r.sample('abcdefghi',r.randint(1,5)))+'\n'
    if n==1191:return f'{r.randint(2,10)}\n'+'\n'.join(' '.join(str(r.randint(0,99)) for _ in range(8)) for _ in range(8))+'\n'
    if n==2287:
        N=r.randint(1,30);return f'{N}\n'+' '.join(str(r.randint(1,100)) for _ in range(N))+'\n'+' '.join(str(r.randint(1,100)) for _ in range(N))+'\n0\n'
    if n==2981:return str(r.randrange(10**50))+'\n'+str(r.randrange(10**50))+'\n'
    if n==2750:return f'{r.randint(1,32767)}\n'
    if n==2788:return '\n'.join(f'{r.randint(1,100000)} {r.randint(1,1000000000)}' for _ in range(r.randint(1,6)))+'\n0 0\n'
    if n==2802:
        w,h=r.randint(2,8),r.randint(2,8);board=[' '*w for _ in range(h)];y2=1 if seed%2==0 else h
        return f'{w} {h}\n'+'\n'.join(board)+f'\n1 1 {w} {y2}\n0 0 0 0\n0 0\n'
    if n==1003:return '\n'.join(f'{r.uniform(.01,5.20):.2f}' for _ in range(r.randint(1,6)))+'\n0.00\n'
    if n==1011:
        a=[r.randint(1,30) for _ in range(r.randint(3,20))];return f'{len(a)}\n'+' '.join(map(str,a))+'\n0\n'
    if n==1017:return ' '.join(str(r.randint(0,20)) for _ in range(6))+'\n0 0 0 0 0 0\n'
    if n==1065:
        out=[str(r.randint(1,3))]
        for _ in range(int(out[0])):
            N=r.randint(1,30);out += [str(N),' '.join(f'{r.randint(1,30)} {r.randint(1,30)}' for _ in range(N))]
        return '\n'.join(out)+'\n'
    if n==1218:
        q=[r.randint(5,100) for _ in range(r.randint(1,10))];return str(len(q))+'\n'+'\n'.join(map(str,q))+'\n'
    raise KeyError(n)

import math,re
from fractions import Fraction
_NUM2=re.compile(r"\d+(\.\d{1,2})?$")
_REAL=re.compile(r"\d+(\.\d+)?$")
def valid(text):
    """题面约束：首行 N M S V，1<=S<=N<=100，1<=M<=100，V 实数且 0<=V<=1000；随后 M 行各 6 个数
    A B R_AB C_AB R_BA C_BA：A、B 为 1..N 的币种编号（兑换点经营两种不同货币，A!=B），
    汇率为至多两位小数的实数且 0.01<=rate<=100，手续费至多两位小数且 0<=c<=100。
    “任意简单兑换序列首末比值 < 10^4” 无法精确多项式判定，这里不核（生成器按构造保证）。"""
    if not text.endswith("\n"):return False
    lines=text[:-1].split("\n")
    head=lines[0].split()
    if len(head)!=4:return False
    try:N,M,S=int(head[0]),int(head[1]),int(head[2])
    except ValueError:return False
    if not all(re.fullmatch(r"\d+",t) for t in head[:3]) or not _REAL.match(head[3]):return False
    V=Fraction(head[3])
    if not(1<=S<=N<=100 and 1<=M<=100 and 0<=V<=1000):return False
    if len(lines)!=M+1:return False
    for ln in lines[1:]:
        t=ln.split()
        if len(t)!=6 or not re.fullmatch(r"\d+",t[0]) or not re.fullmatch(r"\d+",t[1]):return False
        A,B=int(t[0]),int(t[1])
        if not(1<=A<=N and 1<=B<=N and A!=B):return False
        if not all(_NUM2.match(x) for x in t[2:]):return False
        r1,c1,r2,c2=map(Fraction,t[2:])
        if not(Fraction(1,100)<=r1<=100 and Fraction(1,100)<=r2<=100 and 0<=c1<=100 and 0<=c2<=100):return False
    return True

def exact1860(text,wrong=False):
    """精确有理数 Bellman-Ford（独立于浮点参考解）；wrong=True 模拟“先换汇再扣手续费”的常见错误。"""
    t=text.split();N,M,S=int(t[0]),int(t[1]),int(t[2]);V=Fraction(t[3]);e=[];k=4
    for _ in range(M):
        A,B=int(t[k])-1,int(t[k+1])-1;r1,c1,r2,c2=map(Fraction,t[k+2:k+6]);k+=6
        e+=[(A,B,r1,c1),(B,A,r2,c2)]
    d=[None]*N;d[S-1]=V
    for i in range(N+1):
        ch=False
        for x,y,rr,c in e:
            if d[x] is not None and (wrong or d[x]>=c):
                z=d[x]*rr-c if wrong else (d[x]-c)*rr
                if z<0:continue
                if d[y] is None or z>d[y]:d[y]=z;ch=True
        if not ch:return "NO"
        if d[S-1]>V:return "YES"
    return "YES"

def trap1860(r,seed):
    # 小规模边界组：手续费相对本金不可忽略，“先乘汇率再扣手续费”的写法会得出相反结论
    while True:
        N=r.randint(2,4);S=r.randint(1,N);edges=[]
        for i in range(1,N):edges.append([i,r.randrange(i)])
        for _ in range(r.randint(0,3)):edges.append(r.sample(range(N),2))
        rows=[]
        for a,b in edges:
            rows.append(f"{a+1} {b+1} {r.randint(10,300)/100:.2f} {r.randint(0,2000)/100:.2f} {r.randint(10,300)/100:.2f} {r.randint(0,2000)/100:.2f}")
        text=f"{N} {len(rows)} {S} {r.randint(0,10000)/100:.2f}\n"+"\n".join(rows)+"\n"
        if not valid(text):continue
        ans=exact1860(text)
        if ans==("YES" if seed%2 else "NO") and exact1860(text,True)!=ans:return text

def gen1860(r,seed):
    if seed in(2,6,8,9,12,15):return trap1860(r,seed)
    # 公平价模型：每种货币一个“真实价格”p_i，普通兑换点汇率 = p_A/p_B*(1-点差) 向下取两位小数，天然无套利；
    # 再按需植入少量“有利环”。任意序列的首末比值 <= max p/min p * Π(植入环增益) 远小于 1e4。
    if seed<=8:N=r.randint(2,5);M=r.randint(1,8)
    elif seed<=20:N=r.randint(5,40);M=r.randint(N-1 if N<=100 else 99,100)
    elif seed<=30:N=r.randint(60,100);M=100
    else:N=100;M=100
    want="YES" if seed%2 else "NO"
    kind=seed%5  # 0:植入环但不可达 1:植入环增益太小被手续费吃掉 其余:普通
    for attempt in range(2000):
        p=[math.exp(r.uniform(-.7,.7)) for _ in range(N)]
        S=r.randint(1,N)
        comp=[0]*N
        if kind==0 and want=="NO" and N>=4:
            # 两个连通块，S 所在块之外放有利环
            other=set(r.sample([i for i in range(N) if i!=S-1],r.randint(2,N//2)))
            comp=[1 if i in other else 0 for i in range(N)]
        def rate(a,b,gain=0.0):
            f=p[a]/p[b]*(1+gain)
            v=math.ceil(f*100)/100 if gain>0 else math.floor(f*(1-r.uniform(0,.03))*100)/100
            return min(100.0,max(.01,v))
        def comm():
            u=r.random()
            if u<.3:return 0.0
            if u<.8:return round(r.uniform(0,1),2)
            return round(r.uniform(0,100 if r.random()<.2 else 10),2)
        edges=[]
        plant=want=="YES" or kind in(0,1)
        pc=1 if kind==0 and want=="NO" and N>=4 else 0   # 植入环所在连通块
        for c in (0,1):
            nodes=[i for i in range(N) if comp[i]==c];r.shuffle(nodes)
            if not nodes:continue
            done=nodes[:1]
            if plant and c==pc and len(nodes)>=2:
                # 先连若干个有利环（环上各点彼此连通），再把剩余节点挂成树
                ncyc=1 if N>=60 else r.randint(1,2)
                for _ in range(ncyc):
                    k=r.randint(2,min(6,len(nodes)))
                    cyc=r.sample(nodes,k)
                    g=r.choice([1e-4,1e-3,.005,.01,.03]) if not(kind==1 and want=="NO") else 1e-4
                    for i in range(k):
                        x,y=cyc[i],cyc[(i+1)%k]
                        edges.append([x,y,rate(x,y,g),round(r.uniform(0,2),2) if r.random()<.6 else 0.0,rate(y,x),comm()])
                    if ncyc==1:done=cyc
                    else:
                        x,y=cyc[0],r.choice(done)
                        if x!=y:edges.append([x,y,rate(x,y),comm(),rate(y,x),comm()])
                        done=list(dict.fromkeys(done+cyc))
            for a in nodes:
                if a in done:continue
                b=r.choice(done);edges.append([a,b,rate(a,b),comm(),rate(b,a),comm()]);done.append(a)
        while len(edges)<M:
            c=comp[r.randrange(N)];nodes=[i for i in range(N) if comp[i]==c]
            if len(nodes)<2:continue
            a,b=r.sample(nodes,2);edges.append([a,b,rate(a,b),comm(),rate(b,a),comm()])
        if len(edges)>100:continue
        r.shuffle(edges)
        for e in edges:
            if r.random()<.5:e[:]=[e[1],e[0],e[4],e[5],e[2],e[3]]
        if seed==4:V="0"
        elif seed in(5,31):V="1000"
        elif seed==7:V=f"{r.uniform(0,1):.2f}"
        else:V=f"{r.uniform(0,1000):.{r.choice([0,1,2])}f}"
        text=f"{N} {len(edges)} {S} {V}\n"+"\n".join(f"{a+1} {b+1} {r1:.2f} {c1:.2f} {r2:.2f} {c2:.2f}" for a,b,r1,c1,r2,c2 in edges)+"\n"
        if valid(text) and exact1860(text)==want:return text
    raise RuntimeError(seed)

REFERENCE="# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 1860: Currency Exchange\n# Fenced code block index: None\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2025sp_routine/01860/\n# License: not declared in source collection; no license is inferred.\nimport sys\na=sys.stdin.buffer.read().split();it=iter(a);n=int(next(it));m=int(next(it));s=int(next(it))-1;v=float(next(it));e=[]\nfor _ in range(m):\n x=int(next(it))-1;y=int(next(it))-1;r1=float(next(it));c1=float(next(it));r2=float(next(it));c2=float(next(it));e += [(x,y,r1,c1),(y,x,r2,c2)]\nd=[0.0]*n;d[s]=v\ngain=False\nfor i in range(n):\n changed=False\n for x,y,r,c in e:\n  z=(d[x]-c)*r\n  if z>d[y]:d[y]=z;changed=True\n if i==n-1 and changed:gain=True\n if not changed:break\nprint('YES' if gain else 'NO')\n"
NUMBER=1860
SAMPLE='3 2 1 20.0\n1 2 1.00 1.00 1.00 1.00\n2 3 1.10 1.00 1.10 1.00\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
