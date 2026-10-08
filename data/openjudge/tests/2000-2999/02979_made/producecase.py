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
        return gen_2979(r, seed)
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

def jury_solve(n, m, P, D):
    """精确背包 DP：返回 (控方总分, 辩方总分, 成员列表, 最优方案数)。最优：|D-P| 最小，其次 P+D 最大。"""
    off = 20 * m; W = 2 * off + 1
    dp = [[-1] * W for _ in range(m + 1)]; cn = [[0] * W for _ in range(m + 1)]
    dp[0][off] = 0; cn[0][off] = 1; snaps = []
    for i in range(n):
        s = P[i] + D[i]; t = P[i] - D[i]
        snaps.append([row[:] for row in dp])
        for j in range(min(i + 1, m), 0, -1):
            prev = dp[j - 1]; pc = cn[j - 1]; cur = dp[j]; cc = cn[j]
            r = 20 * (j - 1)
            for k in range(off - r, off + r + 1):
                v = prev[k]
                if v >= 0:
                    nv = v + s; kk = k + t
                    if nv > cur[kk]: cur[kk] = nv; cc[kk] = pc[k]
                    elif nv == cur[kk]: cc[kk] += pc[k]
    for diff in range(off + 1):
        ks = [k for k in {off + diff, off - diff} if dp[m][k] >= 0]
        if ks:
            best = max(dp[m][k] for k in ks); ks = [k for k in ks if dp[m][k] == best]
            total = sum(cn[m][k] for k in ks); break
    k = ks[0]; j = m; val = best; members = []
    for i in range(n - 1, -1, -1):
        if j == 0: break
        before = snaps[i]; s = P[i] + D[i]; t = P[i] - D[i]
        if before[j][k] == val: continue
        members.append(i + 1); j -= 1; k -= t; val -= s
    members.reverse()
    sp = sum(P[i - 1] for i in members); sd = sum(D[i - 1] for i in members)
    return sp, sd, members, total

