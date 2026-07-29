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

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1160: Post Office\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01160/\n# License: not declared in source collection; no license is inferred.\nimport sys\n# https://blog.csdn.net/u011262722/article/details/9298011\n# uses dynamic programming to efficiently solve the problem of partitioning\n# an array into p subarrays with minimum cost.\n#\n# dp是前i个村庄建j个邮局，dis是在i和j村庄间建邮局的最小距离\n\'\'\'\n【题目大意】：用数轴描述一条高速公路，有V个村庄，每一个村庄坐落在数轴的某个点上，需要选择P个村庄在其中建立邮局，\n要求每个村庄到最近邮局的距离和最小。\n【题目分析】：经典DP\n1、考虑在V个村庄中只建立【一个】邮局的情况，显然可以知道，将邮局建立在中间的那个村庄即可。\n也就是在a到b间建立一个邮局，若使消耗最小，则应该将邮局建立在（a+b)/2这个村庄上。\n2、下面考虑建立【多个】邮局的问题，可以这样将该问题拆分为若干子问题，在前i个村庄中建立j个邮局的最短距离，\n是在前【k】个村庄中建立【j-1】个邮局的最短距离与 在【k+1】到第i个邮局建立【一个】邮局的最短距离的和。\n而建立一个邮局我们在上面已经求出。\n\n3、状态表示，由上面的讨论，可以开两个数组\ndp[i][j]:在前i个村庄中建立j个邮局的最小耗费\ndis[i][j]:在第i个村庄到第j个村庄中建立1个邮局的最小耗费\n那么就有转移方程：dp[i][j] = min(dp[i][j],dp[k][j-1]+dis[k+1][i])\nDP的边界状态即为dp[i][1] = dis[1][i]; 所要求的结果即为dp[village_num][post office_num];\n\n4、然后就说说求sum数组的优化问题，可以假定有6个村庄，村庄的坐标已知分别为p1,p2,p3,p4,p5,p6;\n那么，如果要求sum[1][4]的话邮局需要建立在2或者3处,放在2处的消耗为p4-p2+p3-p2+p2-p1=p4-p2+p3-p1\n放在3处的结果为p4-p3+p3-p2+p3-p1=p4+p3-p2-p1，可见，将邮局建在2处或3处是一样的。\n现在接着求sum[1][5],现在处于中点的村庄是3，那么1-4到3的距离和刚才已经求出了，即为sum[1][4],\n所以只需再加上5到3的距离即可。同样，求sum[1][6]的时候也可以用sum[1][5]加上6到中点的距离。\n所以有递推关系：sum[i][j] = sum[i][j-1] + p[j] -p[(i+j)/2]\n\n\'\'\'\nv, p = map(int, input().split())\nx = [0] + list(map(int, input().split()))\ndis = [[0] * (v + 1) for _ in range(v + 1)]\ndp = [[0] * (v + 1) for _ in range(v + 1)]\nfor i in range(1, v + 1):\n    for j in range(i + 1, v + 1):\n        dis[i][j] = dis[i][j - 1] + x[j] - x[(i + j) // 2]\nfor i in range(1, v + 1):\n    dp[i][i] = 0\n    dp[i][1] = dis[1][i]\nfor j in range(2, p + 1):\n    for i in range(j + 1, v + 1):\n        dp[i][j] = float("inf")\n        for k in range(j - 1, i):\n            dp[i][j] = min(dp[i][j], dp[k][j - 1] + dis[k + 1][i])\nprint(dp[v][p])\n'
NUMBER=1160
SAMPLE='10 5\n1 2 3 6 7 9 11 22 44 50\n'
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
