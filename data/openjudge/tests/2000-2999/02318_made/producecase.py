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
        # 原写法玩具 x 与竖直隔板 x 可能重合（落在隔板上，违反题面），改为生成斜隔板并用叉积剔除压线玩具
        probs=[]
        for _ in range(r.randint(1,3)):
            n=r.randint(1,8);m=r.randint(1,15)
            probs.append(_toys_problem(r,n,m,r.choice((0,-50,r.randint(-1000,1000))),r.randint(20,200),r.randint(10,200)))
        return "".join(probs)+"0\n"
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

def _toys_problem(r, n, m, x1, w, h, boundary=True):
    # 生成一个问题：盒子左上 (x1,y1)、右下 (x2,y2)；隔板上下端各取严格递增的 x，保证有序且不相交
    x2 = x1 + max(w, n + 2); y2 = r.randint(-h, h); y1 = y2 + h
    U = sorted(r.sample(range(x1 + 1, x2), n)); L = sorted(r.sample(range(x1 + 1, x2), n))
    def side(k, X, Y):
        u, l = U[k], L[k]
        return (l - u) * (Y - y1) - (y2 - y1) * (X - u)
    toys = []
    corners = [(x1, y1), (x2, y2), (x1, y2), (x2, y1)]
    while len(toys) < m:
        if boundary and corners and r.random() < 0.3:
            X, Y = corners.pop()
        elif boundary and r.random() < 0.1:
            X, Y = r.choice(((x1, r.randint(y2, y1)), (x2, r.randint(y2, y1)), (r.randint(x1, x2), y1), (r.randint(x1, x2), y2)))
        else:
            X, Y = r.randint(x1, x2), r.randint(y2, y1)
        # side>0 表示点在隔板右侧，随隔板编号单调变小；二分找第一个 side<=0 的隔板，再看相邻隔板是否压线
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if side(mid, X, Y) <= 0: hi = mid
            else: lo = mid + 1
        if (lo < n and side(lo, X, Y) == 0) or (lo > 0 and side(lo - 1, X, Y) == 0):
            continue
        toys.append((X, Y))
    return (f"{n} {m} {x1} {y1} {x2} {y2}\n" + "".join(f"{u} {l}\n" for u, l in zip(U, L))
            + "".join(f"{X} {Y}\n" for X, Y in toys))

def _extra():
    # 追加的覆盖组：n=m=1、所有玩具挤在同一格、n=m=5000 满规模、14 个问题、竖直隔板
    r = random.Random(23180)
    out = []
    out.append(_toys_problem(r, 1, 1, 0, 2, 2) + _toys_problem(r, 1, 5, -3, 3, 1) + "0\n")
    # 全在最左格 / 最右格
    x1, y1, x2, y2 = 0, 100, 10000, 0
    U = list(range(5000, 10000, 1000)); L = [u + 500 for u in U]
    toys = [(r.randint(0, 4000), r.randint(0, 100)) for _ in range(20)]
    out.append(f"{len(U)} 20 {x1} {y1} {x2} {y2}\n" + "".join(f"{u} {l}\n" for u, l in zip(U, L)) + "".join(f"{a} {b}\n" for a, b in toys)
               + f"{len(U)} 20 {x1} {y1} {x2} {y2}\n" + "".join(f"{u} {l}\n" for u, l in zip(U, L)) + "".join(f"{10000 - a//10} {b}\n" for a, b in toys) + "0\n")
    out.append(_toys_problem(r, 5000, 5000, -10000, 20000, 20000) + "0\n")
    out.append(_toys_problem(r, 5000, 5000, 0, 5002, 3) + "0\n")
    out.append(_toys_problem(r, 100, 5000, -10000, 20000, 10000) + _toys_problem(r, 5000, 100, -10000, 20000, 10000) + "0\n")
    out.append("".join(_toys_problem(r, r.randint(1, 1500), r.randint(1, 1500), r.randint(-5000, 0), r.randint(1, 10000), r.randint(1, 10000)) for _ in range(14)) + "0\n")
    return out

