import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/19947 statistics, Accepted solution 51286241.\n# Source: http://cs101.openjudge.cn/practice/solution/51286241/\n# Statistics: http://cs101.openjudge.cn/practice/19947/statistics/\n# License: not declared on submission page; no license inferred\nn = int(input())\nl = [int(x) for x in input().split()]\nl.sort()\na = sum(l)\nb = l[-1]\nif a % 2 == 1:\n    print('NO')\nelse:\n    if a >= 2*b:\n        print('YES')\n    else:\n        print('NO')\n"
LANGUAGE='Python3'
SAMPLE='3\n1 2 3\n'
GENERATOR_NAME='g19947'
def g19947(r):
    n=r.randint(2,30); return f"{n}\n"+" ".join(str(r.randint(1,1000)) for _ in range(n))+"\n"

def valid(text):
    """题面契约：首行 n，2<=n<=10^5；第二行恰 n 个整数 ai，1<=ai<=10^9。"""
    try:
        if not text.endswith("\n"):
            return False
        lines = text[:-1].split("\n")
        if len(lines) != 2:
            return False
        n = int(lines[0])
        if not 2 <= n <= 10**5:
            return False
        a = lines[1].split(" ")
        if len(a) != n:
            return False
        return all(1 <= int(x) <= 10**9 for x in a)
    except ValueError:
        return False


def _case(a):
    return f"{len(a)}\n" + " ".join(map(str, a)) + "\n"


def extra_cases():
    r = random.Random(199470)
    def big(n, hi, parity):
        """n 个随机数，调整最后一个使总和奇偶性为 parity，且最大值不超过其余之和。"""
        a = [r.randint(1, hi) for _ in range(n)]
        if sum(a) % 2 != parity:
            a[-1] += 1 if a[-1] < hi else -1
        r.shuffle(a)
        return a
    def dominant(n, hi, extra):
        """最大值 = 其余之和 + extra（extra=0 时恰好 YES 的边界）。"""
        rest = [r.randint(1, hi) for _ in range(n - 1)]
        a = rest + [sum(rest) + extra]
        r.shuffle(a)
        return a
    cases = [
        "4\n2 5 3 1\n",                 # 题面样例 2
        "4\n2 8 3 1\n",                 # 题面样例 3
        "2\n7 7\n",                     # 最小 n，YES
        "2\n7 8\n",                     # 最小 n，NO
        "2\n1000000000 1000000000\n",
        "5\n1000000000 1000000000 1000000000 1000000000 200000000\n",  # 32 位求和溢出
        "3\n1 1 1000000000\n",          # 和为偶但最大值过大
        _case(dominant(1000, 10**5, 0)),     # 最大值恰为其余之和，YES
        _case(dominant(1000, 10**5, 2)),     # 和为偶但最大值超出，NO
        _case(dominant(10, 10**8, 1)),       # 和为奇且最大值超出
        _case(big(10**5, 10**8, 0)),         # n 上限，和为偶，YES
        _case(big(10**5, 10**8, 1)),         # n 上限，和为奇，NO
        _case([10**9] * 90000),              # 和 9e13，需 64 位
        _case([1] * 10**5),
        _case([1] * 99999),
        _case(dominant(10**5, 10**4, 0)),    # 大规模边界 YES
        _case(dominant(10**5, 10**4, 2)),    # 大规模边界 NO
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
