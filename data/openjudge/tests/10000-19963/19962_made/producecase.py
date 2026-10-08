import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19962 statistics, Accepted solution 52530564.\n# Source: http://cs101.openjudge.cn/practice/solution/52530564/\n# Statistics: http://cs101.openjudge.cn/practice/19962/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nlis=list(map(int,input().split()))\nlis=sorted(lis)\nl=0\nr=n-1\nans=0\nwhile r>=l:\n    ans=ans+lis[r]-lis[l]\n    l+=1\n    r-=1\nprint(ans)\n'
LANGUAGE='Python3'
SAMPLE='4\n6 2 9 1\n'
GENERATOR_NAME='g19962'
def g19962(r):
    # 题面数据范围：1 <= N <= 100000，1 <= Ai <= 100000（坐标不为负）。
    n=r.randint(2,30); return f"{n}\n"+" ".join(str(r.randint(1,100000)) for _ in range(n))+"\n"

def valid(text):
    """题面契约：首行 N，1<=N<=100000；第二行恰 N 个整数 Ai，1<=Ai<=100000。"""
    try:
        if not text.endswith("\n"):
            return False
        lines = text[:-1].split("\n")
        if len(lines) != 2:
            return False
        n = int(lines[0])
        if not 1 <= n <= 100000:
            return False
        a = lines[1].split(" ")
        if len(a) != n:
            return False
        return all(1 <= int(x) <= 100000 for x in a)
    except ValueError:
        return False


def _case(a):
    return f"{len(a)}\n" + " ".join(map(str, a)) + "\n"


def extra_cases():
    r = random.Random(199620)
    rnd = lambda k, lo, hi: [r.randint(lo, hi) for _ in range(k)]
    skew = [r.randint(1, 10) for _ in range(800)] + [r.randint(90000, 100000) for _ in range(200)]
    r.shuffle(skew)
    half = [1] * 50000 + [100000] * 50000
    r.shuffle(half)
    cases = [
        "6\n6 2 9 1 8 7\n",          # 题面样例 2
        "5\n1 2 3 4 5\n",            # 题面样例 3
        "1\n100000\n",               # N=1，答案 0
        "2\n1 100000\n",
        _case([42] * 1000),           # 全部重合
        _case(skew),                  # 偏态分布：用平均数代替中位数会错
        _case(rnd(100000, 1, 100000)),
        _case(rnd(99999, 1, 100000)),
        _case(half),                  # 答案 4999950000，超出 32 位
        _case(sorted(rnd(100000, 1, 100000))),
        _case(sorted(rnd(100000, 1, 100000), reverse=True)),
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
