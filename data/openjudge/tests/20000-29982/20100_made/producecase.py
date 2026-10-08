import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20100 statistics, Accepted solution 43253417.\n# Source: http://cs101.openjudge.cn/practice/solution/43253417/\n# Statistics: http://cs101.openjudge.cn/practice/20100/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nv=list(map(int,input().split()))\nr=list(map(int,input().split()))\nt=list(map(int,input().split()))\nvm=0\ntm=1<<30\ncnt=0\nfor i in range(n-1):\n    v[i]/=t[i]\nfor i in range(n-1):\n    if (v[i]>vm or t[i]<tm) and t[i]<r[i]:\n        cnt+=1\n    vm=max(vm,v[i])\n    tm=min(tm,t[i])\nprint(cnt)\n'
SAMPLE='4\n6 6 6\n3 4 5\n1 4 6\n'
GENERATOR_NAME='g20100'
def g20100(r):
    n = r.randint(2, 10)
    distances = [r.randint(1, 10000) for _ in range(n - 1)]
    record = [r.randint(1, 10000) for _ in range(n - 1)]
    monster = [r.randint(1, 10000) for _ in range(n - 1)]
    return f"{n}\n{' '.join(map(str, distances))}\n{' '.join(map(str, record))}\n{' '.join(map(str, monster))}\n"

def valid(text):
    """题面：首行 n（0<n<=2000）；第二、三、四行各 n-1 个整数 di、ti、ai，均在 (0, 10000]。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 4 or not lines[0].isdigit() or lines[0] != str(int(lines[0])):
        return False
    n = int(lines[0])
    if not 1 <= n <= 2000:
        return False
    for row in lines[1:]:
        tok = row.split(" ") if row else []
        if len(tok) != n - 1:
            return False
        if not all(t.isdigit() and t == str(int(t)) and 1 <= int(t) <= 10000 for t in tok):
            return False
    return True


def _fmt(d, t, a):
    return f"{len(d) + 1}\n{' '.join(map(str, d))}\n{' '.join(map(str, t))}\n{' '.join(map(str, a))}\n"


def g_trend(r, n):
    """怪先生越游越快（时间递减或速度递增），制造大量打破纪录与相等的平局。"""
    d, t, a = [], [], []
    cur = 10000
    for _ in range(n - 1):
        di = r.randint(1, 10000)
        cur = max(1, cur - r.choice([0, 0, 1, 2, 5]))
        ai = cur if r.random() < 0.6 else r.randint(1, 10000)
        ti = r.choice([ai, ai + 1, max(1, ai - 1), r.randint(1, 10000)])
        ti = min(ti, 10000)
        d.append(di); t.append(ti); a.append(ai)
    return _fmt(d, t, a)


def g_speed(r, n):
    """时间不创新低、速度创新高：只有条件 2 成立（含相等速度的平局）。"""
    d, t, a = [], [], []
    for i in range(n - 1):
        ai = 10000 - i // 2 if i else 5000
        ai = max(ai, 5000)
        di = min(10000, 1 + i * 5)
        d.append(di); a.append(ai); t.append(min(10000, ai + r.randint(0, 1)))
    return _fmt(d, t, a)


def build_extra():
    r = random.Random(20100 * 11)
    cases = [
        "2\n5\n3\n2\n",                      # n=2，第一段即打破（前面没有比较对象）
        "2\n5\n3\n3\n",                      # 与纪录相等 -> 不算
        "3\n4 8\n10 10\n2 4\n",               # 速度相等（4/2 与 8/4），时间未创新低 -> 只第一段
        "4\n1 2 3\n10 10 10\n5 5 5\n",        # 时间相等、速度递增
    ]
    for n in (2000, 2000, 1999, 1500):
        cases.append(g_trend(r, n))
    cases.append(g_speed(r, 2000))
    d = [r.randint(1, 10000) for _ in range(1999)]
    t = [r.randint(1, 10000) for _ in range(1999)]
    a = [r.randint(1, 10000) for _ in range(1999)]
    cases.append(_fmt(d, t, a))
    cases.append(_fmt([10000] * 1999, [10000] * 1999, [1] * 1999))      # 全相等：只第一段算
    cases.append(_fmt([1] * 1999, [1] * 1999, [10000] * 1999))          # 一次都没有
    return cases


def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases += build_extra()
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
