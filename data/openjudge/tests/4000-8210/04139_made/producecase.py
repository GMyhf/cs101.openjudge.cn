import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'a,b,c=map(int,input().split())\nresult=0\nfor k in range(c//b+1):\n    if (c-b*k)%a==0:\n        result+=1\nprint(result)'
SAMPLE = '2 3 18\n'


def valid(text):
    """题面：一行三个正整数 a b c，单个空格分隔，每个数均不大于 1000。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    t = text[:-1].split(" ")
    if len(t) != 3 or not all(x.isdigit() and x[0] != "0" for x in t):
        return False
    return all(1 <= int(x) <= 1000 for x in t)


def g4139(r):
    """原生成器形状（a,b≤30），但把 c 限制在 [1,1000] 内。"""
    while True:
        a, b = r.randint(1, 30), r.randint(1, 30); k = r.randint(0, 20)
        c = a * r.randint(0, k + 1) + b * k
        if 1 <= c <= 1000:
            return f"{a} {b} {c}\n"


FIXED = [
    "1 1 1\n", "1 1 1000\n", "1000 1000 1000\n", "1000 1 1000\n", "1 1000 1000\n",
    "1000 1000 999\n", "2 4 7\n", "6 10 1000\n", "999 998 1000\n", "7 11 5\n",
    "3 3 999\n", "1 2 1000\n", "500 250 1000\n", "13 17 1000\n", "997 991 1000\n",
]


def gen(i, r):
    if i <= 9:
        return g4139(r)
    if i < 10 + len(FIXED):
        return FIXED[i - 10]
    # 全值域随机：a、b 取到 1000，c 取到 1000，含无解（答案 0）的组
    a, b, c = r.randint(1, 1000), r.randint(1, 1000), r.randint(1, 1000)
    if i % 3 == 0:
        a, b = r.randint(1, 40), r.randint(1, 40)
    if i % 5 == 0:
        g = r.randint(2, 9); a, b = g * r.randint(1, 100), g * r.randint(1, 100); c = g * r.randint(1, 1000 // g) + r.randint(0, 1)
    return f"{a} {b} {c}\n"


def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[gen(seed, random.Random(seed)) for seed in range(1, 40)]
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
