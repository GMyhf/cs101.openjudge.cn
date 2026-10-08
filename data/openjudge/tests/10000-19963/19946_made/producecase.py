import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19946 statistics, Accepted solution 51285749.\n# Source: http://cs101.openjudge.cn/practice/solution/51285749/\n# Statistics: http://cs101.openjudge.cn/practice/19946/statistics/\n# License: not declared on submission page; no license inferred\nm, n = map(int, input().split())\nworkers = [int(x) for x in input().split()]\nhamburgers = [int(x) for x in input().split()]\nworkers.sort()\nhamburgers.sort()\ni, j, res = 0, 0, 0\nwhile i < m and j < n:\n    if workers[i] >= hamburgers[j]:\n        res += 1\n        i += 1\n        j += 1\n    else:\n        i += 1\nprint(res)\n'
LANGUAGE='Python3'
SAMPLE='2 2\n1 2\n2 1\n'
GENERATOR_NAME='g19946'
def g19946(r):
    m,n=r.randint(1,15),r.randint(1,15); return f"{m} {n}\n"+" ".join(str(r.randint(1,50)) for _ in range(m))+"\n"+" ".join(str(r.randint(1,50)) for _ in range(n))+"\n"

def _ints(line, k):
    parts = line.split(" ")
    if len(parts) != k:
        raise ValueError
    return [int(x) for x in parts]


def valid(text):
    """题面契约：首行 m n（m 个工人、n 个产品）；第二行恰 m 个整数（熟练度）；
    第三行恰 n 个整数（难度）。题面未给 m、n 与取值的上限。"""
    try:
        if not text.endswith("\n"):
            return False
        lines = text[:-1].split("\n")
        if len(lines) != 3:
            return False
        m, n = _ints(lines[0], 2)
        if m < 1 or n < 1:
            return False
        _ints(lines[1], m)
        _ints(lines[2], n)
        return True
    except ValueError:
        return False


def _case(ws, hs):
    return f"{len(ws)} {len(hs)}\n" + " ".join(map(str, ws)) + "\n" + " ".join(map(str, hs)) + "\n"


def extra_cases():
    r = random.Random(199460)
    rnd = lambda k, lo, hi: [r.randint(lo, hi) for _ in range(k)]
    cases = [
        "8 5\n1 2 3 4 5 6 7 8\n5 6 7 8 9\n",       # 题面样例 2
        "4 3\n11 12 13 14\n21 22 23\n",             # 题面样例 3（答案 0）
        "1 1\n5\n5\n",                              # 熟练度恰等于难度
        "1 1\n4\n5\n",
        "2 2\n5 1\n1 5\n",                          # 按输入顺序贪心会错
        "3 3\n7 7 7\n7 7 7\n",                      # 全相等
        _case(rnd(1, 1, 10**9), rnd(5000, 1, 10**9)),
        _case(rnd(5000, 1, 10**9), rnd(1, 1, 10**9)),
        _case(rnd(5000, 1, 10**9), rnd(5000, 1, 10**9)),
        _case(rnd(5000, 1, 100), rnd(3000, 1, 100)),   # 大量重复值
        _case(rnd(3000, 1, 100), rnd(5000, 1, 100)),
        _case(rnd(4000, 500, 1000), rnd(4000, 1, 500)),  # 全部可做，答案 min(m,n)
        _case(rnd(4000, 1, 500), rnd(4000, 501, 1000)),  # 全不可做，答案 0
    ]
    return cases


def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/'main.py'
        src.write_text(REFERENCE); cmd=[sys.executable,str(src)]
        if LANGUAGE=="G++":
            exe=d/"main"; subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],check=True)
            cmd=[str(exe)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=extra_cases()
    assert len(set(cases))==len(cases), "存在重复测试组"
    for i,text in enumerate(cases):
        assert valid(text), i
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
