import random
REFERENCE='# External reference: /practice/29940/statistics/\n# Accepted submission: 52265911\n# Source: http://cs101.openjudge.cn/practice/solution/52265911/\n# License: not declared on the submission page; no license is inferred.\n\nn=int(input())\nl=[int(i) for i in input().split()]\nresult=0\nmin_result=0\nfor i in l:\n    result+=i\n    min_result=min(min_result,result)\nif (min_result>=0):\n    print(1)\nelse:\n    print(1-min_result)'
SAMPLE='3\n-100 -200 -300\n'
SAMPLE2='5\n-200 -300 1000 -100 -100\n'
GENERATOR_NAME='g29940'
def _nonzero(r):
    # 题面 1 <= |a_i| <= 1000：抽到 0 就重抽（原生成器会抽到 0，第 6、38 组越界）
    while True:
        v = r.randint(-1000, 1000)
        if v:
            return v


def g29940(r):
    n = r.randint(1, 200); return f"{n}\n" + " ".join(str(_nonzero(r)) for _ in range(n)) + "\n"


def valid(text):
    """题面契约：第一行正整数 n（n <= 100000）；第二行恰 n 个整数，1 <= |a_i| <= 1000。"""
    if not text.endswith("\n"):
        return False
    rows = text[:-1].split("\n")
    if len(rows) != 2:
        return False
    try:
        n = int(rows[0])
        a = [int(t) for t in rows[1].split(" ")]
    except ValueError:
        return False
    if rows[0] != str(n) or not 1 <= n <= 100000 or len(a) != n:
        return False
    return all(1 <= abs(v) <= 1000 for v in a)


def fmt(a):
    return f"{len(a)}\n" + " ".join(map(str, a)) + "\n"


def extra_cases():
    """追加：题面样例 2、n=1 正/负、全营地（答案 1）、n=100000 满规模
    （全 -1000 答案 1e8+1；随机；先补血后大量战斗；前缀和恰回到 0 的边界）。"""
    r = random.Random(299400)
    out = [SAMPLE2, fmt([1000]), fmt([-1000]), fmt([-1]), fmt([1] * 50),
           fmt([5, -5, 5, -5, 5, -6]), fmt([-3, 3, -3, 3])]
    n = 100000
    out.append(fmt([-1000] * n))
    out.append(fmt([1000] * n))
    out.append(fmt([_nonzero(r) for _ in range(n)]))
    out.append(fmt([r.randint(1, 1000) for _ in range(n // 2)] + [-r.randint(1, 1000) for _ in range(n // 2)]))
    out.append(fmt([r.choice([-1000, -999, 998, 1000]) for _ in range(n)]))
    out.append(fmt([1000 if i % 2 == 0 else -1000 for i in range(n)]))
    out.append(fmt([-r.randint(900, 1000) if r.random() < .7 else r.randint(1, 1000) for _ in range(n)]))
    return out

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=extra_cases()
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