# 经典「f[j][k] + 沿 path 查重」写法（旧参考解即此写法）会答错的组：用精确 DP 与它对拍随机小数据筛出，
# 均已确认最优方案唯一。
HARD_2979 = [[11, 7, [3, 18, 5, 4, 7, 1, 1, 1, 9, 11, 6], [2, 10, 20, 7, 12, 17, 19, 1, 10, 5, 13]], [13, 6, [16, 7, 8, 14, 9, 8, 6, 17, 7, 17, 5, 6, 0], [5, 6, 16, 12, 16, 6, 1, 7, 16, 0, 16, 5, 20]], [9, 7, [4, 0, 2, 1, 6, 2, 2, 3, 6], [1, 8, 4, 4, 3, 1, 4, 3, 7]], [19, 7, [14, 0, 16, 7, 18, 18, 17, 17, 7, 11, 17, 4, 3, 19, 12, 7, 3, 3, 12], [19, 9, 18, 2, 7, 8, 3, 0, 14, 20, 1, 0, 4, 18, 12, 9, 14, 2, 17]], [10, 7, [1, 3, 18, 20, 10, 6, 10, 6, 16, 10], [11, 10, 13, 20, 8, 20, 6, 20, 13, 2]], [11, 9, [6, 7, 3, 3, 3, 6, 8, 5, 6, 0, 1], [7, 6, 8, 4, 6, 2, 0, 2, 8, 3, 5]], [27, 10, [4, 3, 5, 5, 5, 8, 7, 4, 5, 5, 0, 1, 4, 8, 1, 3, 7, 3, 7, 2, 8, 1, 8, 8, 6, 0, 3], [5, 8, 1, 6, 0, 6, 0, 6, 0, 6, 6, 0, 2, 5, 3, 1, 0, 3, 4, 5, 0, 6, 7, 3, 6, 1, 7]], [12, 10, [14, 5, 0, 15, 1, 15, 18, 9, 1, 2, 18, 10], [10, 9, 14, 1, 15, 0, 8, 8, 13, 6, 16, 20]], [12, 6, [2, 5, 1, 3, 6, 8, 2, 7, 5, 1, 0, 4], [1, 3, 3, 5, 1, 5, 7, 7, 8, 5, 2, 0]], [12, 8, [4, 2, 8, 2, 0, 1, 6, 8, 2, 4, 6, 4], [2, 2, 7, 1, 8, 0, 4, 1, 6, 4, 8, 3]], [30, 7, [18, 14, 17, 5, 1, 19, 4, 12, 20, 17, 17, 17, 14, 5, 16, 7, 11, 2, 5, 13, 10, 1, 16, 11, 6, 15, 9, 8, 12, 2], [3, 6, 15, 8, 2, 14, 14, 3, 13, 2, 18, 14, 4, 10, 13, 9, 18, 3, 4, 5, 7, 3, 8, 19, 18, 17, 20, 6, 19, 19]], [11, 7, [7, 6, 3, 5, 10, 0, 20, 17, 20, 12, 17], [18, 8, 16, 8, 7, 7, 8, 20, 17, 16, 4]], [12, 10, [3, 2, 7, 2, 7, 7, 4, 2, 1, 6, 3, 0], [1, 5, 2, 4, 0, 6, 1, 8, 5, 1, 0, 7]], [12, 9, [7, 8, 8, 14, 0, 20, 20, 5, 12, 19, 13, 6], [15, 3, 0, 4, 6, 18, 8, 7, 18, 12, 7, 17]], [10, 7, [7, 5, 16, 3, 13, 17, 2, 1, 13, 4], [2, 11, 17, 6, 4, 2, 17, 6, 5, 8]], [11, 7, [0, 6, 4, 3, 19, 20, 13, 8, 17, 5, 0], [14, 15, 16, 8, 2, 15, 5, 10, 17, 20, 20]], [21, 7, [3, 19, 8, 15, 15, 14, 2, 2, 7, 2, 13, 17, 9, 20, 5, 4, 20, 16, 13, 6, 15], [13, 14, 15, 12, 11, 2, 13, 1, 19, 13, 14, 4, 19, 11, 14, 14, 2, 14, 8, 6, 20]], [13, 10, [5, 4, 2, 4, 12, 20, 3, 7, 4, 17, 13, 19, 13], [0, 16, 0, 19, 16, 8, 10, 14, 17, 6, 3, 13, 20]], [24, 10, [0, 20, 14, 5, 4, 1, 16, 5, 14, 20, 3, 20, 17, 2, 15, 19, 0, 11, 3, 19, 9, 20, 9, 1], [0, 11, 8, 0, 17, 10, 13, 16, 0, 0, 13, 0, 18, 13, 7, 5, 8, 2, 14, 7, 15, 20, 4, 10]], [11, 9, [1, 4, 8, 4, 6, 8, 6, 0, 6, 4, 5], [5, 4, 6, 5, 4, 1, 3, 0, 6, 7, 7]], [15, 9, [19, 14, 18, 17, 5, 6, 11, 0, 3, 2, 1, 2, 14, 12, 20], [20, 4, 10, 5, 13, 0, 19, 15, 3, 12, 15, 19, 20, 11, 5]], [16, 10, [3, 1, 15, 19, 8, 18, 9, 5, 3, 20, 12, 14, 14, 2, 6, 8], [1, 8, 12, 7, 15, 11, 10, 4, 13, 9, 16, 5, 6, 12, 12, 3]]]
def gen_2979(r, seed):
    # 题面：1<=n<=200，1<=m<=20，m<=n，分值 0..20；组间空行分隔，以 0 0 结束。
    # 题面没说并列时输出哪一组，按 token 比对时并列会让正确程序 WA，所以每组都用计数 DP 确认最优方案唯一。
    # 覆盖：n=1、n=m（全选）、m=1、n=200/m=20 满规模（含单文件 3 组满规模）、控方或辩方一边倒（最优差不为 0、
    # 符号要对）、多组编号、能卡掉经典 path 查重写法的组。
    def scores(n, kind):
        if kind == "sp": return [r.randint(12, 20) for _ in range(n)], [r.randint(0, 8) for _ in range(n)]
        if kind == "sd": return [r.randint(0, 8) for _ in range(n)], [r.randint(12, 20) for _ in range(n)]
        if kind == "corr":
            P = [r.randint(0, 20) for _ in range(n)]; return P, [min(20, max(0, x + r.randint(-6, 6))) for x in P]
        if kind == "small": return [r.randint(0, 6) for _ in range(n)], [r.randint(0, 6) for _ in range(n)]
        return [r.randint(0, 20) for _ in range(n)], [r.randint(0, 20) for _ in range(n)]
    def group(n, m, kind="u"):
        while True:
            P, D = scores(n, kind)
            if jury_solve(n, m, P, D)[3] == 1: return n, m, P, D
    kinds = ("u", "u", "sp", "sd", "corr", "small")
    def small(k, hi=30):
        out = []
        for _ in range(k):
            n = r.randint(1, hi); out.append(group(n, r.randint(1, min(n, 20)), r.choice(kinds) if n <= 40 else "u"))
        return out
    if seed == 1: gs = [group(1, 1)]
    elif seed == 2: gs = [group(20, 20), group(1, 1), group(5, 5, "sp"), group(20, 20, "sd")]
    elif seed == 3: gs = [group(200, 1)]
    elif seed in (4, 5): gs = [group(200, 20)]
    elif seed == 6: gs = [group(200, 20, "sp")]
    elif seed == 7: gs = [group(200, 20, "sd")]
    elif seed == 8: gs = [group(200, r.randint(2, 19), "corr")]
    elif seed == 9: gs = [group(200, 10)]
    elif seed == 10: gs = [group(200, 20) for _ in range(3)]
    elif seed <= 25: gs = small(r.randint(2, 8))
    elif seed <= 30: gs = [group(n, r.randint(1, 20), r.choice(("u", "corr", "sp", "sd"))) for n in [r.randint(30, 120) for _ in range(r.randint(1, 3))]]
    elif seed == 31: gs = small(30, 12)
    elif seed == 32: gs = [tuple(x) for x in HARD_2979[:11]]
    elif seed == 33: gs = [tuple(x) for x in HARD_2979[11:]]
    else:
        n = r.randint(20, 200); gs = [group(n, r.randint(1, 20), r.choice(("u", "corr")))] + small(r.randint(0, 3))
    return "\n\n".join(f"{n} {m}\n" + "\n".join(f"{a} {b}" for a, b in zip(P, D)) for n, m, P, D in gs) + "\n\n0 0\n"

