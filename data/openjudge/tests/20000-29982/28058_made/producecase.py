import random, subprocess, sys, tempfile
from pathlib import Path

REFERENCE = '# External reference: statistics page /practice/28058/\n# Accepted submission: 52734701\n# Source: http://cs101.openjudge.cn/practice/solution/52734701/\n# License: not declared on the submission page; no license is inferred.\n\n# 存菜品：name:[price, stock]\nfood = dict()\nn, m = map(int, input().split())\n\nfor _ in range(n):\n    name, p, s = input().split()\n    price = int(p)\n    stock = int(s)\n    food[name] = [price, stock]\n\nincome = 0\n# 处理每个学生的3个菜\nfor _ in range(m):\n    lst = input().split()\n    for dish in lst:\n        pr, st = food[dish]\n        if st > 0:\n            income += pr\n            food[dish][1] -= 1\n\nprint(income)'

import re

SAMPLE = ('5 5\nyangroupaomo 13 10\njituifan 7 5\nluosifen 16 3\nxinlamian 12 20\njuruo_milktea 999 1\n'
          'yangroupaomo luosifen juruo_milktea\nluosifen xinlamian jituifan\nyangroupaomo jituifan juruo_milktea\n'
          'jituifan xinlamian luosifen\nyangroupaomo yangroupaomo yangroupaomo\n')
NAME = re.compile(r'[a-z_]+')


def _int(s):
    return s.isdigit() and (s == '0' or s[0] != '0')


def valid(text):
    """题面：第一行 n（菜数）m（学生数）；n 行“菜名 售价 可提供量”，菜名互不相同、售价为整数；
    m 行各 3 个菜名，均在菜单中。题面未给数值上界，本数据取 1≤n≤1000、1≤m≤3e4、
    菜名为小写字母与下划线（同样例）、1≤售价≤1000、0≤可提供量≤1e5。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    h = lines[0].split(' ')
    if len(h) != 2 or not all(_int(t) for t in h):
        return False
    n, m = map(int, h)
    if not (1 <= n <= 1000 and 1 <= m <= 30000) or len(lines) != 1 + n + m:
        return False
    menu = set()
    for ln in lines[1:1 + n]:
        p = ln.split(' ')
        if len(p) != 3 or not NAME.fullmatch(p[0]) or len(p[0]) > 20 or p[0] in menu:
            return False
        if not (_int(p[1]) and _int(p[2]) and 1 <= int(p[1]) <= 1000 and 0 <= int(p[2]) <= 10 ** 5):
            return False
        menu.add(p[0])
    for ln in lines[1 + n:]:
        p = ln.split(' ')
        if len(p) != 3 or any(x not in menu for x in p):
            return False
    return True


def names(r, n, lo=3, hi=12):
    out = set()
    while len(out) < n:
        s = ''.join(r.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(r.randint(lo, hi)))
        if r.random() < .2 and len(s) > 2:
            i = r.randint(1, len(s) - 2); s = s[:i] + '_' + s[i + 1:]
        out.add(s)
    out = sorted(out); r.shuffle(out); return out


def fmt(menu, orders):
    return f"{len(menu)} {len(orders)}\n" + "\n".join(f"{a} {b} {c}" for a, b, c in menu) + "\n" + \
        "\n".join(" ".join(o) for o in orders) + "\n"


def gen(r, n, m, smax, pmax=1000, lo=3, hi=12, hot=False):
    ns = names(r, n, lo, hi)
    menu = [(x, r.randint(1, pmax), r.randint(0, smax)) for x in ns]
    if hot:  # 集中点少数几道菜，使大量菜售罄
        w = ns[:max(1, n // 10)]
        orders = [[r.choice(w) if r.random() < .7 else r.choice(ns) for _ in range(3)] for _ in range(m)]
    else:
        orders = [[r.choice(ns) for _ in range(3)] for _ in range(m)]
    return fmt(menu, orders)


def build_cases():
    r = random.Random(28058)
    cases = [SAMPLE]
    # 规模组（单组 .in < 1MB）
    cases.append(gen(r, 1000, 30000, 100, lo=3, hi=6, hot=True))
    cases.append(gen(r, 1000, 30000, 10 ** 5, lo=3, hi=6))            # 全都买得到
    cases.append(gen(r, 50, 30000, 1000, lo=3, hi=5))                 # 少量菜大量售罄
    cases.append(gen(r, 1000, 3000, 0, lo=8, hi=20))                  # 全部库存为 0，答案 0
    # 边界
    cases += [fmt([('a', 5, 2)], [['a', 'a', 'a']]),                  # 同一学生点同一道菜 3 次，库存 2
              fmt([('a', 5, 0)], [['a', 'a', 'a']]),
              fmt([('a', 1000, 100000)], [['a', 'a', 'a']]),
              fmt([('a', 1, 1)], [['a', 'a', 'a']] * 2),
              fmt([('x_y', 3, 1), ('xy', 4, 3), ('yx', 7, 0)], [['yx', 'xy', 'x_y'], ['x_y', 'xy', 'yx'], ['xy', 'xy', 'xy']]),
              fmt([('dish', 9, 3), ('unused', 100, 5)], [['dish', 'dish', 'dish'], ['dish', 'dish', 'dish']])]
    while len(cases) < 41:
        n = r.choice([r.randint(1, 5), r.randint(6, 50), r.randint(51, 1000)])
        m = r.choice([r.randint(1, 10), r.randint(11, 500), r.randint(501, 10000)])
        c = gen(r, n, m, r.choice([0, 3, 30, 1000]), hot=r.random() < .5)
        if c not in cases:
            cases.append(c)
    return cases


def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p = Path(d) / 'main.py'; p.write_text(REFERENCE)
        x = subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout


def main():
    d = Path('data'); d.mkdir(exist_ok=True)
    cases = build_cases()
    assert len(cases) == len(set(cases)), '组间有重复'
    for i, c in enumerate(cases):
        assert valid(c), f'第 {i} 组不合题面'
        (d / f'{i}.in').write_text(c); (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__':
    main()
