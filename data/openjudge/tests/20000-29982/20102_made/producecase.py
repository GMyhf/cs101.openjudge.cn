import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20102 statistics, Accepted solution 52482499.\n# Source: http://cs101.openjudge.cn/practice/solution/52482499/\n# Statistics: http://cs101.openjudge.cn/practice/20102/statistics/\n# License: not declared on submission page; no license inferred\nimport math\n\nt = int(input())\nwhile t > 0:\n    t-=1\n    n = int(input())\n    print(1+math.comb(n,2)+math.comb(n,4))\n'
SAMPLE='4\n1\n2\n3\n4\n'
GENERATOR_NAME='g20102'
def g20102(r):
    t = r.randint(5, 20)
    return f"{t}\n" + "\n".join(str(r.randint(1, 1000)) for _ in range(t)) + "\n"

def valid(text):
    """题面：首行整数 t（t<=100000），接着 t 行，每行整数 n（圆上点数，题面未给上界，按正整数核）。
    注：题面样例首行写 5 却只有 4 个 n、4 行输出，第 0 组按 4 组修正。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0] != str(int(lines[0])):
        return False
    t = int(lines[0])
    if not 1 <= t <= 100000 or len(lines) != t + 1:
        return False
    return all(x.isdigit() and x == str(int(x)) and int(x) >= 1 for x in lines[1:])


def _case(ns):
    return f"{len(ns)}\n" + "\n".join(map(str, ns)) + "\n"


def build_extra():
    r = random.Random(20102 * 7)
    return [
        _case([5]),                                  # 卡 2^(n-1) 的找规律写法
        _case([6, 1]),
        _case(list(range(1, 61))),
        _case([1000, 999, 998]),
        _case([r.randint(1, 1000) for _ in range(100000)]),   # 满 t
        _case([r.choice([1, 2, 3, 4, 5, 1000, r.randint(1, 1000)]) for _ in range(100000)]),
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
