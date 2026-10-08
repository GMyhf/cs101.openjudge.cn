import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'n=int(input())\na=[0]+list(map(int,input().split()))\nb=[0]+list(map(int,input().split()))\nc=[0]+list(map(int,input().split()))\ndp=[[0]*(n+1) for _ in range(2)]\ndp[0][1],dp[1][1]=a[1],b[1]\nfor i in range(2,n+1):\n    dp[0][i]=max(dp[0][i-1]+b[i],dp[1][i-1]+a[i])\n    dp[1][i]=max(dp[0][i-1]+c[i],dp[1][i-1]+b[i])\nprint(dp[0][n])'
SAMPLE = '4\n1 2 2 4\n4 3 3 1\n2 1 1 2\n'
GENERATOR_NAME = 'g4150'
def valid(text):
    """题面契约：第一行 N（1<=N<=10000）；随后三行各 N 个整数 a、b、c，取值 1..10000。"""
    lines = text.split("\n")
    while lines and lines[-1].strip() == "":
        lines.pop()
    if len(lines) != 4:
        return False
    try:
        h = lines[0].split()
        if len(h) != 1:
            return False
        n = int(h[0])
        if not 1 <= n <= 10000:
            return False
        for ln in lines[1:]:
            v = [int(x) for x in ln.split()]
            if len(v) != n or not all(1 <= x <= 10000 for x in v):
                return False
    except ValueError:
        return False
    return True


def g4150(r, plan):
    n, kind = plan
    if isinstance(n, tuple):
        n = r.randint(*n)
    if kind == "max":
        z = [[10000] * n for _ in range(3)]
    elif kind == "one":
        z = [[1] * n for _ in range(3)]
    elif kind == "bigc":      # c 远大于 a、b：尽量让中间的人后坐
        z = [[r.randint(1, 100) for _ in range(n)], [r.randint(1, 100) for _ in range(n)],
             [r.randint(9000, 10000) for _ in range(n)]]
    elif kind == "biga":      # a 远大于其余
        z = [[r.randint(9000, 10000) for _ in range(n)], [r.randint(1, 100) for _ in range(n)],
             [r.randint(1, 100) for _ in range(n)]]
    elif kind == "bigb":
        z = [[r.randint(1, 100) for _ in range(n)], [r.randint(9000, 10000) for _ in range(n)],
             [r.randint(1, 100) for _ in range(n)]]
    elif kind == "small":     # 小值域，平局多
        z = [[r.randint(1, 3) for _ in range(n)] for _ in range(3)]
    else:
        z = [[r.randint(1, 10000) for _ in range(n)] for _ in range(3)]
    return f"{n}\n" + "\n".join(" ".join(map(str, x)) for x in z) + "\n"


PLAN = [
    (1, "rand"), (1, "max"), (2, "rand"), (2, "bigc"), (3, "bigc"), (3, "rand"),
    ((4, 7), "rand"), ((4, 7), "small"), ((4, 7), "bigc"), ((4, 7), "biga"), ((4, 7), "bigb"),
    ((5, 7), "rand"), ((5, 7), "small"), ((5, 7), "rand"), ((8, 20), "rand"), ((8, 20), "small"),
    ((20, 100), "rand"), ((20, 100), "bigc"), ((100, 1000), "rand"), ((100, 1000), "small"),
    ((1000, 5000), "rand"), ((1000, 5000), "biga"), ((1000, 5000), "bigb"), ((1000, 5000), "bigc"),
    (9999, "rand"), (10000, "rand"), (10000, "rand"), (10000, "max"), (10000, "one"),
    (10000, "bigc"), (10000, "biga"), (10000, "bigb"), (10000, "small"), (10000, "rand"),
    (6, "small"), (7, "rand"), (7, "bigc"), (4, "biga"), (10000, "rand"),
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
    cases=[SAMPLE]+[g4150(random.Random(seed), PLAN[seed-1]) for seed in range(1, 40)]
    assert all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
