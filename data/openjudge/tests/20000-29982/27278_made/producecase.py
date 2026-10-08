import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='n, m = map(int,input().split())\nd = [0] + list(map(int,input().split()))\na = [0] + list(map(int,input().split()))\ndef can(x):\n    last = [0] * (m + 1) #last[i]表示科目i在[1,x]中的最后出现位置 ，m科目数，x表示1~x天\n    for i in range(1, x + 1):\n        if d[i] != 0:\n            last[d[i]] = i\n    for i in range(1, m + 1): #有科目没出现\n        if last[i] == 0:\n            return False\n    free = 0  #可用的复习天数\n    done = [False] * (m + 1)\n    for i in range(1, x + 1):\n        subj = d[i]\n        if subj != 0 and last[subj] == i:  #这一天是某科目的最后可考日\n            need = a[subj]\n            if free < need:\n                return False\n            free -= need\n            done[subj] = True\n        else:\n            free += 1\n    return all(done[1:])\nlo, hi = 1, n \nans = -1\nwhile lo <= hi:\n    mid = (lo + hi) // 2\n    if can(mid):\n        ans = mid\n        hi = mid - 1\n    else:\n        lo = mid + 1\nprint(ans)'
SAMPLE='7 2\n0 1 0 2 1 0 2\n2 1\n'
GENERATOR_NAME='g27278'


def valid(text):
    """题面：n m (1<=n,m<=1e5)；n 个 d_i (0<=d_i<=m)；m 个 a_i (1<=a_i<=1e5)。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 3:
        return False
    rows = [ln.split(" ") for ln in lines]
    for row in rows:
        if not all(re.fullmatch(r"0|[1-9][0-9]*", x) for x in row):
            return False
    if len(rows[0]) != 2:
        return False
    n, m = map(int, rows[0])
    if not (1 <= n <= 10**5 and 1 <= m <= 10**5):
        return False
    if len(rows[1]) != n or len(rows[2]) != m:
        return False
    if not all(0 <= int(x) <= m for x in rows[1]):
        return False
    return all(1 <= int(x) <= 10**5 for x in rows[2])


def _fmt(n, m, d, a):
    return f"{n} {m}\n{' '.join(map(str, d))}\n{' '.join(map(str, a))}\n"


def _tight(r, n, m, zero_rate, slack):
    """构造恰好可行/接近可行的数据：先定每科的考试日（即最后出现位置），其余天只放更晚才考的科目或 0。"""
    import bisect
    assert 2 * m <= n
    # 每科占一段长度 >=2 的区间（复习日 + 末尾考试日），总长恰为 n，最后一天必是考试日
    extra = n - 2 * m
    cuts = sorted(r.randint(0, extra) for _ in range(m - 1))
    gaps = [b - a + 2 for a, b in zip([0] + cuts, cuts + [extra])]
    pos = []
    acc = -1
    for g in gaps:
        acc += g; pos.append(acc)
    assert pos[-1] == n - 1
    order = list(range(1, m + 1)); r.shuffle(order)
    d = [0] * n
    exam_at = {}
    for p, sub in zip(pos, order):
        d[p] = sub; exam_at[p] = sub
    for i in range(n):
        if i in exam_at or r.random() < zero_rate:
            continue
        j = bisect.bisect_right(pos, i)
        d[i] = order[r.randint(j, m - 1)]
    a = [0] * (m + 1)
    carry = 0
    prev = -1
    for p, sub in zip(pos, order):
        free = carry + (p - prev - 1)
        give = max(1, min(10**5, free - r.randint(0, slack)))
        a[sub] = give
        carry = free - give
        prev = p
    return d, a[1:]


def g27278(r, index):
    if index <= 12:
        # 小规模（可暴力核对）
        m = r.randint(1, 3); n = r.randint(1, 9)
        if index == 1:
            return _fmt(2, 1, [0, 1], [1])  # 恰好可行
        d = [r.randint(0, m) for _ in range(n)]
        a = [r.randint(1, 2) for _ in range(m)]
        return _fmt(n, m, d, a)
    if index <= 20:
        m = r.randint(1, 10); n = r.randint(m, 100); d = [r.randint(0, m) for _ in range(n)]
        for i in range(1, m + 1): d[r.randrange(n)] = i
        a = [r.randint(1, 8) for _ in range(m)]
        if index % 4 == 0:
            m, n = 1, r.randint(2, 100); d, a = [0] * (n - 1) + [1], [n - 1]
        return _fmt(n, m, d, a)
    if index == 21:
        return _fmt(1, 1, [1], [1])       # 第 1 天无复习时间：-1
    if index == 22:
        return _fmt(3, 2, [0, 1, 2], [1, 1])  # 第 3 天两科都考不完：-1
    if index == 23:
        n = 10**5
        return _fmt(n, 1, [0] * (n - 1) + [1], [10**5 - 1])
    if index == 24:
        n = 10**5
        return _fmt(n, 1, [0] * (n - 1) + [1], [10**5])  # 差一天：-1
    if index == 25:
        # m=1e5、n=1e5：每天都必须考试，无复习时间 -> -1
        n = m = 10**5
        d = list(range(1, m + 1)); r.shuffle(d)
        return _fmt(n, m, d, [1] * m)
    if index == 26:
        # 有一科从未出现 -> -1
        n, m = 10**5, 1000
        d = [r.randint(1, m - 1) for _ in range(n)]
        return _fmt(n, m, d, [r.randint(1, 50) for _ in range(m)])
    # 大规模紧凑构造：答案落在中后段，或因 a_i 多 1 而变 -1
    n = r.choice([10**5, r.randint(60000, 10**5)])
    m = r.choice([r.randint(1, 50), r.randint(100, 5000), r.randint(10000, 30000), r.randint(n // 2 - 10000, n // 2)])
    d, a = _tight(r, n, m, r.choice([0.1, 0.5, 0.9]), r.randint(0, 3))
    if index % 3 == 0:
        k = r.randrange(m); a[k] = min(10**5, a[k] + r.randint(1, 1000))
    return _fmt(n, m, d, a)

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
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])
    for s in range(1, 40):
        for attempt in range(100):
            c = globals()[GENERATOR_NAME](random.Random(s + attempt * 1000), s)
            if c not in cases: break
        cases.append(c)
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
