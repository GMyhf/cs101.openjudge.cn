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
    if number == 1230: return gen_1230(r,seed)
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

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1230: Pass-Muraille\n# Fenced code block index: 0\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01230/\n# License: not declared; no license is inferred.\nimport sys\nfor _ in range(int(input())):\n    n,k=map(int,input().split())\n    wall=[]\n    for _ in range(n):\n        x1,y1,x2,y2=map(int,input().split())\n        if x1>x2:\n            x1,x2=x2,x1\n        wall.append((x1,x2))\n    wall.sort(key=lambda x:(x[1],x[0]))\n    condition=[0]*101\n    s=0\n    for t in wall:\n        x1,x2=t[0],t[1]\n        if all(condition[x]<k for x in range(x1,x2+1)):\n            for x in range(x1,x2+1):\n                condition[x]+=1\n        else:\n            s+=1\n    print(s)\n'
def gen_1230(r,seed):
    # 每行内的墙互不重叠（题面：no grid cell belongs to two or more walls）；端点顺序随机；
    # 按种子分档：小规模（便于暴力核对）、满规模 t=10/n=100、k=0、k>=n、窄列密集覆盖等
    def one(n,k,rows,xlo,xhi,lmax):
        occ={};walls=[];tries=0
        while len(walls)<n and tries<200000:
            tries+=1
            y=r.choice(rows);L=r.randint(1,lmax);x1=r.randint(xlo,max(xlo,xhi-L+1));x2=min(xhi,x1+L-1)
            cells=occ.setdefault(y,set())
            if any(x in cells for x in range(x1,x2+1)):continue
            cells.update(range(x1,x2+1))
            walls.append((x2,y,x1,y) if r.random()<.5 else (x1,y,x2,y))
        return f"{len(walls)} {k}\n"+"\n".join(" ".join(map(str,w)) for w in walls)
    cases=[]
    if seed<=15:
        for _ in range(r.randint(1,10)):
            n=r.randint(1,12);k=r.randint(0,4);w=r.randint(3,15)
            cases.append(one(n,k,list(range(r.randint(2,12))),0,w,r.randint(1,8)))
    elif seed<=30:
        for _ in range(r.randint(5,10)):
            n=r.randint(30,100);k=r.choice([0,1,2,3,5,8,r.randint(0,100)])
            cases.append(one(n,k,list(range(101)),0,100,r.choice([5,20,60,101])))
    else:
        for i in range(10):
            if seed==31: k=0
            elif seed==32: k=100
            elif seed==33: k=r.randint(1,3)
            else: k=r.randint(0,30)
            # 窄列区间 + 多行，制造高覆盖度
            w=r.choice([10,30,100]);off=r.randint(0,100-w)
            cases.append(one(100,k,list(range(101)),off,off+w,r.choice([3,10,w+1])))
    return f"{len(cases)}\n"+"\n".join(cases)+"\n"
def valid(text):
    # 题面：首行 t（1<=t<=10）；每组首行 n k（1<=n<=100，0<=k<=100），随后 n 行 x1 y1 x2 y2，
    # 坐标为 0..100 的非负整数；墙平行于 X 轴（y1==y2）；任何格子不属于两堵及以上的墙
    if not text.endswith('\n'): return False
    lines=text[:-1].split('\n')
    def ints(l,k):
        t=l.split(' ')
        if len(t)!=k or not all(x.isdigit() and (x=='0' or x[0]!='0') for x in t): return None
        return list(map(int,t))
    h=ints(lines[0],1)
    if not h or not 1<=h[0]<=10: return False
    p=1
    for _ in range(h[0]):
        if p>=len(lines): return False
        nk=ints(lines[p],2);p+=1
        if not nk: return False
        n,k=nk
        if not (1<=n<=100 and 0<=k<=100) or p+n>len(lines): return False
        used=set()
        for l in lines[p:p+n]:
            v=ints(l,4)
            if not v or max(v)>100: return False
            x1,y1,x2,y2=v
            if y1!=y2: return False
            for x in range(min(x1,x2),max(x1,x2)+1):
                if (x,y1) in used: return False
                used.add((x,y1))
        p+=n
    return p==len(lines)
NUMBER=1230
SAMPLE='2\n3 1\n2 0 4 0\n0 1 1 1\n1 2 2 2\n7 3\n0 0 3 0\n6 1 8 1\n2 3 6 3\n4 4 6 4\n0 5 1 5\n5 6 7 6\n1 7 3 7\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'s.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout.rstrip()+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
