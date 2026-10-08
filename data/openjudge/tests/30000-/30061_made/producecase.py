import random
REFERENCE="# External reference: /practice/30061/statistics/\n# Accepted submission: 52831600\n# Source: http://cs101.openjudge.cn/practice/solution/52831600/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef main():\n    # 读取所有输入数据\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    # 解析 N 和 M\n    N = int(input_data[0])\n    M = int(input_data[1])\n    \n    # 将报出的编号放入集合中，便于快速查找\n    reported_students = set(map(int, input_data[2:2+M]))\n    \n    # 找出未到达的同学编号\n    missing_students = []\n    for i in range(N):\n        if i not in reported_students:\n            missing_students.append(i)\n            \n    # 根据要求输出结果\n    if not missing_students:\n        print(N)\n    else:\n        print(*(missing_students))\n\nif __name__ == '__main__':\n    main()"
SAMPLE='3 3\n0 2 1\n'
GENERATOR_NAME='g30061'
import re as _re

def valid(text):
    """题面：两行；第一行 N M（2 ≤ N,M ≤ 1000）；第二行 M 个小于 N 的非负整数。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if len(lines) != 2 or not _re.fullmatch(r'\d+ \d+', lines[0]):
        return False
    n, m = map(int, lines[0].split())
    if not (2 <= n <= 1000 and 2 <= m <= 1000):
        return False
    toks = lines[1].split(' ')
    if len(toks) != m or not all(_re.fullmatch(r'0|[1-9]\d*', t) for t in toks):
        return False
    return all(int(t) < n for t in toks)

def _fmt(n, vals):
    return f"{n} {len(vals)}\n" + " ".join(map(str, vals)) + "\n"

def g30061(r):
    # 旧版生成器：N 可为 1、M 可为 0，且编号互不重复；新数据见 build_cases()
    n = r.randint(1, 1000); m = r.randint(0, n); values = r.sample(range(n), m)
    return f"{n} {m}\n" + (" ".join(map(str, values)) + "\n" if values else "\n")

def _all_arrive(r, n, m):
    v = list(range(n)) + [r.randrange(n) for _ in range(m - n)]
    r.shuffle(v); return v

def _some(r, n, m, present):
    pool = r.sample(range(n), present)
    v = pool + [r.choice(pool) for _ in range(m - present)]
    r.shuffle(v); return v

def build_cases():
    r = random.Random(30061)
    cases = [SAMPLE, '3 5\n0 0 0 0 0\n']
    cases += ['2 2\n0 1\n', '2 2\n1 0\n', '2 2\n0 0\n', '2 2\n1 1\n', '3 2\n2 0\n', '2 5\n1 0 1 1 0\n']
    cases.append(_fmt(1000, list(range(1000))))                        # 全到，顺序
    cases.append(_fmt(1000, _all_arrive(r, 1000, 1000)))               # 全到，乱序 → 1000
    cases.append(_fmt(1000, [0] * 1000))                               # 只有 0 号 → 1..999
    cases.append(_fmt(1000, [999] * 1000))                             # 只有 999 号 → 0..998
    cases.append(_fmt(1000, [500, 500]))                               # M=2
    cases.append(_fmt(1000, list(range(1, 1000)) + [1]))               # 只缺 0
    cases.append(_fmt(1000, list(range(999)) + [998]))                 # 只缺 999
    cases.append(_fmt(2, [r.randrange(2) for _ in range(1000)]))       # N=2，M=1000
    cases.append(_fmt(999, _all_arrive(r, 999, 1000)))                 # 全到含重复
    for t in range(11):                                               # 中小规模全到/缺一部分
        n = r.randint(2, 60); m = r.randint(2, 120)
        if t % 3 == 0 and m >= n:
            cases.append(_fmt(n, _all_arrive(r, n, m)))
        else:
            cases.append(_fmt(n, _some(r, n, m, r.randint(1, min(n, m)))))
    for t in range(12):                                               # 大规模随机
        n = r.randint(500, 1000); m = r.randint(500, 1000)
        if t % 4 == 0 and m >= n:
            cases.append(_fmt(n, _all_arrive(r, n, m)))
        elif t % 4 == 1:
            cases.append(_fmt(n, [r.randrange(n) for _ in range(m)]))
        else:
            cases.append(_fmt(n, _some(r, n, m, r.randint(1, min(n, m)))))
    assert len(cases) == 40, len(cases)   # catalog.json 登记了 0..39 共 40 组
    return cases

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert all(valid(c) for c in cases)
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
