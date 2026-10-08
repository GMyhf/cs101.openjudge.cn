import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23805/\n# Accepted submission: 43290402\n# Source: http://cs101.openjudge.cn/practice/solution/43290402/\n# License: not declared on the submission page; no license is inferred.\n\n# -*- coding: utf-8 -*-\n"""\nCreated on Fri Dec 22 14:11 2023\n\n@author: 谢宇翔\n"""\nmdays = [\n    0\n    , 31\n    , 28 + 31\n    , 31 + 28 + 31\n    , 30 + 31 + 28 + 31\n    , 31 + 30 + 31 + 28 + 31\n    , 30 + 31 + 30 + 31 + 28 + 31\n    , 31 + 30 + 31 + 30 + 31 + 28 + 31\n    , 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31\n    , 30 + 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31\n    , 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31\n    , 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31\n    , 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31\n]\n\n\ndef convert(hour, minute, sec, day, mon, year):\n    total = 0\n    for year_ in range(2000, year):\n        if year_ % 4 == 0 and not (year_ % 100 == 0 and year_ % 400):\n            total += 366\n        else:\n            total += 365\n    if year % 4 == 0 and not (year % 100 == 0 and year % 400):\n        if mon > 2:\n            total += 1\n    total += day - 1\n    total += mdays[mon-1]\n    mday = total % 100\n    total //= 100\n    mmonth = total % 10\n    myear = total // 10\n    total = hour * 3600 + minute * 60 + sec\n    total = int(total * 100000 / (24 * 3600))\n    msec = total % 100\n    total //= 100\n    mmin = total % 100\n    mhour = total // 100\n\n    print(\'{}:{}:{} {}.{}.{}\'.format(mhour, mmin, msec, mday + 1, mmonth + 1, myear))\n\n\nn = int(input())\nfor _ in range(n):\n    p, q = input().split()\n    a, b, c = map(int, p.split(":"))\n    d, e, f = map(int, q.split("."))\n    convert(a, b, c, d, e, f)\n\n\n'
SAMPLE='7 \n0:0:0 1.1.2000 \n10:10:10 1.3.2001 \n0:12:13 1.3.2400 \n23:59:59 31.12.2001 \n0:0:1 20.7.7478 \n0:20:20 21.7.7478 \n15:54:44 2.10.20749\n'
GENERATOR_NAME='g23805'
def g23805(r):
    n=r.randint(1,10); rows=[]
    for _ in range(n): rows.append(f"{r.randint(0,23)}:{r.randint(0,59)}:{r.randint(0,59)} {r.randint(1,28)}.{r.randint(1,12)}.{r.randint(2000,50000)}")
    return f"{n}\n"+"\n".join(rows)+"\n"

def _leap(y): return y%4==0 and (y%100!=0 or y%400==0)
def _mdays(y,m): return [31,29 if _leap(y) else 28,31,30,31,30,31,31,30,31,30,31][m-1]

def valid(text):
    """题面：第一行整数 N；其后 N 行 "hour:minute:second day.month.year"，日期总是合法，2000<=year<=50000。"""
    import re
    lines=text.split('\n')
    if lines and lines[-1]=='': lines.pop()
    if not lines or not re.fullmatch(r'[0-9]+',lines[0].strip()): return False
    n=int(lines[0].strip())
    if n<1 or len(lines)!=n+1: return False
    for l in lines[1:]:
        mt=re.fullmatch(r'([0-9]+):([0-9]+):([0-9]+) ([0-9]+)\.([0-9]+)\.([0-9]+)',l.strip())
        if not mt: return False
        h,mi,se,d,mo,y=map(int,mt.groups())
        if not (0<=h<=23 and 0<=mi<=59 and 0<=se<=59): return False
        if not (2000<=y<=50000 and 1<=mo<=12 and 1<=d<=_mdays(y,mo)): return False
    return True

def _from_offset(k):
    # 2000-01-01 之后第 k 天的公历日期（400 年一个周期 146097 天）
    import datetime
    cyc,rem=divmod(k,146097)
    d=datetime.date(2000,1,1)+datetime.timedelta(rem)
    return d.day,d.month,d.year+400*cyc

def _row(h,mi,se,d,mo,y): return f"{h}:{mi}:{se} {d}.{mo}.{y}"

def _rand_time(r):
    t=r.choice([r.randrange(86400), r.randrange(800)*108, (r.randrange(800)*108+r.choice([-1,1]))%86400])
    t%=86400
    return t//3600,t//60%60,t%60

def _rand_date(r,y0=2000,y1=50000):
    while True:
        y=r.randint(y0,y1); mo=r.randint(1,12); d=r.randint(1,31)
        if d<=_mdays(y,mo): return d,mo,y

def g_edge(r,n,kind):
    rows=[]
    for _ in range(n):
        h,mi,se=_rand_time(r)
        if kind=='monthend':
            y=r.choice([r.randint(2000,50000),r.choice([2000,2100,2400,4000,4100,49996,50000])]); mo=r.randint(1,12); d=_mdays(y,mo)-r.choice([0,0,1,2])
        elif kind=='feb':
            y=r.choice([2000,2001,2004,2100,2400,3900,4000,10000,49996,49900,50000,r.randint(2000,50000)]); mo=r.choice([2,2,3]); d=r.choice([28,29,1]) if mo==2 else 1
            if d>_mdays(y,mo): d=28
        elif kind=='round':
            # 特殊历法换日/换月/换年边界：距 2000-01-01 恰为 100/1000 的倍数及其前一天
            k=r.randint(0,17530)*1000+r.choice([-1,0,0,99,100,-100])
            k=min(max(k,0),17531400)
            d,mo,y=_from_offset(k)
            if y>50000: d,mo,y=31,12,50000
        elif kind=='big':
            d,mo,y=_rand_date(r,45000,50000)
        else:
            d,mo,y=_rand_date(r)
        rows.append(_row(h,mi,se,d,mo,y))
    return f"{n}\n"+"\n".join(rows)+"\n"

def build_cases():
    cases=[SAMPLE]+[g23805(random.Random(s)) for s in range(1,20)]
    fixed="6\n0:0:0 1.1.2000\n23:59:59 31.12.50000\n0:1:48 29.2.2000\n0:1:47 28.2.2100\n12:0:0 29.2.2400\n23:59:59 29.2.49996\n"
    cases.append(fixed)
    spec=[(1,'monthend'),(10,'monthend'),(30,'monthend'),(10,'feb'),(30,'feb'),(10,'round'),(30,'round'),(60,'round'),
          (20,'rand'),(50,'rand'),(100,'rand'),(100,'big'),(150,'big'),(200,'big'),(100,'round'),(100,'monthend'),(100,'feb'),
          (200,'rand'),(200,'round')]
    cases+=[g_edge(random.Random(23805*100+i),n,k) for i,(n,k) in enumerate(spec)]
    return cases

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=build_cases()
    assert len(cases)==40 and len(set(cases))==40 and all(valid(c) for c in cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
