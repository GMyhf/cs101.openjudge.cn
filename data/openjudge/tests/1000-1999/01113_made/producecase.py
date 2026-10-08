import random,subprocess,sys,tempfile
from pathlib import Path
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
    if number==2373:
        L=2*r.randint(8,35);a=r.randint(1,max(1,L//6));b=r.randint(a,min(L//2,a+8));rows=[]
        for _ in range(r.randint(1,8)):
            x,y=sorted(r.sample(range(L+1),2));rows.append((x,y))
        return f"{len(rows)} {L}\n{a} {b}\n"+"\n".join(f"{x} {y}" for x,y in rows)+"\n"
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
def _seg_inter(p1,p2,p3,p4):
    def cr(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    def on(p,q,r):return min(p[0],q[0])<=r[0]<=max(p[0],q[0]) and min(p[1],q[1])<=r[1]<=max(p[1],q[1])
    d1=cr(p3,p4,p1);d2=cr(p3,p4,p2);d3=cr(p1,p2,p3);d4=cr(p1,p2,p4)
    if ((d1>0 and d2<0) or (d1<0 and d2>0)) and ((d3>0 and d4<0) or (d3<0 and d4>0)):return True
    if d1==0 and on(p3,p4,p1):return True
    if d2==0 and on(p3,p4,p2):return True
    if d3==0 and on(p1,p2,p3):return True
    if d4==0 and on(p1,p2,p4):return True
    return False

def valid(text):
    """题面契约：首行 N L（3<=N<=1000，1<=L<=1000），随后 N 行整点 Xi Yi（|Xi|,|Yi|<=10000），
    顶点互不相同、按顺时针给出、边除顶点外不相交（简单多边形）。"""
    import re
    lines=text.split('\n')
    if not text.endswith('\n'):return False
    lines=lines[:-1]
    def ints(s,k):
        t=s.split()
        if len(t)!=k or not all(re.fullmatch(r'-?\d+',x) for x in t):return None
        return list(map(int,t))
    if not lines:return False
    h=ints(lines[0],2)
    if not h:return False
    N,L=h
    if not(3<=N<=1000 and 1<=L<=1000) or len(lines)!=N+1:return False
    P=[]
    for s in lines[1:]:
        v=ints(s,2)
        if not v or not all(-10000<=c<=10000 for c in v):return False
        P.append(tuple(v))
    if len(set(P))!=N:return False
    area=sum(P[i][0]*P[(i+1)%N][1]-P[(i+1)%N][0]*P[i][1] for i in range(N))
    if area>=0:return False  # 顺时针 => 有向面积为负
    E=[(P[i],P[(i+1)%N]) for i in range(N)]
    box=[(min(a[0],b[0]),max(a[0],b[0]),min(a[1],b[1]),max(a[1],b[1])) for a,b in E]
    for i in range(N):
        a,b=E[i];c=E[(i+1)%N][1]
        dx1,dy1=b[0]-a[0],b[1]-a[1];dx2,dy2=c[0]-b[0],c[1]-b[1]
        if dx1*dy2-dy1*dx2==0 and dx1*dx2+dy1*dy2<0:return False  # 相邻边折返重叠
    for i in range(N):
        bi=box[i]
        for j in range(i+2,N):
            if i==0 and j==N-1:continue
            bj=box[j]
            if bi[1]<bj[0] or bj[1]<bi[0] or bi[3]<bj[2] or bj[3]<bi[2]:continue
            if _seg_inter(E[i][0],E[i][1],E[j][0],E[j][1]):return False
    return True

def _wall(P,L):
    import math
    pts=sorted(set(P))
    def cr(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in pts:
        while len(lo)>1 and cr(lo[-2],lo[-1],p)<=0:lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up)>1 and cr(up[-2],up[-1],p)<=0:up.pop()
        up.append(p)
    h=lo[:-1]+up[:-1]
    return sum(math.dist(h[i],h[(i+1)%len(h)]) for i in range(len(h)))+2*math.pi*L

def _star(r,N,R,cx,cy,rmin=1,convex=False):
    import math
    pts={}
    tries=0
    while len(pts)<N and tries<50*N:
        tries+=1
        a=r.uniform(0,2*math.pi);rad=R if convex else r.uniform(rmin,R)
        x=round(cx+rad*math.cos(a));y=round(cy+rad*math.sin(a))
        if not(-10000<=x<=10000 and -10000<=y<=10000) or (x,y)==(cx,cy):continue
        ang=math.atan2(y-cy,x-cx)
        if any(abs(ang-b)<1e-12 for b in ()):continue
        pts.setdefault(ang,(x,y))
    order=sorted(pts,reverse=True)  # 角度递减 => 顺时针
    return [pts[k] for k in order]

def _comb(r,teeth,W,H):
    # 梳子形：底边 + teeth 个齿，顺时针
    xs=sorted(r.sample(range(-W,W+1),2*teeth))
    top=[]
    for k in range(teeth):
        x1,x2=xs[2*k],xs[2*k+1];hh=r.randint(1,H)
        top+=[(x1,0),(x1,hh),(x2,hh),(x2,0)] if False else [(x1,hh),(x2,hh)]
    pts=[(xs[0],-H)]
    up=[]
    for k in range(teeth):
        x1,x2=xs[2*k],xs[2*k+1];hh=top[2*k][1]
        if k==0:up+=[(x1,hh),(x2,hh)]
        else:up+=[(x1,0),(x1,hh),(x2,hh)]
        if k<teeth-1:up+=[(x2,0)]
    return [(xs[0],-H)]+up+[(xs[-1],-H)]

def gen1113(seed):
    import math
    r=random.Random(1113*1000+seed)
    while True:
        L=r.choice([1,1000,r.randint(1,1000)])
        if seed==1:P=[(0,0),(0,1),(1,0)];L=1
        elif seed==2:P=[(-10000,-10000),(10000,10000),(10000,-10000)];L=1000
        elif seed==3:
            P=[(-10000,-10000),(-10000,10000),(10000,10000),(10000,-10000)];L=1000
        elif seed<=6:  # 近千点凸多边形（圆上整点）
            P=_star(r,1000,10000 if seed==4 else r.randint(2000,10000),0,0,convex=True)
            if len(P)>1000:P=P[:1000]
        elif seed<=9:  # 带共线点的矩形边：考察共线处理
            w,hh=r.randint(10,10000),r.randint(10,10000);x0,y0=r.randint(-10000,10000-w),r.randint(-10000,10000-hh)
            k=r.randint(50,240)
            left=sorted(set(r.randint(y0+1,y0+hh-1) for _ in range(k)))
            topp=sorted(set(r.randint(x0+1,x0+w-1) for _ in range(k)))
            right=sorted(set(r.randint(y0+1,y0+hh-1) for _ in range(k)),reverse=True)
            bot=sorted(set(r.randint(x0+1,x0+w-1) for _ in range(k)),reverse=True)
            P=[(x0,y0)]+[(x0,y) for y in left]+[(x0,y0+hh)]+[(x,y0+hh) for x in topp]+[(x0+w,y0+hh)]+[(x0+w,y) for y in right]+[(x0+w,y0)]+[(x,y0) for x in bot]
            P=P[:1000] if len(P)<=1000 else None
        elif seed<=13:  # 梳子形，大量凹点
            t=r.randint(2,249) if seed<13 else 249
            P=_comb(r,t,10000,10000)
        elif seed>=36:  # 满规模星形
            P=_star(r,1000,10000,r.randint(-50,50),r.randint(-50,50),rmin=r.choice([1,5000,9000]))
        else:
            N=r.choice([3,4,5,r.randint(3,50),r.randint(50,1000)])
            R=r.choice([5,100,10000,r.randint(10,10000)])
            cx=r.randint(-10000+R,10000-R);cy=r.randint(-10000+R,10000-R)
            P=_star(r,N,R,cx,cy,rmin=1)
        if not P or len(P)<3:continue
        P=P[:1000]
        if seed>3:
            k=r.randrange(len(P));P=P[k:]+P[:k]
        x=f'{len(P)} {L}\n'+''.join(f'{a} {b}\n' for a,b in P)
        v=_wall(P,L)
        if abs(v-math.floor(v)-0.5)<0.02:continue  # 避开四舍五入临界
        if valid(x):return x

REFERENCE="# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1113: Wall\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01113/\n# License: not declared; no license is inferred.\nimport math\nN,L=map(int,input().split())\npoints=[]\nfor _ in range(N):\n    points.append(tuple(map(int,input().split())))\ndef cross(o,a,b):\n\t# 矢量叉乘\n    return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])\ndef distance(a,b):\n    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)\n# 对x坐标进行排序\npoints.sort()\n# 下凸边\nlower=[]\nfor p in points:\n    while len(lower)>1 and cross(lower[-2],lower[-1],p)<=0:\n        lower.pop()\n    lower.append(p)\n# 上凸边\nupper=[]\nfor p in reversed(points):\n    while len(upper)>1 and cross(upper[-2],upper[-1],p)<=0:\n        upper.pop()\n    upper.append(p)\nhull=lower[:-1]+upper[:-1]\nn=len(hull)\nl=0\nfor i in range(n):\n    j=(i+1)%n\n    l+=distance(hull[i],hull[j])\nl+=2*math.pi*L\nprint(f'{l:.0f}')\n"
LANGUAGE='Python3'
NUMBER=1113
SAMPLE='9 100\n200 400\n300 400\n300 300\n400 300\n400 400\n500 400\n500 200\n350 200\n200 200\n'
def main():
 with tempfile.TemporaryDirectory() as d:
  d=Path(d);src=d/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE);cmd=[sys.executable,'-I',str(src)]
  if LANGUAGE!='Python3':
   exe=d/'s';subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]
  out=Path('data');out.mkdir(exist_ok=True)
  for p in out.glob('*'):p.unlink()
  cases=([SAMPLE] if SAMPLE or NUMBER in (2698,3225) else [])+([] if NUMBER in (2698,3225) else [gen1113(s) for s in range(1, 40)])
  for i,x in enumerate(cases):
   assert valid(x),i
   q=subprocess.run(cmd,input=x,text=True,capture_output=True,timeout=120,check=True);(out/f'{i}.in').write_text(x);(out/f'{i}.out').write_text(q.stdout.rstrip()+'\n')
if __name__=='__main__':main()
