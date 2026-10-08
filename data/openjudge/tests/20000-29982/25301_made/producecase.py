import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='n=int(input())\nbirs={}\nfor i in range(n):\n    num,m,d=map(str,input().split())\n    m,d=int(m),int(d)\n    if (m,d) not in birs.keys():\n        birs[(m,d)]=[num]\n    else:\n        birs[(m,d)].append(num)\ndays=list(birs.keys())\ndays.sort()\nfor m,d in days:\n    if len(birs[(m,d)])>1:\n        output=[m,d]\n        for num in birs[(m,d)]:\n            output.append(num)\n        print(*output)'
SAMPLE='5\n00508192 3 2\n00508153 4 5\n00508172 3 2\n00508023 4 5\n00509122 4 5\n'
GENERATOR_NAME='g25301'
import re
MDAYS = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def valid(text):
    """题面契约：第一行整数 n (n<100)；之后恰好 n 行「学号 月 日」，单空格分隔；
    学号是长度小于 10 的字符串，1<=m<=12，1<=d<=31。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9][0-9]?", lines[0]):
        return False
    n = int(lines[0])
    if len(lines) != n + 1:
        return False
    for line in lines[1:]:
        m = re.fullmatch(r"(\S{1,9}) ([1-9][0-9]?) ([1-9][0-9]?)", line)
        if not m or not 1 <= int(m.group(2)) <= 12 or not 1 <= int(m.group(3)) <= 31:
            return False
    return True

def _ids(r, n):
    """互不相同、与输入顺序无关的学号（长度 1..9，不全按字典序递增）。"""
    out, used = [], set()
    while len(out) < n:
        k = r.choice([8, 8, 8, r.randint(1, 9)])
        x = "".join(r.choice("0123456789") for _ in range(k))
        if x not in used:
            used.add(x); out.append(x)
    return out

def _date(r, pool=None):
    if pool:
        return r.choice(pool)
    m = r.randint(1, 12)
    return m, r.randint(1, MDAYS[m - 1])

def _fmt(ids, dates):
    return f"{len(ids)}\n" + "\n".join(f"{i} {m} {d}" for i, (m, d) in zip(ids, dates)) + "\n"

def special_cases():
    r = random.Random(253010)
    cases = []
    # n=1：没有生日相同的，输出为空
    cases.append("1\n123456789 12 31\n")
    # n=99 全部同一天：一行输出 99 个学号，且学号按输入顺序（非字典序）
    ids = _ids(r, 99)
    cases.append(_fmt(ids, [(2, 29)] * 99))
    # n=99，日期集中在少数几天，含 10/11/12 月与 29/30/31 日，卡按字符串排序日期
    pool = [(1, 31), (2, 1), (10, 2), (11, 30), (12, 31), (9, 9), (1, 10), (3, 2)]
    ids = _ids(r, 99)
    cases.append(_fmt(ids, [_date(r, pool) for _ in range(99)]))
    # n=99，两两日期均不同之外再加少量重复
    ids = _ids(r, 99)
    alld = [(m, d) for m in range(1, 13) for d in range(1, MDAYS[m - 1] + 1)]
    ds = r.sample(alld, 95) + [(12, 31), (1, 1), (10, 10), (7, 31)]
    r.shuffle(ds)
    cases.append(_fmt(ids, ds))
    return cases

def g25301(r):
    n = r.choice([r.randint(2, 30), r.randint(30, 99), 99])
    ids = _ids(r, n)
    if r.random() < 0.5:
        pool = [_date(r) for _ in range(r.randint(1, 20))]
    else:
        pool = None
    return _fmt(ids, [_date(r, pool) for _ in range(n)])

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
    sp=special_cases(); cases=[SAMPLE]+sp+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40-len(sp))]
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)==40
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
