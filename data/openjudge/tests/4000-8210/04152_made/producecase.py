import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = "import sys\ncontent=sys.stdin.read().split()\nptr=0\nwhile ptr<len(content):\n    m=int(content[ptr])\n    num=content[ptr+1]\n    ptr+=2\n    #dp[i][j]表示放i个加号，前j+1位数的最小和，dp[i][j]=max(dp[i][j],dp[i-1][j-t]+int(num[j-t:j]))\n    dp=[[float('inf')]*len(num) for _ in range(m+1)]\n    for j in range(len(num)):\n        dp[0][j]=int(num[:j+1])\n    for i in range(1,m+1):\n        for j in range(len(num)):\n            for t in range(1,j-i+2):\n                dp[i][j]=min(dp[i][j],dp[i-1][j-t]+int(num[j-t+1:j+1]))\n    print(dp[m][len(num)-1])"
SAMPLE = '2\n123456\n1\n123456\n4\n12345\n'
GENERATOR_NAME = 'g4152'
def valid(text):
    """题面契约：不超过 15 组数据，每组两行：第一行 m（0<=m<=50），第二行 n 个 1..9 的数字
    （n<=50，且 m<=n-1），数字连写成一个串。"""
    lines = text.split("\n")
    while lines and lines[-1].strip() == "":
        lines.pop()
    if not lines or len(lines) % 2 or len(lines) // 2 > 15:
        return False
    for k in range(0, len(lines), 2):
        a, b = lines[k].split(), lines[k + 1].split()
        if len(a) != 1 or len(b) != 1:
            return False
        try:
            m = int(a[0])
        except ValueError:
            return False
        s = b[0]
        if not 0 <= m <= 50 or not 1 <= len(s) <= 50:
            return False
        if any(ch not in "123456789" for ch in s) or m > len(s) - 1:
            return False
    return True


def _digits(r, n, kind):
    if kind == "nine":
        return "9" * n
    if kind == "one":
        return "1" * n
    if kind == "small":
        return "".join(r.choice("12") for _ in range(n))
    return "".join(str(r.randint(1, 9)) for _ in range(n))


def g4152(r, plan):
    count, (nlo, nhi), mode, kind = plan
    z = []
    for _ in range(count):
        n = r.randint(nlo, nhi)
        if mode == "zero":
            m = 0
        elif mode == "full":
            m = n - 1
        elif mode == "few":
            m = r.randint(0, min(3, n - 1))
        else:
            m = r.randint(0, n - 1)
        z += [str(m), _digits(r, n, kind)]
    return "\n".join(z) + "\n"


# (组数, n 范围, m 取法, 数字取法)
PLAN = [
    (1, (1, 1), "zero", "rand"), (3, (1, 3), "any", "rand"), (5, (2, 6), "any", "rand"),
    (5, (4, 10), "any", "rand"), (5, (4, 10), "full", "rand"), (5, (4, 10), "zero", "rand"),
    (8, (8, 14), "any", "rand"), (8, (8, 14), "few", "rand"), (8, (8, 14), "any", "small"),
    (10, (10, 15), "any", "rand"), (15, (1, 15), "any", "rand"), (15, (12, 15), "few", "rand"),
    (15, (15, 15), "any", "rand"), (15, (1, 15), "any", "small"), (5, (20, 30), "any", "rand"),
    (5, (30, 40), "any", "rand"), (5, (40, 50), "any", "rand"), (1, (50, 50), "zero", "rand"),
    (1, (50, 50), "full", "rand"), (3, (50, 50), "few", "rand"), (5, (50, 50), "any", "rand"),
    (15, (50, 50), "any", "rand"), (15, (50, 50), "few", "rand"), (15, (50, 50), "any", "nine"),
    (15, (50, 50), "any", "one"), (15, (50, 50), "zero", "nine"), (15, (50, 50), "full", "nine"),
    (15, (45, 50), "any", "small"), (15, (1, 50), "any", "rand"), (15, (1, 50), "few", "rand"),
    (15, (50, 50), "any", "rand"), (15, (50, 50), "any", "rand"), (15, (25, 50), "any", "rand"),
    (10, (1, 5), "any", "rand"), (15, (2, 2), "any", "rand"), (15, (3, 9), "full", "rand"),
    (15, (40, 50), "few", "nine"), (15, (50, 50), "any", "small"), (15, (49, 50), "any", "rand"),
]

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g4152(random.Random(seed), PLAN[seed-1]) for seed in range(1, 40)]
    assert all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
