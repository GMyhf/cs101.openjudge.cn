import random,subprocess,sys,tempfile
from pathlib import Path
def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    letters = "abcdefghijklmnopqrstuvwxyz"
    word = lambda a=1, b=10: "".join(r.choice(letters) for _ in range(r.randint(a, b)))
    if number == 3247: return f"{seed % 9 + 1}\n"
    if number == 1002:
        base = ["4873279", "ITS-EASY", "888-4567", "3-10-10-10"]
        rows = [r.choice(base) for _ in range(r.randint(2, 30))]
        return f"{len(rows)}\n" + "\n".join(rows) + "\n"
    if number == 2181:
        a = [r.randint(0, 1000) for _ in range(r.randint(1, 100))]
        return f"{len(a)}\n" + "\n".join(map(str, a)) + "\n"
    if number == 2936:
        a = sorted(r.sample(range(1, 9), r.randint(1, 8))); return f"{len(a)}\n" + " ".join(map(str, a)) + "\n"
    if number == 2814: return " ".join(str(r.randrange(4)) for _ in range(9)) + "\n"
    if number == 2910:
        chars = letters + letters.upper() + "0123456789*?-_"; return "".join(r.choice(chars) for _ in range(r.randint(1, 100))) + "\n"
    if number == 2940: return f"{r.randint(1,9)} {r.randint(1,9)}\n"
    if number == 1178:
        squares = [f"{chr(65+x)}{y+1}" for y in range(8) for x in range(8)]
        return "".join(r.sample(squares, r.randint(2, 12))) + "\n"
    if number == 1190: return f"{r.randint(1, 2000)}\n{r.randint(1, 7)}\n"
    if number == 2899:
        rows = [" ".join(str(r.randint(-1000, 1000)) for _ in range(5)) for _ in range(5)]
        return "\n".join(rows) + f"\n{r.randint(-2,6)} {r.randint(-2,6)}\n"
    if number == 2942: return f"{seed % 19 + 1}\n"
    if number == 2791:
        pts=set(); n=r.randint(2,8)
        while len(pts)<n: pts.add((r.randint(-20,20),r.randint(-20,20)))
        return f"{n}\n"+"\n".join(f"{x} {y}" for x,y in pts)+"\n0\n"
    if number == 2804:
        foreign=[]; rows=[]
        for _ in range(r.randint(2,15)):
            f=word(); foreign.append(f); rows.append(f"{word()} {f}")
        docs=[r.choice(foreign+[word()]) for _ in range(r.randint(2,20))]
        return "\n".join(rows)+"\n\n"+"\n".join(docs)+"\n"
    if number == 1077:
        board=list("12345678x"); pos=8
        for _ in range(r.randint(0,30)):
            y,x=divmod(pos,3); choices=[q for q in (pos-3,pos+3,pos-1,pos+1) if 0<=q<9 and abs(q%3-x)+abs(q//3-y)==1]
            q=r.choice(choices);board[pos],board[q]=board[q],board[pos];pos=q
        return " ".join(board)+"\n"
    if number == 1230:
        cases=[]
        for _ in range(r.randint(1,4)):
            n=r.randint(1,20); k=r.randint(0,10); walls=[]
            for _ in range(n):
                x1,x2=sorted((r.randint(0,100),r.randint(0,100))); y=r.randint(0,100);walls.append(f"{x1} {y} {x2} {y}")
            cases.append(f"{n} {k}\n"+"\n".join(walls))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number == 1276:
        cases=[]
        for _ in range(r.randint(1,5)):
            n=r.randint(1,12); pairs=[(r.randint(1,20),r.randint(1,200)) for _ in range(n)]
            cases.append(f"{r.randint(0,3000)} {n} "+" ".join(f"{c} {v}" for c,v in pairs))
        return "\n".join(cases)+"\n"
    if number == 1481:
        w=h=r.randint(5,15); grid=[["."]*w for _ in range(h)]
        for y,x in [(2,2),(2,3),(3,2),(3,3)]: grid[y][x]="*"
        for y,x in r.sample([(2,2),(2,3),(3,2),(3,3)],r.randint(1,4)):grid[y][x]="X"
        return f"{w} {h}\n"+"\n".join("".join(x) for x in grid)+"\n0 0\n"
    if number == 2049:
        if seed % 2:
            x,y=r.randint(1,198),r.randint(1,198);return f"0 0\n{x}.5 {y}.5\n-1 -1\n"
        # The statement sample exercises walls and doors; translate it so even
        # seeds remain distinct without changing its topology.
        d=seed % 30
        return ("8 9\n"+"\n".join((f"{1+d} 1 1 3",f"{2+d} 1 1 3",f"{3+d} 1 1 3",f"{4+d} 1 1 3",
          f"{1+d} 1 0 3",f"{1+d} 2 0 3",f"{1+d} 3 0 3",f"{1+d} 4 0 3",
          f"{2+d} 1 1",f"{2+d} 2 1",f"{2+d} 3 1",f"{3+d} 1 1",f"{3+d} 2 1",f"{3+d} 3 1",
          f"{1+d} 2 0",f"{3+d} 3 0",f"{4+d} 3 1"))+f"\n{1.5+d} 1.5\n-1 -1\n")
    if number == 2767:
        chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ ,.'!?";return "".join(r.choice(chars) for _ in range(r.randint(1,200)))+"\n"
    if number == 2787:
        rows=[" ".join(str(r.randint(1,9)) for _ in range(4)) for _ in range(r.randint(1,12))]
        return "\n".join(rows)+"\n0 0 0 0\n"
    if number == 2927:
        chars=letters+"0123456789 &^$#@*";return "\n".join("".join(r.choice(chars) for _ in range(r.randint(1,80))) for _ in range(r.randint(1,8)))+"\n"
    if number == 2979:
        cases=[]
        for _ in range(r.randint(1,3)):
            n=r.randint(1,20);m=r.randint(1,n);cases.append(f"{n} {m}\n"+"\n".join(f"{r.randint(0,20)} {r.randint(0,20)}" for _ in range(n)))
        return "\n".join(cases)+"\n0 0\n"
    if number == 1008:
        months="pop no zip zotz tzec xul yoxkin mol chen yax zac ceh mac kankin muan pax koyab cumhu uayet".split();rows=[]
        for _ in range(r.randint(1,12)):
            m=r.randrange(19);day=r.randrange(5 if m==18 else 20);rows.append(f"{day}. {months[m]} {r.randint(0,5000)}")
        return f"{len(rows)}\n"+"\n".join(rows)+"\n"
    if number == 1019:
        a=[r.randint(1,2_147_483_647) for _ in range(r.randint(1,10))];return f"{len(a)}\n"+"\n".join(map(str,a))+"\n"
    if number in (1026,2818):
        n=r.randint(1,30);perm=list(range(1,n+1));r.shuffle(perm);rows=[]
        for _ in range(r.randint(1,8)):
            msg="".join(r.choice(letters+" ") for _ in range(r.randint(1,n)));rows.append(f"{r.randint(1,10**6)} {msg}")
        return f"{n}\n"+" ".join(map(str,perm))+"\n"+"\n".join(rows)+"\n0\n0\n"
    if number == 1047:
        return "\n".join("".join(r.choice("0123456789") for _ in range(r.randint(2,35))) for _ in range(r.randint(1,8)))+"\n"
    if number == 1056:
        groups=[]
        for _ in range(r.randint(1,5)):
            codes=set()
            while len(codes)<r.randint(2,8):codes.add("".join(r.choice("01") for _ in range(r.randint(1,10))))
            groups.extend(sorted(codes));groups.append("9")
        return "\n".join(groups)+"\n"
    if number == 1742:
        cases=[]
        for _ in range(r.randint(1,4)):
            n=r.randint(1,20);m=r.randint(1,1000);a=[r.randint(1,100) for _ in range(n)];c=[r.randint(1,20) for _ in range(n)]
            cases.append(f"{n} {m}\n"+" ".join(map(str,a+c)))
        return "\n".join(cases)+"\n0 0\n"
    if number == 1789:
        cases=[]
        for _ in range(r.randint(1,3)):
            codes=set()
            while len(codes)<r.randint(2,30):codes.add("".join(r.choice(letters) for _ in range(7)))
            cases.append(f"{len(codes)}\n"+"\n".join(sorted(codes)))
        return "\n".join(cases)+"\n0\n"
    if number == 1941:return "\n".join(map(str,[r.randint(1,8) for _ in range(r.randint(1,5))]))+"\n0\n"
    if number == 2092:
        cases=[]
        for _ in range(r.randint(1,4)):
            n,m=r.randint(2,20),r.randint(1,20);cases.append(f"{n} {m}\n"+"\n".join(" ".join(str(r.randint(1,60)) for _ in range(m)) for _ in range(n)))
        return "\n".join(cases)+"\n0 0\n"
    if number == 2253:
        cases=[]
        for _ in range(r.randint(1,4)):
            n=r.randint(2,30);cases.append(f"{n}\n"+"\n".join(f"{r.randint(0,1000)} {r.randint(0,1000)}" for _ in range(n)))
        return "\n".join(cases)+"\n0\n"
    if number == 2337:
        cases=[]
        for _ in range(r.randint(1,5)):
            words=[word() for _ in range(r.randint(3,40))];cases.append(f"{len(words)}\n"+"\n".join(words))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number == 2676:
        a=[r.randint(1,20) for _ in range(r.randint(1,100))];return f"{len(a)}\n"+" ".join(map(str,a))+"\n"
    if number == 2712:
        md=[31,28,31,30,31,30,31,31,30,31,30,31];days=[]
        for m,d in enumerate(md,1):days.extend((m,x) for x in range(1,d+1))
        rows=[]
        for _ in range(r.randint(1,8)):
            a=r.randint(0,350);b=r.randint(a+1,min(364,a+30));rows.append(f"{days[a][0]} {days[a][1]} {r.randint(1,1000)} {days[b][0]} {days[b][1]}")
        return f"{len(rows)}\n"+"\n".join(rows)+"\n"
    if number == 2883:return "\n".join(" ".join(str(r.randint(-99,99)) for _ in range(5)) for _ in range(r.randint(1,12)))+"\n"
    if number == 2911:return f"{r.randint(1000,9999)}\n"
    if number == 2913:
        chars="".join(chr(i) for i in range(32,123));return "".join(r.choice(chars) for _ in range(r.randint(1,100)))+"\n"
    if number == 1753:return "\n".join("".join(r.choice("bw") for _ in range(4)) for _ in range(4))+"\n"
    raise KeyError(number)

REFERENCE='# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 2049: Finding Nemo\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/02049/\n# License: not declared; no license is inferred.\n# 本地修订：原代码用普通 BFS（入队即标记访问）累计门数，求的是“步数最短路径上的门数”，\n# 不是最少门数；改为 0-1 BFS（不过门代价 0、过门代价 1）。\nimport sys\nfrom collections import deque\n\ndef main():\n    data = sys.stdin.read().split()\n    p = 0\n    out = []\n    while True:\n        m, n = int(data[p]), int(data[p + 1]); p += 2\n        if m == -1 and n == -1:\n            break\n        # vert[x][y]: 竖直单位段 (x,y)-(x,y+1)；horz[x][y]: 水平单位段 (x,y)-(x+1,y)；0 空 1 墙 2 门\n        vert = [[0] * 201 for _ in range(201)]\n        horz = [[0] * 201 for _ in range(201)]\n        for _ in range(m):\n            x, y, d, t = map(int, data[p:p + 4]); p += 4\n            for k in range(t):\n                if d:\n                    vert[x][y + k] = 1\n                else:\n                    horz[x + k][y] = 1\n        for _ in range(n):\n            x, y, d = map(int, data[p:p + 3]); p += 3\n            if d:\n                vert[x][y] = 2\n            else:\n                horz[x][y] = 2\n        fx, fy = float(data[p]), float(data[p + 1]); p += 2\n        sx, sy = int(fx), int(fy)\n        # 格子 (i,j) 表示 [i,i+1]x[j,j+1]；i 或 j 为 0 或 >=199 的格子在所有墙之外，与 (0,0) 连通\n        if sx <= 0 or sy <= 0 or sx >= 199 or sy >= 199:\n            out.append(0)\n            continue\n        INF = 1 << 30\n        dist = [[INF] * 200 for _ in range(200)]\n        dist[sx][sy] = 0\n        dq = deque([(sx, sy)])\n        ans = -1\n        while dq:\n            i, j = dq.popleft()\n            d0 = dist[i][j]\n            if i == 0 or j == 0 or i == 199 or j == 199:\n                ans = d0\n                break\n            for ni, nj, st in ((i + 1, j, vert[i + 1][j]), (i - 1, j, vert[i][j]),\n                               (i, j + 1, horz[i][j + 1]), (i, j - 1, horz[i][j])):\n                if st == 1:\n                    continue\n                c = 1 if st == 2 else 0\n                if d0 + c < dist[ni][nj]:\n                    dist[ni][nj] = d0 + c\n                    if c:\n                        dq.append((ni, nj))\n                    else:\n                        dq.appendleft((ni, nj))\n        out.append(ans)\n    print("\\n".join(map(str, out)))\n\nmain()\n'
NUMBER=2049
SAMPLE='8 9\n1 1 1 3\n2 1 1 3\n3 1 1 3\n4 1 1 3\n1 1 0 3\n1 2 0 3\n1 3 0 3\n1 4 0 3\n2 1 1\n2 2 1\n2 3 1\n3 1 1\n3 2 1\n3 3 1\n1 2 0\n3 3 0\n4 3 1\n1.5 1.5\n4 0\n1 1 0 1\n1 1 1 1\n2 1 1 1\n1 2 0 1\n1.5 1.7\n-1 -1\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'s.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout.rstrip()+'\n'
def valid(text):
    # 题面：多组；每组首行两个非负整数 M N；M 行墙 "x y d t"（d∈{0,1}，端点坐标在 [1,199]）；
    # N 行门 "x y d"（长 1，开在墙上，端点在 [1,199]）；最后一行两个正浮点数 f1 f2，不在任何墙或门上；
    # 以 "-1 -1" 结束
    if not text.endswith('\n'):return False
    lines=text[:-1].split('\n');i=0
    def ints(t,k):
        v=t.split(' ')
        if len(v)!=k:return None
        for z in v:
            u=z[1:] if z.startswith('-') else z
            if not u.isdigit() or z!=str(int(z)):return None
        return list(map(int,v))
    cases=0
    while True:
        if i>=len(lines):return False
        h=ints(lines[i],2);i+=1
        if h is None:return False
        if h==[-1,-1]:break
        M,N=h
        if M<0 or N<0 or i+M+N+1>len(lines):return False
        V=set();H=set();walls=[]
        for t in lines[i:i+M]:
            w=ints(t,4)
            if w is None:return False
            x,y,d,L=w
            if d not in (0,1) or L<1:return False
            x2,y2=(x,y+L) if d else (x+L,y)
            if not all(1<=c<=199 for c in (x,y,x2,y2)):return False
            walls.append((x,y,x2,y2))
            for k in range(L):(V.add((x,y+k)) if d else H.add((x+k,y)))
        i+=M
        for t in lines[i:i+N]:
            w=ints(t,3)
            if w is None:return False
            x,y,d=w
            if d not in (0,1):return False
            x2,y2=(x,y+1) if d else (x+1,y)
            if not all(1<=c<=199 for c in (x,y,x2,y2)):return False
            if (x,y) not in (V if d else H):return False      # 门开在墙上
        i+=N
        f=lines[i].split(' ');i+=1
        if len(f)!=2:return False
        try:fx,fy=float(f[0]),float(f[1])
        except ValueError:return False
        if not all(c.replace('.','',1).isdigit() for c in f) or not(fx>0 and fy>0):return False
        for x,y,x2,y2 in walls:                                # 门都在墙上，只需查墙
            if x<=fx<=x2 and y<=fy<=y2:return False
        cases+=1
    return i==len(lines)
def extra_cases():
    r=random.Random(20492049)
    def fmt(cs):
        out=[]
        for walls,doors,(fx,fy) in cs:
            out.append(f'{len(walls)} {len(doors)}')
            out+=['%d %d %d %d'%w for w in walls]+['%d %d %d'%dd for dd in doors]+[f'{fx} {fy}']
        return '\n'.join(out)+'\n-1 -1\n'
    def segs_of(walls):
        S=[]
        for x,y,d,t in walls:S+=[(x,y+k,1) if d else (x+k,y,0) for k in range(t)]
        return sorted(set(S))
    def trap(ox,oy):
        # 普通 BFS 先从右侧门摸到出口格并打上标记，真实最优是从上方无门绕过去（答案 0）
        walls=[(ox,oy,1,2),(ox,oy,0,2),(ox+2,oy,1,2),(ox,oy+2,0,1),(ox+1,oy,1,1)]
        return walls,[(ox+1,oy,1)],(ox+0.5,oy+0.5)
    def rand_maze(lo,hi,nw,nd,frac=True,box=False):
        walls=[(lo,lo,1,hi-lo),(hi,lo,1,hi-lo),(lo,lo,0,hi-lo),(lo,hi,0,hi-lo)] if box else []
        for _ in range(nw):
            d=r.randint(0,1);t=r.randint(1,max(1,min(hi-lo,r.choice((3,10,hi-lo)))))
            if d:x=r.randint(lo,hi);y=r.randint(lo,hi-t)
            else:x=r.randint(lo,hi-t);y=r.randint(lo,hi)
            walls.append((x,y,d,t))
        S=segs_of(walls);doors=r.sample(S,min(len(S),nd))
        fx=r.randint(max(lo,1),hi-1)+(r.choice((0.5,0.25,0.75,0.1,0.9)) if frac else 0.5)
        fy=r.randint(max(lo,1),hi-1)+0.5
        return walls,doors,(fx,fy)
    def grid_maze(lo,hi,pdoor):
        # 每条格线都是整墙，按概率开门：门数最少的路径需要真正的最短路
        walls=[(x,lo,1,hi-lo) for x in range(lo,hi+1)]+[(lo,y,0,hi-lo) for y in range(lo,hi+1)]
        S=segs_of(walls);doors=[s for s in S if r.random()<pdoor]
        c=(lo+hi)//2;return walls,doors,(c+0.5,c+0.5)
    def nested(k,c=100,door=True):
        # k 层同心方框，每层开一扇门：答案 k（无门则 -1）
        walls=[];doors=[]
        for t in range(1,k+1):
            a,b=c-t,c+1+t
            walls+=[(a,a,1,b-a),(b,a,1,b-a),(a,a,0,b-a),(a,b,0,b-a)]
            if door:
                side=r.randrange(4);o=r.randrange(b-a)
                doors.append([(a,a+o,1),(b,a+o,1),(a+o,a,0),(a+o,b,0)][side])
        return walls,doors,(c+0.5,c+0.5)
    def spiral(c=100,k=45):
        # 方框套方框，每层下边只留一个无门缺口，路线迂回很长：答案 0
        walls=[];gaps=[]
        for t in range(1,k+1):
            a,b=c-2*t,c+1+2*t
            g=r.randrange(b-a)
            # 下边留缺口 (a+g)-(a+g+1)
            if g>0:walls.append((a,a,0,g))
            if b-a-g-1>0:walls.append((a+g+1,a,0,b-a-g-1))
            walls+=[(a,a,1,b-a),(b,a,1,b-a),(a,b,0,b-a)]
        return walls,[],(c+0.5,c+0.5)
    def checker_box(cx,cy):
        # Nemo 被四面墙封死（无门）：-1
        return [(cx,cy,1,1),(cx+1,cy,1,1),(cx,cy,0,1),(cx,cy+1,0,1)],[],(cx+0.3,cy+0.6)
    cs=[]
    cs.append(fmt([trap(10,10),trap(150,40),trap(1,1),trap(196,196)]))
    cs.append(fmt([checker_box(1,1),checker_box(198,198),checker_box(100,57),([],[],(0.5,0.5)),([],[],(199.5,3.5)),([],[],(250.5,300.5)),([],[],(98.5,1.5))]))
    cs.append(fmt([nested(1),nested(2),nested(5,door=False),nested(3,c=7)]))
    cs.append(fmt([nested(98)]))
    cs.append(fmt([nested(98,door=False)]))
    cs.append(fmt([spiral()]))
    for k in range(10):
        cs.append(fmt([rand_maze(1,r.choice((6,10,20)),r.randint(1,30),r.randint(0,12),box=(t%2==0)) for t in range(12)]+[trap(r.randint(1,190),r.randint(1,190))]))
    for k in range(4):
        cs.append(fmt([rand_maze(1,199,r.randint(200,600),r.randint(0,300),box=(t%2==1)) for t in range(5)]))
    for p in (0.55,0.62,0.75,0.9):
        cs.append(fmt([grid_maze(1,199,p)]))
    cs.append(fmt([grid_maze(1,40,0.4),grid_maze(60,90,0.6),grid_maze(1,199,0.05)]))
    return cs
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1, 40)]+extra_cases()):
  assert valid(x),i
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
