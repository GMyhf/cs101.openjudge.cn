import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/27367/\n# Accepted submission: 52735844\n# Source: http://cs101.openjudge.cn/practice/solution/52735844/\n# License: not declared on the submission page; no license is inferred.\n\nn, m = map(int, input().split())\nstudents = []\n\nfor _ in range(n):\n    parts = list(map(int, input().split()))\n    idx = parts[0]          # 编号\n    scores = parts[1:]     # 分数列表\n\n    # 1. 计算优秀次数（>=90）\n    excellent = sum(1 for s in scores if s >= 90)\n\n    # 2. 计算进步总和\n    progress = 0\n    for i in range(1, len(scores)):\n        diff = scores[i] - scores[i-1]\n        if diff > 0:\n            progress += diff\n\n    students.append((-excellent, -progress, idx))  # 负号=降序\n\n# 排序：默认升序，负号就等价于降序\nstudents.sort()\n\n# 输出\nfor s in students:\n    print(s[2])'
SAMPLE='5 4\n1001 60 80 90 90\n1002 90 80 91 92\n1003 95 94 93 92\n1004 70 90 80 85\n1005 85 88 91 96\n'
EXTRA_CASE=None
GENERATOR_NAME='g27367'
def valid(text):
    """题面：第一行两个正整数 N M；接下来 N 行，每行 M+1 个整数：营员编号（唯一）和 M 次得分（60~100）。"""
    lines = text.split('\n')
    if len(lines) < 2 or lines[-1] != '':
        return False
    lines = lines[:-1]
    def ints(line):
        toks = line.split(' ')
        if any(not t.isdigit() or t != str(int(t)) for t in toks):
            return None
        return list(map(int, toks))
    first = ints(lines[0])
    if first is None or len(first) != 2 or first[0] < 1 or first[1] < 1:
        return False
    n, m = first
    if len(lines) != n + 1:
        return False
    ids = set()
    for line in lines[1:]:
        row = ints(line)
        if row is None or len(row) != m + 1:
            return False
        if any(not 60 <= s <= 100 for s in row[1:]):
            return False
        ids.add(row[0])
    return len(ids) == n

def fmt(rows, m):
    return f"{len(rows)} {m}\n" + "".join(f"{i} {' '.join(map(str, sc))}\n" for i, sc in rows)

def g27367(r):
    kind = r.random()
    if kind < 0.1:
        n, m = r.randint(1, 5), r.randint(1, 3)
    elif kind < 0.2:
        n, m = r.randint(300, 1000), r.randint(20, 50)
    else:
        n, m = r.randint(2, 80), r.randint(1, 12)
    # 编号唯一但打乱顺序，卡掉“依赖稳定排序、不按编号比较”的写法
    ids = r.sample(range(1, 100000), n) if r.random() < .5 else r.sample(range(1000, 1000 + n), n)
    rows = []
    pool = []
    for i in ids:
        if pool and r.random() < 0.35:
            sc = list(r.choice(pool))           # 复制已有分数，制造优秀数与进步分都相同的并列
            if r.random() < .5:
                r.shuffle(sc)                    # 打乱：优秀数相同而进步分常不同
        else:
            lo = r.choice([60, 60, 80, 88])
            sc = [r.randint(lo, 100) for _ in range(m)]
        pool.append(sc)
        rows.append((i, sc))
    return fmt(rows, m)

SPECIAL_CASES = [
    '1 1\n7 60\n',                                    # 最小规模
    '3 1\n30 90\n10 89\n20 100\n',                  # M=1：无进步分，只比优秀数和编号
    '4 3\n4 90 90 90\n3 60 100 60\n2 100 60 100\n1 89 89 89\n',  # 优秀数、进步分各种并列
    '4 2\n9 60 100\n8 100 60\n7 61 100\n6 60 99\n',  # 进步只算正差，下降不扣分
]

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case(): return EXTRA_CASE
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+SPECIAL_CASES; s=0
    while len(cases)<40:
        s+=1; c=globals()[GENERATOR_NAME](random.Random(s))
        if c not in cases: cases.append(c)
    assert all(valid(c) for c in cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
