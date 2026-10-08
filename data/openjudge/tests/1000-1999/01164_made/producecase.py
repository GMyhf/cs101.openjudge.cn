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
        if seed<=4:
            h,w=1+(seed-1)%8,2+(seed-1)//8;return f"{h}\n{w}\n"+"\n".join(" ".join(["15"]*w) for _ in range(h))+"\n"
        return castle_case(r,seed)
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

def castle_rooms(m,n,V,H):
    """V[i][j]: (i,j) 与 (i,j+1) 之间有墙；H[i][j]: (i,j) 与 (i+1,j) 之间有墙。返回房间数。"""
    seen=[[False]*n for _ in range(m)];cnt=0
    for i in range(m):
        for j in range(n):
            if seen[i][j]:continue
            cnt+=1;seen[i][j]=True;st=[(i,j)]
            while st:
                x,y=st.pop()
                for nx,ny,ok in ((x,y+1,y+1<n and not V[x][y]),(x,y-1,y>0 and not V[x][y-1]),(x+1,y,x+1<m and not H[x][y]),(x-1,y,x>0 and not H[x-1][y])):
                    if ok and not seen[nx][ny]:seen[nx][ny]=True;st.append((nx,ny))
    return cnt
def castle_text(m,n,V,H):
    rows=[]
    for i in range(m):
        row=[]
        for j in range(n):
            p=(1 if j==0 or V[i][j-1] else 0)+(2 if i==0 or H[i-1][j] else 0)+(4 if j==n-1 or V[i][j] else 0)+(8 if i==m-1 or H[i][j] else 0)
            row.append(str(p))
        rows.append(" ".join(row))
    return f"{m}\n{n}\n"+"\n".join(rows)+"\n"
def castle_case(r,seed):
    sizes={5:(50,50),6:(50,50),7:(50,50),8:(50,50),9:(50,50),10:(50,50),11:(50,50),12:(50,50),13:(1,50),14:(50,1),15:(2,1),16:(1,3),
           17:(50,50),18:(50,50),19:(49,50),20:(50,37),21:(10,10),22:(3,3),23:(50,50),24:(50,50),25:(25,50)}
    m,n=sizes.get(seed,(r.randint(2,50),r.randint(2,50)))
    kind=["prob","maze","split","voronoi","hole","prob","maze","voronoi"][seed%8] if m*n>2 else "split"
    if seed in (5,23):kind="hole"
    if seed in (6,24):kind="maze"
    if seed in (7,):kind="split"
    while True:
        V=[[False]*(n-1) for _ in range(m)];H=[[False]*n for _ in range(m-1)]
        if kind=="prob":
            q=r.choice((0.05,0.15,0.3,0.5,0.8))
            for i in range(m):
                for j in range(n-1):V[i][j]=r.random()<q
            for i in range(m-1):
                for j in range(n):H[i][j]=r.random()<q
        elif kind in ("maze","hole"):
            if kind=="maze":
                for i in range(m):V[i]=[True]*(n-1)
                for i in range(m-1):H[i]=[True]*n
                seen=[[False]*n for _ in range(m)];st=[(r.randrange(m),r.randrange(n))];seen[st[0][0]][st[0][1]]=True
                while st:
                    x,y=st[-1];nb=[(a,b) for a,b in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)) if 0<=a<m and 0<=b<n and not seen[a][b]]
                    if not nb:st.pop();continue
                    a,b=r.choice(nb);seen[a][b]=True;st.append((a,b))
                    if a==x:V[x][min(y,b)]=False
                    else:H[min(x,a)][y]=False
            x,y=r.randrange(m),r.randrange(n)
            if y<n-1:V[x][y]=True
            if y>0:V[x][y-1]=True
            if x<m-1:H[x][y]=True
            if x>0:H[x-1][y]=True
        elif kind=="split":
            if n>1 and (m==1 or r.random()<.5):
                c=r.randrange(n-1)
                for i in range(m):V[i][c]=True
            else:
                c=r.randrange(m-1);H[c]=[True]*n
        else:
            k=r.randint(2,min(40,m*n));pts=r.sample([(i,j) for i in range(m) for j in range(n)],k)
            lab=[[min(range(k),key=lambda t:(abs(pts[t][0]-i)+abs(pts[t][1]-j),t)) for j in range(n)] for i in range(m)]
            for i in range(m):
                for j in range(n-1):V[i][j]=lab[i][j]!=lab[i][j+1] or r.random()<.03
            for i in range(m-1):
                for j in range(n):H[i][j]=lab[i][j]!=lab[i+1][j] or r.random()<.03
        if castle_rooms(m,n,V,H)>=2:return castle_text(m,n,V,H)
def valid(text):
    """题面：先给南北向模块数 m、东西向模块数 n（m,n<=50，样例中各占一行），其后 m 行每行 n 个 0..15 的整数；
    内墙两侧都要标出（东墙与右邻西墙一致、南墙与下邻北墙一致），外围有墙（城堡封闭），且至少有两个房间。"""
    import re
    if not text.endswith('\n'):return False
    lines=text[:-1].split('\n')
    if len(lines)<3 or not re.fullmatch(r'[1-9][0-9]*',lines[0]) or not re.fullmatch(r'[1-9][0-9]*',lines[1]):return False
    m,n=int(lines[0]),int(lines[1])
    if not(1<=m<=50 and 1<=n<=50) or len(lines)!=m+2:return False
    g=[]
    for i in range(m):
        t=lines[i+2].split(' ')
        if len(t)!=n or not all(re.fullmatch(r'0|[1-9][0-9]?',x) and int(x)<=15 for x in t):return False
        g.append(list(map(int,t)))
    for i in range(m):
        for j in range(n):
            p=g[i][j]
            if j==0 and not p&1 or i==0 and not p&2 or j==n-1 and not p&4 or i==m-1 and not p&8:return False
            if j<n-1 and bool(p&4)!=bool(g[i][j+1]&1):return False
            if i<m-1 and bool(p&8)!=bool(g[i+1][j]&2):return False
    V=[[bool(g[i][j]&4) for j in range(n-1)] for i in range(m)];H=[[bool(g[i][j]&8) for j in range(n)] for i in range(m-1)]
    return castle_rooms(m,n,V,H)>=2
NO_INPUT={3225, 2698}
REFERENCE='# External reference: http://cs101.openjudge.cn/practice/01164/statistics/\n# Accepted submission: 51696044\n# Source: http://cs101.openjudge.cn/practice/solution/51696044/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nsys.setrecursionlimit(20000)\ndire = [(0, -1), (-1, 0), (0, 1), (1, 0)]\ndef dfs(visited, x, y):\n    global num\n    visited[x][y] = True\n    for i in range(4):\n        if cond[x][y] >> i & 1:\n            continue\n        nx, ny = x+dire[i][0], y+dire[i][1]\n        if not visited[nx][ny]:\n            num += 1\n            dfs(visited, nx, ny)\n    return num\nm = int(input())\nn = int(input())\ncond = [[int(x) for x in input().split()] for _ in range(m)]\nvisited = [[False]*n for _ in range(m)]\nres, cnt = 0, 0\nfor i in range(m):\n    for j in range(n):\n        if not visited[i][j]:\n            cnt += 1\n            num = 1\n            space = dfs(visited, i, j)\n            res = max(res, space)\nprint(cnt)\nprint(res)\n'
LANGUAGE='Python3'
NUMBER=1164
SAMPLE='4\n7\n11 6 11 6 3 10 6\n7 9 6 13 5 15 5\n1 10 12 7 13 7 5\n13 11 10 8 10 12 13\n'
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
