import random,subprocess,sys,tempfile
from pathlib import Path
def fence_counts(n):
    if n == 1:
        return 1
    count = [[[0, 0] for _ in range(n + 1)] for _ in range(n + 1)]
    count[1][1] = [1, 1]
    for size in range(2, n + 1):
        for first in range(1, size + 1):
            count[size][first][0] = sum(count[size - 1][second][1]
                                            for second in range(first, size))
            count[size][first][1] = sum(count[size - 1][second][0]
                                            for second in range(1, first))
    return sum(sum(count[n][first]) for first in range(1, n + 1))
def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    if number == 1258:
        cases = []
        for _ in range(r.randint(1, 3)):
            n = r.randint(3, 18)
            matrix = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    matrix[i][j] = matrix[j][i] = r.randint(1, 100000)
            cases.append(str(n) + "\n" + "\n".join(" ".join(map(str, row)) for row in matrix))
        return "\n".join(cases) + "\n"
    if number == 1661:
        cases = []
        for _ in range(r.randint(1, 4)):
            n = r.randint(1, 12); y = r.randint(2, 200); max_drop = y
            platforms = []
            for height in r.sample(range(1, y), min(n, y - 1)):
                left = r.randint(20, 1000); platforms.append((left, left + r.randint(1, 30), height))
            while len(platforms) < n:
                left = 1100 + len(platforms) * 40; platforms.append((left, left + 10, 1))
            cases.append(f"{n} 0 {y} {max_drop}\n" + "\n".join("%d %d %d" % p for p in platforms))
        return str(len(cases)) + "\n" + "\n".join(cases) + "\n"
    if number == 1664:
        values = [(r.randint(1, 10), r.randint(1, 10)) for _ in range(r.randint(1, 20))]
        return str(len(values)) + "\n" + "\n".join(f"{m} {n}" for m, n in values) + "\n"
    if number == 1703:
        cases = []
        for _ in range(r.randint(1, 4)):
            n = r.randint(3, 80); gangs = [0, 1] + [r.randrange(2) for _ in range(n - 2)]; ops = []
            for _ in range(r.randint(3, 100)):
                a, b = r.sample(range(n), 2)
                if r.random() < .55:
                    while gangs[a] == gangs[b]: b = r.randrange(n)
                    ops.append(f"D {a+1} {b+1}")
                else: ops.append(f"A {a+1} {b+1}")
            cases.append(f"{n} {len(ops)}\n" + "\n".join(ops))
        return str(len(cases)) + "\n" + "\n".join(cases) + "\n"
    if number == 1958:
        return ""
    if number == 2812:
        rows, cols = r.randint(5, 40), r.randint(5, 40); planted_row = r.randint(1, rows)
        points = {(planted_row, col) for col in range(1, cols + 1)}
        target = r.randint(max(3, cols), min(rows * cols, cols + 80))
        while len(points) < target: points.add((r.randint(1, rows), r.randint(1, cols)))
        points = list(points); r.shuffle(points)
        return f"{rows} {cols}\n{len(points)}\n" + "\n".join(f"{x} {y}" for x, y in points) + "\n"
    if number == 1042:
        cases = []
        for _ in range(r.randint(1, 3)):
            n = r.randint(2, 8); h = r.randint(1, 5)
            fish = [r.randint(0, 100) for _ in range(n)]; decreases = [r.randint(0, 20) for _ in range(n)]
            travel = [r.randint(1, min(12, h * 12)) for _ in range(n - 1)]
            cases.append("\n".join((str(n), str(h), " ".join(map(str, fish)),
                                     " ".join(map(str, decreases)), " ".join(map(str, travel)))))
        return "\n".join(cases) + "\n0\n"
    if number == 2226:
        rows, cols = r.randint(1, 18), r.randint(1, 18)
        grid = ["".join(r.choice("***...") for _ in range(cols)) for _ in range(rows)]
        return f"{rows} {cols}\n" + "\n".join(grid) + "\n"
    if number == 1064:
        n, k = r.randint(1, 80), r.randint(1, 500)
        lengths = [r.randint(100, 10_000_000) for _ in range(n)]
        return f"{n} {k}\n" + "\n".join(f"{x//100}.{x%100:02d}" for x in lengths) + "\n"
    if number == 1185:
        rows, cols = r.randint(1, 25), r.randint(1, 10)
        return f"{rows} {cols}\n" + "\n".join("".join(r.choice("PPPH") for _ in range(cols)) for _ in range(rows)) + "\n"
    if number == 2229:
        return f"{r.randint(1, 1_000_000)}\n"
    if number == 2533:
        values = [r.randint(0, 10000) for _ in range(r.randint(1, 200))]
        return f"{len(values)}\n" + " ".join(map(str, values)) + "\n"
    if number == 2659:
        rows, cols, count = r.randint(1, 30), r.randint(1, 30), r.randint(1, 30)
        bombs = [(r.randint(1, rows), r.randint(1, cols), r.randrange(1, 100, 2), r.randint(0, 1))
                 for _ in range(count)]
        return f"{rows} {cols} {count}\n" + "\n".join("%d %d %d %d" % b for b in bombs) + "\n"
    if number == 2946:
        value, count = r.randint(-100, 100), r.randint(1, 30); operations = []
        for _ in range(count): operations.append((r.choice(("plus", "minus", "multiply")), r.randint(-5, 5)))
        return f"{value} {count}\n" + "\n".join(f"{op} {x}" for op, x in operations) + "\n"
    if number == 1037:
        values = []
        for _ in range(r.randint(1, 8)):
            n = r.randint(1, 10); values.append((n, r.randint(1, fence_counts(n))))
        return str(len(values)) + "\n" + "\n".join(f"{n} {c}" for n, c in values) + "\n"
    if number == 1160:
        villages = sorted(r.sample(range(1, 10001), r.randint(1, 100)))
        return f"{len(villages)} {r.randint(1, min(30, len(villages)))}\n" + " ".join(map(str, villages)) + "\n"
    if number == 1944: return gen1944(r, seed)
    if number == 2385:
        total, walks = r.randint(1, 200), r.randint(1, 30)
        return f"{total} {walks}\n" + "\n".join(str(r.randint(1, 2)) for _ in range(total)) + "\n"
    if number == 2711:
        heights = [r.randint(130, 230) for _ in range(r.randint(2, 100))]
        return f"{len(heights)}\n" + " ".join(map(str, heights)) + "\n"
    if number == 2797:
        words = set(); target = r.randint(2, 60)
        while len(words) < target:
            words.add("".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1, 20))))
        words = sorted(words); r.shuffle(words)
        return "\n".join(words) + "\n"
    raise KeyError(number)

