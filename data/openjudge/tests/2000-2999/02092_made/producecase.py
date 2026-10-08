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
            while True:
                n,m=r.randint(2,20),r.randint(2,20)            # 题面：2<=N,M<=500
                rows=[r.sample(range(1,61),m) for _ in range(n)]   # 每张榜内编号互不相同
                counts={}
                for row in rows:
                    for player in row: counts[player]=counts.get(player,0)+1
                best=max(counts.values())
                # 题面保证：恰好一个最佳选手，且至少有一个次佳选手
                if sum(value==best for value in counts.values())!=1: continue
                if all(value==best for value in counts.values()): continue
                break
            cases.append(f"{n} {m}\n"+"\n".join(" ".join(map(str,row)) for row in rows))
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

REFERENCE="# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 2092: Grandpa is Famous\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/02092/\n# License: not declared; no license is inferred.\nimport sys\nwhile True:\n    n, m = map(int, input().split())\n    if n == 0 and m == 0:\n        break\n\n    count = [0] * 10001\n    for _ in range(n):\n        for player in map(int, input().split()):\n            count[player] += 1\n\n    max_count = max(count)\n    second_max_count = max(x for x in count if x != max_count)\n\n    for player, player_count in enumerate(count):\n        if player_count == second_max_count:\n            print(player, end=' ')\n    print()\n"
NUMBER=2092
SAMPLE='4 5\n20 33 25 32 99\n32 86 99 25 10\n20 99 10 33 86\n19 33 74 99 32\n3 6\n2 34 67 36 79 93\n100 38 21 76 91 85\n32 23 85 31 88 1\n0 0\n'
def valid(text):
    """题面契约：多组数据，每组首行 N M（2<=N,M<=500），随后 N 行各 M 个互不相同的 1..10000 编号，
    单空格分隔；以 "0 0" 结束。保证恰有一个最佳选手且至少有一个次佳选手。"""
    if not text.endswith('\n') or '\r' in text:
        return False
    lines = text[:-1].split('\n')
    i = 0
    cases = 0
    while True:
        if i >= len(lines):
            return False
        head = lines[i].split(' ')
        if len(head) != 2 or not all(t.isdigit() for t in head):
            return False
        n, m = map(int, head)
        i += 1
        if n == 0 and m == 0:
            return i == len(lines) and cases >= 1
        if not (2 <= n <= 500 and 2 <= m <= 500):
            return False
        if i + n > len(lines):
            return False
        counts = {}
        for row in lines[i:i + n]:
            toks = row.split(' ')
            if len(toks) != m or not all(t.isdigit() and t[0] != '0' for t in toks):
                return False
            vals = list(map(int, toks))
            if len(set(vals)) != m or not all(1 <= v <= 10000 for v in vals):
                return False
            for v in vals:
                counts[v] = counts.get(v, 0) + 1
        i += n
        best = max(counts.values())
        if sum(c == best for c in counts.values()) != 1 or len(counts) < 2:
            return False
        cases += 1


