import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19965 statistics, Accepted solution 43122751.\n# Source: http://cs101.openjudge.cn/practice/solution/43122751/\n# Statistics: http://cs101.openjudge.cn/practice/19965/statistics/\n# License: not declared on submission page; no license inferred\ndef f(a,b):\n    if a%b==0:\n        return a//b\n    else:\n        return a//b+1\na,b,c=map(int,input().split())\nwhile b<=a and c>=f(a,b):\n    c-=f(a, b)\n    b+=a//b\nprint(b)\n'
LANGUAGE='Python3'
SAMPLE='5 2 10\n'
GENERATOR_NAME='g19965'
def g19965(r): return f"{r.randint(1,10000)} {r.randint(1,10000)} {r.randint(1,10000)}\n"

def valid(text):
    """题面契约：一行三个整数 A B C，单个空格分隔，均为不超过 10000 的正整数。"""
    try:
        if not text.endswith("\n"):
            return False
        lines = text[:-1].split("\n")
        if len(lines) != 1:
            return False
        parts = lines[0].split(" ")
        if len(parts) != 3:
            return False
        return all(1 <= int(x) <= 10000 for x in parts)
    except ValueError:
        return False


def _need(a, b, rounds):
    """前 rounds 个战斗期累计要吃的肉块数（只在 b<=a 的范围内有意义）。"""
    total = 0
    for _ in range(rounds):
        if b > a:
            break
        total += -(-a // b)
        b += a // b
    return total


def extra_cases():
    r = random.Random(199650)
    cases = [
        "10 1 10\n",       # 题面样例 2
        "100 1 50\n",      # 题面样例 3
        "1 1 1\n",
        "1 1 10000\n",
        "10000 1 10000\n",  # 肉恰好够一次
        "10000 1 9999\n",   # 差一块
        "5 6 100\n",        # 初始战斗力已超过容量
        "7 7 1\n",          # B==A
        "10000 2 10000\n",
        "10000 10000 10000\n",
        "9999 3 10000\n",
    ]
    while len(cases) < 31:
        a = r.randint(50, 10000)
        b = r.randint(1, max(1, a // 20))
        k = r.randint(1, 12)
        c = _need(a, b, k) + r.choice([0, -1])   # 恰好够第 k 期 / 差一块
        if 1 <= c <= 10000:
            case = f"{a} {b} {c}\n"
            if case not in cases:
                cases.append(case)
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
