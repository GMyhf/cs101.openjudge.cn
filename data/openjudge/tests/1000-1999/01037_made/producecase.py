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
    if number == 1944:
        n = r.randint(2, 80); all_pairs = [(a, b) for a in range(1, n + 1) for b in range(a + 1, n + 1)]
        pairs = r.sample(all_pairs, r.randint(1, min(200, len(all_pairs))))
        return f"{n} {len(pairs)}\n" + "\n".join(f"{a} {b}" for a, b in pairs) + "\n"
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

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1037: A decorative fence\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01037/\n# License: not declared in source collection; no license is inferred.\nimport sys\n# http://cs101.openjudge.cn/practice/01037/\n#\n# https://blog.csdn.net/u014236804/article/details/38373729\n# POJ1037 A decorative fence by Guo Wei\n\nUP = 0\nDOWN = 1\nMAXN = 25\n\narr = lambda m,n,l : [ [ [0 for k in range(l)] for j in range(n)] for i in range(m) ]\n#m = arr(2,3,4)\n\n# C[i][k][DOWN] 是S(i)中以第k短的木棒打头的DOWN方案数,C[i][k][UP] 是S(i)中以第k短的木棒打头的UP方案数,第k短指i根中第k短\nC = arr(MAXN, MAXN, 2)\n\ndef Init(n: int):\n    C[1][1][UP] = C[1][1][DOWN] = 1\n    for i in range(2, n+1):\n        for k in range(1, i+1):         # 枚举第一根木棒的长度\n            for M in range(k, i):       # 枚举第二根木棒的长度\n                C[i][k][UP] += C[i-1][M][DOWN]\n            for N in range(1, k):       # 枚举第二根木棒的长度\n                C[i][k][DOWN] += C[i-1][N][UP]\n\n# 总方案数是 Sum{ C[n][k][DOWN] + C[n][k][UP] } k = 1.. n;\n\ndef Print(n: int, cc: int):\n    skipped = 0         #已经跳过的方案数\n    seq = [0]*MAXN      #最终要输出的答案\n    used = [False]*MAXN     #木棒是否用过\n\n    for i in range(1, n+1):     # 依次确定每一个位置i的木棒序号\n        oldVal = skipped\n        k = 0\n        No = 0      # k是剩下的木棒里的第No短的,No从1开始算\n        for k in range(1, n+1):     # 枚举位置i的木棒 ，其长度为k\n            oldVal = skipped\n            if used[k]==False:\n                No += 1      # k是剩下的木棒里的第No短的\n                if i == 1:\n                    skipped += C[n][No][UP] + C[n][No][DOWN]\n                else:\n                    if k > seq[i-1] and ( i <=2 or seq[i-2]>seq[i-1]): #合法放置\n                        skipped += C[n-i+1][No][DOWN]\n                    elif k < seq[i-1] and (i<=2 or seq[i-2]<seq[i-1]): #合法放置\n                        skipped += C[n-i+1][No][UP]\n\n                if skipped >= cc:\n                    break\n\n\n        used[k] = True\n        seq[i] = k\n        skipped = oldVal\n\n    print(\' \'.join(map(str, seq[1:n+1])))\n    \'\'\'\n    for i in range(1, n+1):\n        print("{}".format(seq[i]), end=\' \')\n    print()\n    \'\'\'\n\nInit(20);\nfor _ in range(int(input())):\n    n, c = map(int, input().split())\n\n    Print(n,c)\n'
NUMBER=1037
SAMPLE='2\n2 1\n3 3\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout.rstrip()+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1,21)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
