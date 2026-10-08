import random, subprocess, sys, tempfile
from pathlib import Path
def g1328(r):
    blocks = []
    for _ in range(r.randint(1, 3)):
        n, d = r.randint(1, 25), r.randint(1, 30)
        points = [f"{r.randint(-80,80)} {r.randint(0,d + (5 if r.random()<.15 else 0))}" for _ in range(n)]
        blocks.append(f"{n} {d}\n" + "\n".join(points) + "\n\n")
    return "".join(blocks) + "0 0\n"


def valid(text):
    """题面契约：多组，每组 n d（1<=n<=1000，d 为整数），随后 n 个整数坐标的岛屿，岛在海一侧（x 轴上方，y>0）；
    以一对 0 结束。"""
    try:
        t = [int(x) for x in text.split()]
    except ValueError:
        return False
    i, cases = 0, 0
    while True:
        if i + 2 > len(t):
            return False
        n, d = t[i], t[i + 1]; i += 2
        if n == 0 and d == 0:
            return i == len(t) and cases >= 1
        if not 1 <= n <= 1000 or i + 2 * n > len(t):
            return False
        if any(t[i + 2 * j + 1] <= 0 for j in range(n)):
            return False
        i += 2 * n
        cases += 1


def _blk1328(n, d, pts):
    return f"{n} {d}\n" + "".join(f"{x} {y}\n" for x, y in pts) + "\n"


def _touch1328(r, k, d=5):
    """勾股数构造端点恰好相接的区间链：(x,3) 覆盖 [x-4,x+4]，相邻岛间距 8。"""
    base = r.randint(-1000, 1000)
    return [(base + 8 * i, 3) for i in range(k)]


def g1328_v2(r, seed):
    blocks = []
    if seed == 1:      # 边界：n=1；d=0 / d<0 无解；y==d 恰好够；端点恰相接；嵌套区间
        blocks.append(_blk1328(1, 1, [(0, 1)]))
        blocks.append(_blk1328(1, 0, [(5, 1)]))
        blocks.append(_blk1328(2, -3, [(0, 1), (2, 2)]))
        blocks.append(_blk1328(3, 5, [(0, 5), (10, 5), (20, 5)]))
        blocks.append(_blk1328(2, 5, [(0, 3), (8, 3)]))
        blocks.append(_blk1328(2, 5, [(0, 4), (1, 1)]))       # 小区间套在大区间里：按左端点贪心不更新右端会错
        blocks.append(_blk1328(3, 2, [(1, 2), (1, 3), (0, 1)]))
        blocks.append(_blk1328(4, 10, [(0, 1), (0, 1), (100, 10), (100, 10)]))
    elif seed <= 4:    # 端点相接的长链（问 < 还是 <=）
        k = 1000; pts = _touch1328(r, k); r.shuffle(pts)
        blocks.append(_blk1328(k, 5, pts))
        pts = _touch1328(r, 300); r.shuffle(pts); blocks.append(_blk1328(300, 5, pts))
    elif seed <= 20:   # 随机中小规模多组，含无解
        for _ in range(r.randint(2, 8)):
            n = r.randint(1, 60); d = r.randint(1, 50)
            pts = [(r.randint(-200, 200), r.randint(1, d)) for _ in range(n)]
            if r.random() < .25: pts[r.randrange(n)] = (r.randint(-200, 200), d + r.randint(1, 5))
            blocks.append(_blk1328(n, d, pts))
    elif seed <= 32:   # n=1000 满规模，坐标大
        for _ in range(r.randint(1, 3)):
            d = r.choice([1, 10, 1000, 30000, r.randint(1, 50000)])
            span = r.choice([10 ** 3, 10 ** 5, 10 ** 6])
            pts = [(r.randint(-span, span), r.randint(1, d)) for _ in range(1000)]
            if r.random() < .15: pts[r.randrange(1000)] = (r.randint(-span, span), d + 1)
            blocks.append(_blk1328(1000, d, pts))
    else:              # 很多组满规模（卡每组重复初始化/低效读入）
        for _ in range(40):
            d = r.randint(1, 100)
            pts = [(r.randint(-10000, 10000), r.randint(1, d)) for _ in range(1000)]
            blocks.append(_blk1328(1000, d, pts))
    return "".join(blocks) + "0 0\n"

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1328: Radar Installation\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/01328/\n# License: not declared in source collection; no license is inferred.\nimport math\n\ndef solve(n, d, islands):\n    if d < 0:\n        return -1\n\n    ranges = []\n    for x, y in islands:\n        if y > d:\n            return -1\n        delta = math.sqrt(d * d - y * y)\n        ranges.append((x - delta, x + delta))\n\n    if not ranges:\n        return -1\n\n    ranges.sort(key=lambda x:x[1])\n\n    number = 1\n    r = ranges[0][1]\n    for start, end in ranges[1:]:\n        if r < start:\n            r = end\n            number += 1\n\n    return number\n\ncase_number = 0\nwhile True:\n    n, d = map(int, input().split())\n    if n == 0 and d == 0:\n        break\n\n    case_number += 1\n    islands = []\n    for _ in range(n):\n        islands.append(tuple(map(int, input().split())))\n\n    result = solve(n, d, islands)\n    print(f"Case {case_number}: {result}")\n    input()\n'
SAMPLE='3 2\n1 2\n-3 1\n2 1\n\n1 2\n0 2\n\n0 0\n'
GENERATOR='g1328'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[g1328_v2(random.Random(seed), seed) for seed in range(1, 40)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