def valid(text):
    """题面约束：首行 N P（1<=N<=1000，1<=P<=10000）；随后 P 行，每行两个 1..N 的谷仓编号，
    表示需要通信的一对（两个不同谷仓）；“No pair is duplicated”——按无序对判重。"""
    if not text.endswith("\n"):return False
    lines=text[:-1].split("\n")
    def ints(ln):
        t=ln.split(" ")
        if not all(x.isdigit() and str(int(x))==x for x in t):return None
        return list(map(int,t))
    h=ints(lines[0])
    if not h or len(h)!=2:return False
    n,p=h
    if not(1<=n<=1000 and 1<=p<=10000) or len(lines)!=p+1:return False
    seen=set()
    for ln in lines[1:]:
        v=ints(ln)
        if not v or len(v)!=2:return False
        a,b=v
        if not(1<=a<=n and 1<=b<=n) or a==b:return False
        k=(min(a,b),max(a,b))
        if k in seen:return False
        seen.add(k)
    return True

def gen1944(r, seed):
    # 规模说明：N=1000 时内嵌参考解是 O(N*P)，P 取到 6000 左右（约 4s，Python 单组时限 10s 的一半以内）；
    # P=10000 满规模放在 N≈150..200 的组里。
    def arcs_pairs(n,P,k):
        # 在环上取 k 段弧（可跨过 N-1 接口、可重叠），每对谷仓都落在同一段弧内
        arcs=[(r.randint(1,n),r.randint(1,max(1,min(n-1,r.choice([n//(2*k)+1,n//k,n//2,n-1]))))) for _ in range(k)]
        got=set();tries=0
        while len(got)<P and tries<P*30:
            tries+=1;st,ln=r.choice(arcs)
            if ln<1:continue
            i,j=r.sample(range(ln+1),2)
            a=(st-1+i)%n+1;b=(st-1+j)%n+1
            got.add((min(a,b),max(a,b)))
        return list(got)
    def rand_pairs(n,P):
        got=set()
        while len(got)<P:
            a,b=r.sample(range(1,n+1),2);got.add((min(a,b),max(a,b)))
        return list(got)
    if seed==1:n,pairs=2,[(1,2)]
    elif seed==2:n,pairs=3,[(1,3)]
    elif seed==3:n,pairs=1000,[(1,1000)]
    elif seed==4:n,pairs=1000,[(1,500)]
    elif seed==5:n,pairs=1000,[(1,501),(250,750)]
    elif seed<=16:
        n=r.randint(4,12);P=r.randint(1,min(15,n*(n-1)//2))
        pairs=arcs_pairs(n,P,r.randint(1,3)) if seed%3 else rand_pairs(n,P)
    elif seed<=26:
        n=r.randint(50,400);P=r.randint(100,min(3000,n*(n-1)//2))
        pairs=arcs_pairs(n,P,r.randint(1,6))
    elif seed<=32:
        n=1000;pairs=arcs_pairs(n,r.randint(4500,6000),r.randint(2,8))
    elif seed<=35:
        n=r.randint(150,200);pairs=arcs_pairs(n,10000,r.randint(1,3))
        if len(pairs)<10000:pairs=rand_pairs(n,10000)
    elif seed<=37:
        n=1000;pairs=rand_pairs(n,6000)
    else:
        n=r.randint(150,200);pairs=rand_pairs(n,10000)
    r.shuffle(pairs)
    pairs=[(b,a) if r.random()<.5 else (a,b) for a,b in pairs]
    return f"{n} {len(pairs)}\n"+"\n".join(f"{a} {b}" for a,b in pairs)+"\n"

REFERENCE="# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 1944: Fiber Communications\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01944/\n# License: not declared in source collection; no license is inferred.\nimport sys\n# https://www.cnblogs.com/lightspeedsmallson/p/4785834.html\nN, P = map(int, input().split())\nnode_one = []\n\nfor i in range(P):\n    Q1, Q2 = map(int, input().split())\n    node_one.append({'start': min(Q1, Q2), 'end': max(Q1, Q2)})\n\nnode_one.sort(key=lambda x: (x['start'], x['end']))\n\nINF = float('inf')\nans = INF\n\nfor i in range(1, N + 1):\n    to = [0] * (N + 1)\n\n    for j in range(P):\n        if node_one[j]['end'] >= i + 1 and node_one[j]['start'] <= i:\n            to[1] = max(to[1], node_one[j]['start'])\n            to[node_one[j]['end']] = N + 1\n        else:\n            to[node_one[j]['start']] = max(to[node_one[j]['start']], node_one[j]['end'])\n\n    duandian = 0\n    result = 0\n\n    for j in range(1, N + 1):\n        if to[j] == 0:\n            continue\n\n        if to[j] > duandian:\n            if j >= duandian:\n                result += (to[j] - j)\n            else:\n                result += (to[j] - duandian)\n\n            duandian = to[j]\n\n    ans = min(ans, result)\n\nprint(ans)\n"
NUMBER=1944
SAMPLE='5 2\n1 3\n4 5\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout.rstrip()+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
