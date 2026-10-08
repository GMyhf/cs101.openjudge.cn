import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19948 statistics, Accepted solution 52600565.\n# Source: http://cs101.openjudge.cn/practice/solution/52600565/\n# Statistics: http://cs101.openjudge.cn/practice/19948/statistics/\n# License: not declared on submission page; no license inferred\nn, m = map(int, input().split())\na = list(map(int, input().split()))\na.sort()\n\nif m >= n:\n    print(0)\nelse:\n    diff = [a[i] - a[i-1] for i in range(1, n)]\n    diff.sort()\n    total = a[-1] - a[0]\n    for i in range(m-1):\n        total -= diff[-1 - i]\n    print(total)\n'
LANGUAGE='Python3'
SAMPLE='7 3\n2 7 9 9 16 28 45\n'
GENERATOR_NAME='g19948'
def g19948(r):
    n=r.randint(1,30); m=r.randint(1,n); return f"{n} {m}\n"+" ".join(str(r.randint(1,1000)) for _ in range(n))+"\n"

def valid(text):
    """题面契约：首行 n m，1<=m<=n<=10^5；第二行恰 n 个整数 ri，1<=ri<=10^9。"""
    try:
        if not text.endswith("\n"):
            return False
        lines = text[:-1].split("\n")
        if len(lines) != 2:
            return False
        head = lines[0].split(" ")
        if len(head) != 2:
            return False
        n, m = int(head[0]), int(head[1])
        if not 1 <= m <= n <= 10**5:
            return False
        a = lines[1].split(" ")
        if len(a) != n:
            return False
        return all(1 <= int(x) <= 10**9 for x in a)
    except ValueError:
        return False


def _case(m, a):
    return f"{len(a)} {m}\n" + " ".join(map(str, a)) + "\n"


def extra_cases():
    r = random.Random(199480)
    rnd = lambda k, lo, hi: [r.randint(lo, hi) for _ in range(k)]
    cases = [
        "15 9\n90 73 116 47 400 212 401 244 13 372 248 56 194 482 177\n",  # 题面样例 2
        "1 1\n1000000000\n",
        "2 1\n1 1000000000\n",
        "5 5\n5 4 3 2 1\n",
        _case(1, rnd(10**5, 1, 10**8)),
        _case(10**5, rnd(10**5, 1, 10**8)),
        _case(50000, rnd(10**5, 1, 10**8)),
        _case(99999, rnd(10**5, 1, 10**8)),
        _case(2, rnd(90000, 1, 10**9)),
        _case(777, rnd(90000, 1, 10**9)),
        _case(30000, rnd(10**5, 1, 1000)),     # 大量重复值
        _case(100, [12345678] * 10**5),         # 全相等，答案 0（8 位数，.in 不超过 1MB）
        _case(40, sorted(rnd(10**5, 1, 10**8), reverse=True)),
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
