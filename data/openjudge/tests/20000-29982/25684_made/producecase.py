import random, subprocess, sys, tempfile
from pathlib import Path
# 原参考解 chairs=[0]*(10**6+1) 逐时刻累加：s+d 可达 2*10^6 会越界，且 O(sum d) 满规模超时。
# 换成按时刻扫描：同一时刻先离开后到达（区间 [s, s+d) 左闭右开）。
REFERENCE="""import sys
data = sys.stdin.buffer.read().split()
m, c = int(data[0]), int(data[1])
ev = {}
for i in range(m):
    n, s, d = int(data[2 + 3 * i]), int(data[3 + 3 * i]), int(data[4 + 3 * i])
    if d > 0:
        ev[s] = ev.get(s, 0) + n
        ev[s + d] = ev.get(s + d, 0) - n
cur = 0
ok = True
for t in sorted(ev):
    cur += ev[t]
    if cur > c:
        ok = False
        break
print('Y' if ok else 'N')
"""
SAMPLE='2 3\n2 1 4\n3 5 3\n'
SAMPLE2='2 3\n2 1 4\n2 1 4\n'
GENERATOR_NAME='g25684'

def parse(text):
    t = text.split(); m, c = int(t[0]), int(t[1])
    return m, c, [tuple(map(int, t[2 + 3 * i:5 + 3 * i])) for i in range(m)]

def valid(text):
    """题面：第一行 m c（1<=m<=1000，1<=c<=10000）；接下来 m 行 n s d，
    0<=s,d<=10^6，人数 n 为正整数（题面未给上界）。"""
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    def ints(line, k):
        x = line.split(" ")
        if len(x) != k or not all(v.isdigit() for v in x): return None
        return list(map(int, x))
    h = ints(lines[0], 2) if lines else None
    if h is None: return False
    m, c = h
    if not (1 <= m <= 1000 and 1 <= c <= 10000) or len(lines) != m + 1: return False
    for line in lines[1:]:
        x = ints(line, 3)
        if x is None: return False
        n, s, d = x
        if n < 1 or not (0 <= s <= 10 ** 6 and 0 <= d <= 10 ** 6): return False
    return True

def occupancy_at(rows, t):
    return sum(n for n, s, d in rows if s <= t < s + d)

def unambiguous(text):
    """d=0 的组题面没说是否需要座位：只允许它们在到达时刻本来就坐得下。"""
    m, c, rows = parse(text)
    return all(occupancy_at(rows, s) + n <= c for n, s, d in rows if d == 0)

def brute(text):
    """独立 oracle：在所有到达时刻检查占用（占用只在到达时刻增加）。"""
    m, c, rows = parse(text)
    return 'Y' if all(occupancy_at(rows, s) <= c for n, s, d in rows if d > 0) else 'N'

def max_occ(rows):
    ev = {}
    for n, s, d in rows:
        if d: ev[s] = ev.get(s, 0) + n; ev[s + d] = ev.get(s + d, 0) - n
    cur = best = 0
    for t in sorted(ev): cur += ev[t]; best = max(best, cur)
    return best

def fmt(c, rows):
    return f"{len(rows)} {c}\n" + "\n".join(f"{n} {s} {d}" for n, s, d in rows) + "\n"

def tight(r, m, smax, dmax, nmax, want, zero=0.0):
    """随机区间，c 取最大占用（Y）或最大占用-1（N）。"""
    while True:
        rows = []
        for _ in range(m):
            d = 0 if r.random() < zero else r.randint(1, dmax)
            rows.append((r.randint(1, nmax), r.randint(0, smax), d))
        M = max_occ(rows)
        c = M if want == 'Y' else M - 1
        if not (1 <= c <= 10000): continue
        text = fmt(c, rows)
        if valid(text) and unambiguous(text): return text

def g25684(r):
    m = r.randint(1, 30)
    return tight(r, m, r.choice([20, 1000, 10 ** 6]), r.choice([5, 100, 10 ** 6]), r.randint(1, 50), r.choice('YN'), 0.1)

def special():
    out = [SAMPLE2, "1 1\n1 0 1\n", "1 1\n2 0 1\n", "1 10000\n10000 1000000 1000000\n",
           "2 5\n5 0 10\n5 10 10\n", "2 5\n5 0 11\n5 10 10\n", "3 4\n1 7 0\n4 3 4\n3 7 2\n"]
    # 首尾相接的长链：闭区间写法会误判 N
    rows = [(10000, 1000 * i, 1000) for i in range(1000)]
    out.append(fmt(10000, rows))
    rows = [(10000 - (i % 7), 1000 * i, 1000 + (i == 777)) for i in range(1000)]
    out.append(fmt(10000, rows))  # 第 777 组多占 1 个时刻，与下一组重叠 -> N
    r = random.Random(256840)
    out.append(tight(r, 1000, 10 ** 6, 10 ** 6, 20, 'Y'))
    out.append(tight(r, 1000, 10 ** 6, 10 ** 6, 20, 'N'))
    out.append(tight(r, 1000, 10 ** 6, 3000, 300, 'Y'))
    out.append(tight(r, 1000, 10 ** 6, 3000, 300, 'N'))
    out.append(tight(r, 1000, 2000, 100, 100, 'Y', 0.05))
    out.append(tight(r, 1000, 2000, 100, 100, 'N', 0.05))
    # 单个大组超过 c，其余都很空
    rows = [(1, 2 * i, 1) for i in range(999)] + [(10001, 500000, 1)]
    out.append(fmt(10000, rows))
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
        assert valid(c) and unambiguous(c), i
        out = run(c)
        assert out.strip() == brute(c), i
        (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(out)
if __name__=='__main__': main()
