import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/20090 statistics, Accepted solution 42650453.\n# Source: http://cs101.openjudge.cn/practice/solution/42650453/\n# Statistics: http://cs101.openjudge.cn/practice/20090/statistics/\n# License: not declared on submission page; no license inferred\nfor _ in range(int(input())):print((' 1','3971')[(n:=int(input()))>1][n%4])\n"
SAMPLE='1\n2\n'
GENERATOR_NAME='g20090'
def g20090(r):
    q = r.randint(5, 20)
    return f"{q}\n" + "\n".join(str(r.randint(1, 1008612138)) for _ in range(q)) + "\n"

QMAX, NMAX = 10086, 1008612138


def valid(text):
    """题面：首行 q（1<=q<=10086），接着 q 行，每行正整数 n（1<=n<=1008612138）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0] != str(int(lines[0])):
        return False
    q = int(lines[0])
    if not 1 <= q <= QMAX or len(lines) != q + 1:
        return False
    for x in lines[1:]:
        if not x.isdigit() or x != str(int(x)) or not 1 <= int(x) <= NMAX:
            return False
    return True


def _case(ns):
    return f"{len(ns)}\n" + "\n".join(map(str, ns)) + "\n"


def build_extra():
    r = random.Random(20090 * 17)
    return [
        _case([1]),                                   # X1 特判
        _case([NMAX]),
        _case(list(range(1, 201))),                   # 前 200 项逐项核
        _case([NMAX - i for i in range(8)] + [1, 2, 3, 4, 5]),
        _case([r.randint(1, NMAX) for _ in range(QMAX)]),            # 满 q
        _case([r.choice([1, NMAX, r.randint(1, 50), r.randint(1, NMAX)]) for _ in range(QMAX)]),
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
