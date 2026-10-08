import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20091 statistics, Accepted solution 42729047.\n# Source: http://cs101.openjudge.cn/practice/solution/42729047/\n# Statistics: http://cs101.openjudge.cn/practice/20091/statistics/\n# License: not declared on submission page; no license inferred\nfrom math import factorial\n\n\ndef c(n, k):\n    return factorial(n) // (factorial(k) * factorial(n - k))  # 原 AC 代码用 / 走浮点，n 稍大末位全错，改整除\n\n\nt = int(input())\nfor i in range(t):\n    n = int(input())\n    print(int(max(c(n, n // 2), c(n, n // 2 + 1))))\n'
SAMPLE='1\n3\n'
GENERATOR_NAME='g20091'
def g20091(r):
    t = r.randint(3, 20)
    return f"{t}\n" + "\n".join(str(r.randint(3, 1000)) for _ in range(t)) + "\n"

def valid(text):
    """题面：首行整数 t（组数，题面未给上界，按正整数核），接着 t 行，每行整数 n，3<=n<=1000。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0] != str(int(lines[0])):
        return False
    t = int(lines[0])
    if t < 1 or len(lines) != t + 1:
        return False
    return all(x.isdigit() and x == str(int(x)) and 3 <= int(x) <= 1000 for x in lines[1:])


def _case(ns):
    return f"{len(ns)}\n" + "\n".join(map(str, ns)) + "\n"


def build_extra():
    r = random.Random(20091 * 13)
    return [
        _case([1000]),
        _case([999]),
        _case([4]),
        _case(list(range(3, 61))),             # 浮点仍可能碰巧对的小 n 段
        _case(list(range(3, 1001))),           # 全部 n
        _case([r.randint(900, 1000) for _ in range(200)]),
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
