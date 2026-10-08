import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = """# 高效参考解：每个公共场所把自己的人数加到覆盖它的所有炸点上，O(k*(2d+1)^2*T)。
# 计数口径与原 AC 解（samplecode.py，提交 22600399）一致：数 (位置, 时间) 对、t 取 (x, y, t) 字典序第一个达到最大值的时间。
d = int(input())
k, T = map(int, input().split())
N = 129
acc = [[0] * (N * N) for _ in range(T)]
for _ in range(k):
    row = list(map(int, input().split()))
    x, y, p = row[0], row[1], row[2:]
    for i in range(max(0, x - d), min(N - 1, x + d) + 1):
        for j in range(max(0, y - d), min(N - 1, y + d) + 1):
            idx = i * N + j
            for t in range(T):
                acc[t][idx] += p[t]
best = max(max(a) for a in acc)
num = sum(a.count(best) for a in acc)
t0 = None
for idx in range(N * N):
    for t in range(T):
        if acc[t][idx] == best:
            t0 = t
            break
    if t0 is not None:
        break
print(num, t0, best)
"""
SAMPLE='1\n2 1\n4 4 10\n6 6 20\n'
GENERATOR_NAME='g20107'
SAMPLE2='4\n3 3\n100 100 30 21 29\n108 108 20 20 20\n50 50 50 10 10\n'


def valid(text):
    """题面：1<=d<=20, 1<=k<=20, 1<=T<=10, 0<=x,y<=128, 0<=Pi<=1,000,000，坐标不重复；
    第一行 d，第二行 k T，接下来 k 行每行 2+T 个整数。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    try:
        if len(lines) < 2 or len(lines[0].split()) != 1 or len(lines[1].split()) != 2:
            return False
        d = int(lines[0]); k, t = map(int, lines[1].split())
        if not (1 <= d <= 20 and 1 <= k <= 20 and 1 <= t <= 10) or len(lines) != 2 + k:
            return False
        seen = set()
        for line in lines[2:]:
            v = list(map(int, line.split()))
            if len(v) != 2 + t or not (0 <= v[0] <= 128 and 0 <= v[1] <= 128):
                return False
            if any(not 0 <= p <= 1000000 for p in v[2:]) or (v[0], v[1]) in seen:
                return False
            seen.add((v[0], v[1]))
    except ValueError:
        return False
    return True


def best_times(text):
    """返回达到全局最大伤亡的时间集合；生成器拒收跨时间并列的数据（题面没说并列时 T 取哪个、位置怎么计数）。"""
    lines = text.split('\n'); d = int(lines[0]); k, t = map(int, lines[1].split())
    pts = [list(map(int, lines[2 + i].split())) for i in range(k)]
    best = {}
    for tt in range(t):
        m = 0
        for i in range(129):
            near = [p for p in pts if abs(p[0] - i) <= d]
            if not near:
                continue
            for j in range(129):
                s = sum(p[2 + tt] for p in near if abs(p[1] - j) <= d)
                if s > m:
                    m = s
        best[tt] = m
    top = max(best.values())
    return {tt for tt, v in best.items() if v == top}


def g20107(r):
    kind = r.randrange(6)
    d = r.randint(1, 20) if kind != 5 else r.choice([1, 20])
    k = r.randint(1, 20) if kind not in (4, 5) else 20
    t = r.randint(1, 10) if kind != 5 else 10
    pmax = r.choice([10, 1000, 1000000])
    if kind == 0:      # 密集簇：大量公共场所挤在一起，覆盖关系复杂
        cx, cy = r.randint(0, 128), r.randint(0, 128)
        pool = [(x, y) for x in range(max(0, cx - 2 * d), min(128, cx + 2 * d) + 1)
                for y in range(max(0, cy - 2 * d), min(128, cy + 2 * d) + 1)]
    elif kind == 1:    # 贴边贴角：炸点必须裁到 0..128 之内
        pool = [(x, y) for x in range(129) for y in range(129)
                if min(x, 128 - x) <= d or min(y, 128 - y) <= d]
    else:
        pool = [(x, y) for x in range(129) for y in range(129)]
    coords = r.sample(pool, min(k, len(pool)))
    rows = [f"{x} {y} " + " ".join(str(r.randint(0, pmax)) for _ in range(t)) for x, y in coords]
    return f"{d}\n{len(coords)} {t}\n" + "\n".join(rows) + "\n"


FIXED = [
    '1\n1 1\n0 0 5\n',                                  # 角点：只有 (d+1)^2 个位置
    '20\n1 1\n128 128 1000000\n',                       # 对角 + d 上界
    '3\n1 1\n64 64 0\n',                                # 全 0：所有 129*129 个位置都并列
    '20\n2 1\n0 0 1000000\n128 128 1000000\n',          # 两点不可能同覆盖
    '20\n2 2\n0 64 7 3\n40 64 7 9\n',                   # 恰好 2d 距离可同覆盖
    '20\n2 2\n0 64 7 3\n41 64 7 9\n',                   # 距离 2d+1 不能同覆盖
]


def build_cases():
    cases = [SAMPLE, SAMPLE2] + FIXED
    seed = 1
    while len(cases) < 40:
        text = g20107(random.Random(seed)); seed += 1
        if text in cases or len(best_times(text)) != 1:
            continue
        cases.append(text)
    return cases

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