def valid(text):
    """题面 02979：多组数据；每组首行 n m（1<=n<=200，1<=m<=20，m<=n），随后恰 n 行「控方分 辩方分」，分值 0..20；
    两组有效数据之间恰一个空行；最后一行为 0 0（样例里 0 0 前也有一个空行，这里允许有或没有）。"""
    import re
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n"); i = 0; groups = 0
    while True:
        if i >= len(lines): return False
        mt = re.fullmatch(r"(0|[1-9]\d*) (0|[1-9]\d*)", lines[i])
        if not mt: return False
        n, m = int(mt.group(1)), int(mt.group(2))
        if n == 0 and m == 0: return i == len(lines) - 1 and groups >= 1
        if not (1 <= n <= 200 and 1 <= m <= 20 and m <= n): return False
        if i + 1 + n > len(lines): return False
        for line in lines[i + 1:i + 1 + n]:
            ms = re.fullmatch(r"(0|[1-9]\d*) (0|[1-9]\d*)", line)
            if not ms or int(ms.group(1)) > 20 or int(ms.group(2)) > 20: return False
        groups += 1; i += 1 + n
        if i < len(lines) and lines[i] == "": i += 1
        elif not (i < len(lines) and lines[i] == "0 0"): return False

REFERENCE='# 陪审团的人选（POJ 1015）参考解：按候选人逐个做 0/1 背包，\n# dp[j][k] = 选 j 人、控辩差偏移为 k 时的最大控辩和；保存每步快照用于回溯成员。\n# 旧参考解是经典的「f[j][k] + 沿 path 查重」写法，它只保留每个状态的一条路径，\n# 在少数数据上会漏掉最优方案（不满足最优子结构），故换成这个精确解。\nimport sys\ndef solve(n, m, P, D):\n    off = 20 * m; W = 2 * off + 1\n    dp = [[-1] * W for _ in range(m + 1)]; dp[0][off] = 0; snaps = []\n    for i in range(n):\n        s = P[i] + D[i]; t = P[i] - D[i]\n        snaps.append([row[:] for row in dp])\n        for j in range(min(i + 1, m), 0, -1):\n            prev = dp[j - 1]; cur = dp[j]; r = 20 * (j - 1)\n            for k in range(off - r, off + r + 1):\n                v = prev[k]\n                if v >= 0 and v + s > cur[k + t]: cur[k + t] = v + s\n    for diff in range(off + 1):\n        ks = [k for k in sorted({off + diff, off - diff}) if dp[m][k] >= 0]\n        if ks:\n            k = max(ks, key=lambda x: dp[m][x]); break\n    j = m; val = dp[m][k]; members = []\n    for i in range(n - 1, -1, -1):\n        if j == 0: break\n        if snaps[i][j][k] == val: continue\n        members.append(i + 1); j -= 1; k -= P[i] - D[i]; val -= P[i] + D[i]\n    members.reverse(); return members\ndef main():\n    data = list(map(int, sys.stdin.read().split())); p = 0; case = 0; out = []\n    while True:\n        n, m = data[p], data[p + 1]; p += 2\n        if n == 0 and m == 0: break\n        P = data[p:p + 2 * n:2]; D = data[p + 1:p + 2 * n:2]; p += 2 * n; case += 1\n        mem = solve(n, m, P, D)\n        out.append(f"Jury #{case}")\n        out.append(f"Best jury has value {sum(P[i-1] for i in mem)} for prosecution and value {sum(D[i-1] for i in mem)} for defence:")\n        out.append("".join(f" {i}" for i in mem)); out.append("")\n    print("\\n".join(out))\nmain()\n'
NUMBER=2979
SAMPLE='4 2\n1 2\n2 3\n4 1\n6 2\n\n0 0\n'
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
