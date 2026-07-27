import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23805/\n# Accepted submission: 43290402\n# Source: http://cs101.openjudge.cn/practice/solution/43290402/\n# License: not declared on the submission page; no license is inferred.\n\n# -*- coding: utf-8 -*-\n"""\nCreated on Fri Dec 22 14:11 2023\n\n@author: 谢宇翔\n"""\nmdays = [\n    0\n    , 31\n    , 28 + 31\n    , 31 + 28 + 31\n    , 30 + 31 + 28 + 31\n    , 31 + 30 + 31 + 28 + 31\n    , 30 + 31 + 30 + 31 + 28 + 31\n    , 31 + 30 + 31 + 30 + 31 + 28 + 31\n    , 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31\n    , 30 + 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31\n    , 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31\n    , 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31\n    , 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31 + 28 + 31\n]\n\n\ndef convert(hour, minute, sec, day, mon, year):\n    total = 0\n    for year_ in range(2000, year):\n        if year_ % 4 == 0 and not (year_ % 100 == 0 and year_ % 400):\n            total += 366\n        else:\n            total += 365\n    if year % 4 == 0 and not (year % 100 == 0 and year % 400):\n        if mon > 2:\n            total += 1\n    total += day - 1\n    total += mdays[mon-1]\n    mday = total % 100\n    total //= 100\n    mmonth = total % 10\n    myear = total // 10\n    total = hour * 3600 + minute * 60 + sec\n    total = int(total * 100000 / (24 * 3600))\n    msec = total % 100\n    total //= 100\n    mmin = total % 100\n    mhour = total // 100\n\n    print(\'{}:{}:{} {}.{}.{}\'.format(mhour, mmin, msec, mday + 1, mmonth + 1, myear))\n\n\nn = int(input())\nfor _ in range(n):\n    p, q = input().split()\n    a, b, c = map(int, p.split(":"))\n    d, e, f = map(int, q.split("."))\n    convert(a, b, c, d, e, f)\n\n\n'
SAMPLE='7 \n0:0:0 1.1.2000 \n10:10:10 1.3.2001 \n0:12:13 1.3.2400 \n23:59:59 31.12.2001 \n0:0:1 20.7.7478 \n0:20:20 21.7.7478 \n15:54:44 2.10.20749\n'
GENERATOR_NAME='g23805'
def g23805(r):
    n=r.randint(1,10); rows=[]
    for _ in range(n): rows.append(f"{r.randint(0,23)}:{r.randint(0,59)}:{r.randint(0,59)} {r.randint(1,28)}.{r.randint(1,12)}.{r.randint(2000,50000)}")
    return f"{n}\n"+"\n".join(rows)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