def valid(text):
    # 1..14 个问题；首行 n m x1 y1 x2 y2（0<n<=5000, 0<m<=5000，左上 (x1,y1)、右下 (x2,y2)）；
    # n 行 Ui Li：隔板端点 (Ui,y1)-(Li,y2)，从左到右有序且互不相交；m 行 Xj Yj：玩具在盒内（含边界）且不落在隔板上；
    # 以单独一行 0 结束。注：题面样例有一行带前导空格（" 5 10"），故行内按空白切分。
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    def ints(ln, k):
        t = ln.split()
        if len(t) != k:
            return None
        for x in t:
            y = x[1:] if x.startswith('-') else x
            if not y.isdigit():
                return None
        return list(map(int, t))
    i = 0; probs = 0
    while True:
        if i >= len(lines):
            return False
        if lines[i] == '0':
            i += 1; break
        h = ints(lines[i], 6); i += 1
        if h is None:
            return False
        n, m, x1, y1, x2, y2 = h
        if not (0 < n <= 5000 and 0 < m <= 5000) or not (x1 < x2 and y1 > y2):
            return False
        if i + n + m > len(lines):
            return False
        parts = []
        for k in range(n):
            p = ints(lines[i + k], 2)
            if p is None or not (x1 <= p[0] <= x2 and x1 <= p[1] <= x2):
                return False
            if parts and not (parts[-1][0] < p[0] and parts[-1][1] < p[1]):
                return False
            parts.append(p)
        i += n
        for k in range(m):
            q = ints(lines[i + k], 2)
            if q is None:
                return False
            X, Y = q
            if not (x1 <= X <= x2 and y2 <= Y <= y1):
                return False
            for u, l in parts:
                # 叉积为 0 即落在隔板所在直线上（盒内即在隔板上）
                if (l - u) * (Y - y1) - (y2 - y1) * (X - u) == 0:
                    return False
        i += m; probs += 1
    return i == len(lines) and 1 <= probs < 15

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2318: TOYS\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/02318/\n# License: not declared; no license is inferred.\ndef compute_bin(toy_x, toy_y, y1, y2, partitions):\n    # 二分查找找到 toy 落在哪个 bin 中\n    left, right = 0, len(partitions)\n    while left < right:\n        mid = (left + right) // 2\n        u, l = partitions[mid]\n        # 计算直线 (u,y1) 到 (l,y2) 在 toy_y 高度的 x 坐标\n        part_x = u + (l - u) * (y1 - toy_y) / (y1 - y2)\n        if toy_x < part_x:\n            right = mid\n        else:\n            left = mid + 1\n    return left\n\ndef main():\n    import sys\n    input_lines = sys.stdin.read().splitlines()\n    idx = 0\n    output = []\n\n    while idx < len(input_lines):\n        line = input_lines[idx].strip()\n        idx += 1\n        if line == \'0\':\n            break\n        if not line:\n            continue\n        n, m, x1, y1, x2, y2 = map(int, line.split())\n        partitions = []\n        for _ in range(n):\n            u, l = map(int, input_lines[idx].split())\n            partitions.append((u, l))\n            idx += 1\n        toys = []\n        for _ in range(m):\n            x, y = map(int, input_lines[idx].split())\n            toys.append((x, y))\n            idx += 1\n\n        bin_counts = [0] * (n + 1)\n        for tx, ty in toys:\n            bin_index = compute_bin(tx, ty, y1, y2, partitions)\n            bin_counts[bin_index] += 1\n\n        for i, count in enumerate(bin_counts):\n            output.append(f"{i}: {count}")\n        output.append("")  # blank line between problems\n\n    print("\\n".join(output).strip())  # strip the last blank line\n\nif __name__ == "__main__":\n    main()\n'
LANGUAGE='Python3'
NUMBER=2318
SAMPLE='5 6 0 10 60 0\n3 1\n4 3\n6 8\n10 10\n15 30\n1 5\n2 1\n2 8\n5 5\n40 10\n7 9\n4 10 0 10 100 0\n20 20\n40 40\n60 60\n80 80\n 5 10\n15 10\n25 10\n35 10\n45 10\n55 10\n65 10\n75 10\n85 10\n95 10\n0\n'
def main():
 with tempfile.TemporaryDirectory() as d:
  d=Path(d);src=d/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE);cmd=[sys.executable,'-I',str(src)]
  if LANGUAGE!='Python3':
   exe=d/'s';subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]
  out=Path('data');out.mkdir(exist_ok=True)
  for p in out.glob('*'):p.unlink()
  cases=([SAMPLE] if SAMPLE or NUMBER in (2698,3225) else [])+([] if NUMBER in (2698,3225) else [generate(NUMBER,s) for s in range(1, 40)]+_extra())
  for i,x in enumerate(cases):
   q=subprocess.run(cmd,input=x,text=True,capture_output=True,timeout=120,check=True);(out/f'{i}.in').write_text(x);(out/f'{i}.out').write_text(q.stdout.rstrip()+'\n')
if __name__=='__main__':main()