def _case2092(r, n, m, pool, best=None, fixed=()):
    """随机生成一组：best 每榜都出现（保证唯一最佳），其余从 pool 抽；fixed 里的编号尽量放进去。"""
    pool = list(pool)
    # 每个非最佳选手至少要缺席一榜，才可能「恰好一个最佳」：池子不够大就扩
    while n * (len(pool) - m) < len(pool) - 1 + n and len(pool) < 10000:
        pool.append(max(pool) + 1) if max(pool) < 10000 else pool.append(min(pool) - 1)
    while True:
        b = best if best is not None else r.choice(pool)
        others = [p for p in pool if p != b]
        rows = []
        for k in range(n):
            row = r.sample(others, m - 1)
            if fixed and k % 3 == 0:
                f = fixed[k // 3 % len(fixed)]
                if f != b and f not in row:
                    row[r.randrange(m - 1)] = f
            row.append(b)
            r.shuffle(row)
            rows.append(row)
        counts = {}
        for row in rows:
            for p in row:
                counts[p] = counts.get(p, 0) + 1
        # 其他人若也每榜都在（与最佳并列），在某一榜里把他换成出现最少的人
        for _ in range(4 * n):
            ties = sorted(p for p, c in counts.items() if c == n and p != b)
            if not ties:
                break
            p = ties[0]; k = r.randrange(n); row = rows[k]
            q = min((x for x in others if x not in row), key=lambda x: (counts.get(x, 0), x))
            row[row.index(p)] = q
            counts[p] -= 1; counts[q] = counts.get(q, 0) + 1
        top = max(counts.values())
        if sum(c == top for c in counts.values()) == 1:
            return rows


def _fmt2092(cases):
    return "".join(f"{len(rows)} {len(rows[0])}\n" + "".join(" ".join(map(str, row)) + "\n" for row in rows)
                   for rows in cases) + "0 0\n"


def gen2092(seed):
    r = random.Random(2092_000 + seed)
    if seed == 1:      # 最小规模 N=M=2，编号取到两端 1 与 10000
        return _fmt2092([[[1, 10000], [10000, 2]], [[5, 6], [6, 7]], [[10000, 1], [1, 9999]]])
    if seed == 2:      # 次佳并列极多：除最佳外每人恰好出现一次（9900 人并列次佳）
        ids = list(range(1, 10001)); r.shuffle(ids)
        b = ids.pop(); rows = []
        for k in range(100):
            row = ids[k * 99:(k + 1) * 99] + [b]; r.shuffle(row); rows.append(row)
        return _fmt2092([rows])
    if seed == 3:      # 满规模 N=M=500，编号 1..999（控制文件 ≤1MB），含 1
        return _fmt2092([_case2092(r, 500, 500, range(1, 1000), fixed=(1,))])
    if seed == 4:      # N=500,M=300，编号覆盖到 10000
        return _fmt2092([_case2092(r, 500, 300, range(1, 10001), best=10000)])
    if seed == 5:      # N=300,M=500，编号 1..10000，次佳里放 10000
        return _fmt2092([_case2092(r, 300, 500, range(1, 10001), fixed=(10000,))])
    if seed == 6:      # 最佳编号为 1，次佳为 10000（越界、下标 0 的写法会出错）
        rows = [[1, 10000] + r.sample(range(2, 10000), 3) for _ in range(9)] + [[1] + r.sample(range(2, 10000), 4)]
        return _fmt2092([rows])
    if seed == 7:      # N 小 M 大：最佳 10 次，次佳只有寥寥几次
        rows = [_case2092(r, 10, 500, range(1, 10001))]
        return _fmt2092(rows)
    if seed == 8:      # 小池子：人人都出现很多次，次数差 1 的紧密竞争
        return _fmt2092([_case2092(r, 50, 9, range(1, 11)) for _ in range(30)])
    if seed <= 20:     # 多组中小规模混合
        cases = []
        for _ in range(r.randint(5, 40)):
            n, m = r.randint(2, 30), r.randint(2, 30)
            lo = r.choice([1, 1, 5000, 9900])
            hi = min(10000, lo + r.choice([m + 1, 2 * m, 100, 10000]))
            cases.append(_case2092(r, n, m, range(lo, hi + 1)))
        return _fmt2092(cases)
    if seed <= 30:     # 中等规模多组
        cases = []
        for _ in range(r.randint(2, 5)):
            n, m = r.randint(50, 150), r.randint(50, 150)
            cases.append(_case2092(r, n, m, range(1, r.choice([m + 2, 2 * m, 1000, 10001]))))
        return _fmt2092(cases)
    # 大规模单组/双组
    n, m = r.randint(300, 500), r.randint(150, 300)
    return _fmt2092([_case2092(r, n, m, range(1, r.choice([m + 3, 1000, 10001])))])

def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'s.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout.rstrip()+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[gen2092(s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
