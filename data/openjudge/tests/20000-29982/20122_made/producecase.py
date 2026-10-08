import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20122 statistics, Accepted solution 42258230.\n# Source: http://cs101.openjudge.cn/practice/solution/42258230/\n# Statistics: http://cs101.openjudge.cn/practice/20122/statistics/\n# License: not declared on submission page; no license inferred\n\'\'\'\n2300015897\n吴杰稀\n光华管理学院\n\'\'\'\ncases,date = map(int,input().split())\ncompany = []\nfor i in range(cases):\n    dates = list(map(int,input().split()))\n    dates.append(date)\n    dates.sort(reverse = True)\n    company.append(dates)\nfor _ in company:\n    t = _.index(date)\n    if t == 0:\n        print("3")\n    elif t == 1:\n        print("2")\n    elif t == 2:\n        print("1")\n    elif t == 3:\n        print("-4")\n    elif t == 4:\n        print("-3")\n'
SAMPLE='1 0626\n0320 0418 0816 1024\n'
GENERATOR_NAME='g20122'
SAMPLE2='3 0421\n0327 0426 0821 1026\n0428 0428 0825 1031\n0421 0421 0830 1030\n'
MDAYS = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def _mmdd(tok):
    if len(tok) != 4 or not tok.isdigit():
        return None
    mm, dd = int(tok[:2]), int(tok[2:])
    if not (1 <= mm <= 12 and 1 <= dd <= MDAYS[mm - 1]):
        return None
    return int(tok)


def valid(text):
    """题面：第一行 n m（n>0，m 为 MMDD 日期）；接下来 n 行每行 4 个 MMDD 日期：前一年年报、今年一/二/三季报的发布日期，
    均为今年的日期。年报→一季报→二季报→三季报按时间先后发布（可同日，见样例 2），题面的「最新可得」判断以此为前提。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    head = lines[0].split()
    if len(head) != 2 or not head[0].isdigit() or _mmdd(head[1]) is None:
        return False
    n = int(head[0])
    if n <= 0 or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        tok = line.split()
        if len(tok) != 4:
            return False
        v = [_mmdd(t) for t in tok]
        if None in v or v != sorted(v):
            return False
    return True


ALL_DATES = [m * 100 + d for m in range(1, 13) for d in range(1, [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1] + 1)]


def g20122(r, n=None):
    if n is None:
        n = r.choice([r.randint(1, 8), r.randint(10, 60), r.randint(500, 1000)])
    pool = r.choice([ALL_DATES, r.sample(ALL_DATES, 6)])     # 小日期池 → 大量同日发布、m 与发布日相等
    rows = []
    for _ in range(n):
        rows.append(sorted(r.choice(pool) for _ in range(4)))
    flat = [x for row in rows for x in row]
    m = r.choice([r.choice(flat), r.choice(flat), r.choice(ALL_DATES), 101, 1231])
    return f"{n} {m:04d}\n" + "\n".join(" ".join(f"{x:04d}" for x in row) for row in rows) + "\n"


FIXED = [
    '1 0101\n0101 0101 0101 0101\n',                 # 全部同日且等于 m → 3
    '1 0101\n0102 0103 0104 0105\n',                 # 早于所有发布 → -3
    '1 1231\n0331 0430 0831 1031\n',                 # 晚于所有发布 → 3
    '5 0430\n0430 0430 0830 1030\n0331 0430 0830 1030\n0331 0429 0430 1030\n0331 0429 0429 0430\n0501 0502 0830 1030\n',
    '5 0815\n0320 0418 0816 1024\n0320 0418 0815 1024\n0815 0815 0815 0815\n0816 0816 0816 0816\n0320 0418 0626 0815\n',
]


def build_cases():
    cases = [SAMPLE, SAMPLE2] + FIXED
    seed = 1
    while len(cases) < 40:
        text = g20122(random.Random(seed)); seed += 1
        if text not in cases:
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
