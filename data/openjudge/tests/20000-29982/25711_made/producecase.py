import random, subprocess, sys, tempfile
from pathlib import Path
# 原参考解用 int() 读得分，题面说“得分可能带有小数”，遇小数直接崩；改成 float()。
REFERENCE="""N, M = map(int, input().split())
result = []
for _ in range(N):
    line = input().split()
    s1 = 0.0
    s2 = 0
    for i in range(1, len(line) - 1, 2):
        sc = float(line[i]); cr = int(line[i + 1])
        g = 4 - 3 * (100 - sc) ** 2 / 1600 if sc >= 60 else 0
        s1 += g * cr
        s2 += cr
    result.append((s1 / s2, line[0]))
result.sort(key=lambda x: -x[0])
print(' '.join(x[1] for x in result[:M]))
"""
SAMPLE='5 3\n2201111000 80 5 78 3 95 2\n2201111001 59 2 67 3 60 4 57 2\n2201111002 78 5 80 2\n2201111003 60 2 100 5\n2201111004 78 4 84 2\n'
GENERATOR_NAME='g25711'

import re
from fractions import Fraction
SCORE_RE = re.compile(r"\d+(\.\d+)?")

def exact_gpas(text):
    lines = text[:-1].split("\n"); res = []
    for line in lines[1:]:
        t = line.split(" "); num = Fraction(0); den = 0
        for k in range(1, len(t), 2):
            sc = Fraction(t[k]); cr = int(t[k + 1])
            g = 4 - Fraction(3) * (100 - sc) ** 2 / 1600 if sc >= 60 else Fraction(0)
            num += g * cr; den += cr
        res.append((num / den, t[0]))
    return res

def valid(text):
    """题面：第一行 N M；接下来 N 行：学号 + 若干对（得分 学分），学分为整数、得分可带小数。
    同一学号只出现一次；保证绩点互不相同；需输出 M 个学号，故 1<=M<=N；每人至少一门课、学分为正，得分 0~100。"""
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    h = lines[0].split(" ")
    if len(h) != 2 or not all(x.isdigit() for x in h): return False
    n, m = map(int, h)
    if not (1 <= m <= n) or len(lines) != n + 1: return False
    ids = set()
    for line in lines[1:]:
        t = line.split(" ")
        if len(t) < 3 or len(t) % 2 == 0 or not t[0].isdigit() or t[0] in ids: return False
        ids.add(t[0])
        for k in range(1, len(t), 2):
            if not SCORE_RE.fullmatch(t[k]) or not t[k + 1].isdigit(): return False
            if not (0 <= Fraction(t[k]) <= 100) or int(t[k + 1]) < 1: return False
    g = [x[0] for x in exact_gpas(text)]
    return len(set(g)) == len(g)

def separated(text):
    """相邻绩点差足够大，浮点累加的误差不会影响排序。"""
    g = sorted(x[0] for x in exact_gpas(text))
    return all(b - a > Fraction(1, 10 ** 9) for a, b in zip(g, g[1:]))

def expected(text):
    m = int(text.split()[1])
    return " ".join(x[1] for x in sorted(exact_gpas(text), key=lambda x: -x[0])[:m])

def score(r, low, decimal):
    if r.random() < low: v = r.randint(0, 59) if not decimal or r.random() < 0.5 else round(r.uniform(0, 59.9), 1)
    else: v = r.randint(60, 100) if not decimal or r.random() < 0.5 else round(r.uniform(60, 99.9), r.choice([1, 2]))
    if isinstance(v, float) and v == int(v): v = int(v)
    return str(v)

def make(r, n, m, cmax, low, decimal):
    """逐行生成；与已有绩点相差不足 1e-9 的行重抽，保证绩点互异。"""
    import bisect
    ids = r.sample(range(2200000000, 2299999999), n); rows = []; gs = []
    for sid in ids:
        tries = 0
        while True:
            tries += 1
            if tries % 50 == 0: cmax += 1; decimal = True  # 取值空间不够时放宽
            vals = []
            for _ in range(r.randint(1, cmax)): vals += [score(r, low, decimal), str(r.randint(1, 6))]
            row = f"{sid} " + " ".join(vals)
            g = exact_gpas("0 0\n" + row + "\n")[0][0]
            k = bisect.bisect_left(gs, g)
            eps = Fraction(1, 10 ** 8)
            if (k == len(gs) or gs[k] - g > eps) and (k == 0 or g - gs[k - 1] > eps): break
        gs.insert(k, g); rows.append(row)
    text = f"{n} {m}\n" + "\n".join(rows) + "\n"
    assert valid(text) and separated(text)
    return text

def g25711(r):
    n = r.randint(2, 80); m = r.randint(1, n)
    return make(r, n, m, r.randint(1, 6), r.choice([0, 0.1, 0.3]), r.random() < 0.6)

def special():
    r = random.Random(257110)
    out = ["1 1\n2201111000 59.5 3\n",              # 唯一一人、59.5 分绩点为 0
           "2 1\n1 60 1\n2 59.9 9\n",               # 60 分恰好 1.0，59.9 为 0
           "3 3\n10 100 1\n11 99.5 2 100 1\n12 0 4 100 1\n",
           "3 2\n7 70.25 3 88 2\n8 88 2 70.5 3\n9 65 5\n"]
    out.append(make(r, 1000, 1, 8, 0.2, True))
    out.append(make(r, 1000, 1000, 8, 0.2, True))
    out.append(make(r, 1000, 500, 10, 0.4, True))
    out.append(make(r, 2000, 1234, 6, 0.1, False))
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=60)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case():
    if GENERATOR_NAME == 'g26267': return 'A'*1000000+'\n'+'A'*1000+'\n'
    if GENERATOR_NAME == 'g26273': return ('abcdefghij'*10000)+'\n'
    if GENERATOR_NAME == 'g26835':
        e=[(i-1,i,float(i)) for i in range(1,99)]
        for i in range(99):
            for j in range(i+2,min(99,i+12)): e.append((i,j,float(10000+i*99+j)))
        return '99 %d\n'%len(e)+'\n'.join(f'{a} {b} {w:.3f}' for a,b,w in e)+'\n'
    if GENERATOR_NAME == 'g27311': return '100000\n'+' '.join(str(i%10001) for i in range(100000))+'\n'+' '.join(str((i*7)%10001) for i in range(100000))+'\n'
    return None
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]
    cases += special()
    assert len(set(cases)) == len(cases)
    for i,c in enumerate(cases):
        assert valid(c) and separated(c), i
        out = run(c)
        assert out.strip() == expected(c), i
        (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(out)
if __name__=='__main__': main()
