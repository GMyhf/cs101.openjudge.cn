import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'import math\na,b = map(int, input().split())\nprint(math.gcd(a,b))'
SAMPLE = '6 9\n'
GENERATOR_NAME = 'g7592'
def valid(text):
    """题面契约：一行两个正整数，均 < 1,000,000,000。"""
    if not text.endswith('\n') or text.count('\n') != 1:
        return False
    t = text[:-1].split(' ')
    return len(t) == 2 and all(x.isdigit() and x == str(int(x)) and 1 <= int(x) < 10**9 for x in t)


MAXV = 10**9 - 1
FIB = [1, 2]
while FIB[-1] + FIB[-2] < 10**9:
    FIB.append(FIB[-1] + FIB[-2])


def g7592(r, i=0):
    if i <= 12:
        return f"{r.randint(1,MAXV)} {r.randint(1,MAXV)}\n"
    if i <= 24:
        # 公约数较大：g * 互质的 x、y
        g = r.randint(2, 10**6) if i % 2 else r.randint(10**6, 10**8)
        x, y = r.randint(1, MAXV // g), r.randint(1, MAXV // g)
        if x == y:
            y = max(1, y - 1)
        return f"{g*x} {g*y}\n"
    special = [
        (MAXV, 1), (1, MAXV), (1, 1), (MAXV, MAXV), (999999937, 999999929),   # 两个大质数
        (FIB[-1], FIB[-2]), (FIB[-2], FIB[-1]),                               # 辗转相除步数最多
        (MAXV, 3), (2, MAXV - 1), (536870912, 268435456),                     # 整除关系、2 的幂
        (999999000, 999999), (123456789, 987654321), (735134400, 698377680), (500000000, 999999999), (999999999, 333333333),
    ]
    x, y = special[i - 25]
    return f"{x} {y}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed), seed) for seed in range(1, 40)]
    for i,text in enumerate(cases):
        assert valid(text), i
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
