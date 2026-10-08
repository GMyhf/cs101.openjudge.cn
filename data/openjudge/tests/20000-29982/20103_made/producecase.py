import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20103 statistics, Accepted solution 43490046.\n# Source: http://cs101.openjudge.cn/practice/solution/43490046/\n# Statistics: http://cs101.openjudge.cn/practice/20103/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nm,l=[-float("inf")],[0]\nfor i in range(n):\n    mi,li=map(int,input().split())\n    m.append(mi)\n    l.append(li)\nm.append(float("inf"))\nl.append(0)\nans=0\nend=-float("inf")\nfor i in range(1,n+1):\n    if m[i-1]<m[i]-l[i] and end<m[i]-l[i] and  m[i]+l[i]<m[i+1]:\n        ans+=1\n        end=m[i]+l[i]\nprint(ans)\n'
SAMPLE='2\n1 3\n3 1\n'
GENERATOR_NAME='g20103'
def g20103(r):
    n = r.randint(2, 15)
    marks = sorted(r.sample(range(1, 200), n))
    return f"{n}\n" + "\n".join(f"{x} {r.randint(1, 30)}" for x in marks) + "\n"

def valid(text):
    """题面：首行 n（1<=n<=1e5），接着 n 行 "mi li"，整数，li>0，m1<m2<...<mn。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0] != str(int(lines[0])):
        return False
    n = int(lines[0])
    if not 1 <= n <= 100000 or len(lines) != n + 1:
        return False
    prev = None
    for row in lines[1:]:
        tok = row.split(" ")
        if len(tok) != 2:
            return False
        try:
            m, l = int(tok[0]), int(tok[1])
        except ValueError:
            return False
        if tok[0] != str(m) or tok[1] != str(l) or l <= 0:
            return False
        if prev is not None and m <= prev:
            return False
        prev = m
    return True


def _fmt(ms, ls):
    return f"{len(ms)}\n" + "\n".join(f"{m} {l}" for m, l in zip(ms, ls)) + "\n"


def g_big(r, n, lo, gapmax, mode):
    """mode: 'mix' 随机；'chain' 相邻区间大量互相重叠，考贪心选择。
    相邻两段若右端点恰等于下一段左端点（"相接算不算重叠"有歧义），把后一段 l 加 1 避开。"""
    ms, x = [], lo
    for _ in range(n):
        x += r.randint(1, gapmax)
        ms.append(x)
    ls = []
    for i in range(n):
        left = ms[i] - ms[i - 1] if i else gapmax
        right = ms[i + 1] - ms[i] if i + 1 < n else gapmax
        room = min(left, right)
        if mode == "chain":
            l = r.randint(max(1, room // 2), max(1, room - 1)) if r.random() < 0.85 else r.randint(1, room + 5)
        else:
            l = r.randint(1, max(1, room * 3 // 2))
        if i and ms[i - 1] + ls[-1] == ms[i] - l:
            l += 1
        ls.append(l)
    return _fmt(ms, ls)


def build_extra():
    r = random.Random(20103 * 3)
    return [
        "1\n0 5\n",                                      # 单个路标必然可开
        "1\n-1000000000 1000000000\n",
        "2\n1 2\n3 1\n",                                # 端点恰压到另一路标 -> 第一份不合法
        "3\n0 3\n5 3\n10 3\n",                          # 中间一段与两边都重叠：选两端
        "3\n-10 3\n-5 1\n0 3\n",                        # 负坐标
        g_big(r, 100000, 0, 8, "mix"),
        g_big(r, 100000, -100000, 5, "chain"),
        g_big(r, 100000, 0, 3, "chain"),
        g_big(r, 50000, -10 ** 9, 40000, "mix"),
        _fmt([i * 10 for i in range(100000)], [4] * 100000),            # 全部可开 -> n
        _fmt([i * 10 for i in range(100000)], [10] * 100000),           # 全部压到邻居 -> 0
        _fmt([i * 10 for i in range(100000)], [9, 2] * 50000),          # 长短交替、相邻两两重叠
    ]


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
