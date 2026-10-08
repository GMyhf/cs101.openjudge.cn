import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/20196/\n# Accepted submission: 31921452\n# Source: http://cs101.openjudge.cn/practice/solution/31921452/\n# License: not declared on the submission page; no license is inferred.\n\nlt1=[31,29,31,30,31,30,31,31,30,31,30,31]\nlt=[31,28,31,30,31,30,31,31,30,31,30,31]\nimport math\ny,m,d=map(int,input().split())\ni_sl=365\nG=y\nif (y%4==0 and y%100!=0) or y%400==0:\n    used=lt1\n    i_sl=366\nelse:\n    used=lt\nG+=(sum(used[:m-1])+d-1)/i_sl\nH=(G-621.5774) / 0.970224\n\ny1=int(H)\nd1=H-y1\nlt2={2,5,7,10,13,16,18,21,24,26,29}\nis_sleap=354\nif y1%30 in lt2:\n    is_sleap=355\nd1*=is_sleap\n\nd1=math.ceil(d1)\n\nm1=0\nmut_year=[30,29,30,29,30,29,30,29,30,29,30,29]\nwhile m1<11 and d1>mut_year[m1]:\n    d1-=mut_year[m1]\n    m1+=1\nprint(y1,m1+1,d1)'
SAMPLE='2020 1 10\n'
GENERATOR_NAME='g20196'

# 题面：一行三个整数，公历生日的年、月、日（须是合法的公历日期）。题面没给年份范围；
# 生成数据取 1600..2400（H 恒为正，避免负数取整口径之争）。
from fractions import Fraction

_MDAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_ILEAP = {2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29}


def _gleap(y):
    return y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)


def _mdays(y, m):
    return 29 if m == 2 and _gleap(y) else _MDAYS[m - 1]


def valid(text):
    import re
    m = re.fullmatch(r"(-?\d+) (\d+) (\d+)\n", text)
    if not m:
        return False
    y, mo, d = map(int, m.groups())
    return y >= 1 and 1 <= mo <= 12 and 1 <= d <= _mdays(y, mo)


def _exact(y, m, d):
    """按题面公式用有理数精确计算，返回 (结果, 向上取整前距最近整数的距离)。"""
    doy = sum(_mdays(y, k) for k in range(1, m)) + d - 1
    G = y + Fraction(doy, 366 if _gleap(y) else 365)
    H = (G - Fraction(6215774, 10000)) / Fraction(970224, 1000000)
    hy = H.numerator // H.denominator
    t = (H - hy) * (355 if hy % 30 in _ILEAP else 354)
    day = -((-t.numerator) // t.denominator)
    gap = min(t - (t.numerator // t.denominator), day - t)
    mi = 0
    while mi < 11 and day > (30 if mi % 2 == 0 else 29):
        day -= 30 if mi % 2 == 0 else 29
        mi += 1
    return (hy, mi + 1, day), gap


def _safe(y, m, d):
    # 向上取整前离整数太近的日期，浮点写法不同可能差一天，不出这种数据
    return _exact(y, m, d)[1] > Fraction(1, 10 ** 6)


def _special():
    """满足特殊结果的日期：伊斯兰历 12 月 30 日（闰年最后一天）、1 月 1 日、某月 29/30 日；
    以及公历边界：1/1、12/31、2/29（含 1600、2000、2400）、1900/2100 的 2/28 与 3/1。"""
    out = [(2000, 2, 29), (1600, 2, 29), (2400, 2, 29), (1900, 2, 28), (1900, 3, 1), (2100, 3, 1),
           (2024, 12, 31), (2023, 1, 1), (2019, 12, 31), (2020, 12, 31)]
    want = {"12/30": None, "1/1": None, "12/29": None, "2/29": None, "11/30": None}
    for y in range(2000, 2100):
        for m in range(1, 13):
            for d in range(1, _mdays(y, m) + 1):
                (hy, hm, hd), _ = _exact(y, m, d)
                k = f"{hm}/{hd}"
                if k in want and want[k] is None and _safe(y, m, d):
                    want[k] = (y, m, d)
    return [v for v in out if _safe(*v)] + [v for v in want.values() if v]


_SPECIAL = None


def g20196(r, s):
    global _SPECIAL
    if _SPECIAL is None:
        _SPECIAL = _special()
    if s <= len(_SPECIAL):
        y, m, d = _SPECIAL[s - 1]
        return f"{y} {m} {d}\n"
    while True:
        y = r.randint(1600, 2400) if s % 3 == 0 else r.randint(1900, 2200)
        m = r.randint(1, 12)
        d = r.randint(1, _mdays(y, m))
        if _safe(y, m, d):
            return f"{y} {m} {d}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[g20196(random.Random(s), s) for s in range(1, 40)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
