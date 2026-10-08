import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/22548/\n# Accepted submission: 52510538\n# Source: http://cs101.openjudge.cn/practice/solution/52510538/\n# License: not declared on the submission page; no license is inferred.\n\nprice=[int(i) for i in input().split()]\nupstack=[]\nm=0\nfor p in price:\n    while upstack and upstack[-1]>=p:\n        upstack.pop()\n    upstack.append(p)\n    m=max(m,upstack[-1]-upstack[0])\nprint(m)'
SAMPLE='7 1 5 3 6 4\n'
GENERATOR_NAME='g22548'
def g22548(r):
    n=r.randint(2,40); a=[r.randint(0,10000) for _ in range(n)]
    if r.random()<.5: a.sort(reverse=True)
    return " ".join(map(str,a))+"\n"

def valid(text):
    # 题面：由空格分开的若干非负整数，长度不超过 100,000，0 <= a[i] <= 10000（单行）
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    line = text[:-1]
    toks = line.split(" ")
    if not 1 <= len(toks) <= 100000:
        return False
    for t in toks:
        if not t.isdigit() or not t.isascii() or (len(t) > 1 and t[0] == "0"):
            return False
        if not 0 <= int(t) <= 10000:
            return False
    return True

def special_cases():
    r = random.Random(22548)
    N = 100000
    out = []
    out.append("5\n")                                   # n=1，答案 0
    out.append("7 6 5 4 3 1\n")                         # 提示中的单调下降
    out.append(" ".join(str(r.randint(0, 10000)) for _ in range(N)) + "\n")   # 满规模随机
    a = sorted((r.randint(0, 10000) for _ in range(N)), reverse=True)
    out.append(" ".join(map(str, a)) + "\n")            # 满规模不增，答案 0
    # 满规模：全局最大在前、全局最小在后，卡 max-min 写法；中段有一段上升
    a = [10000] + [r.randint(3000, 6000) for _ in range(N - 2)] + [0]
    out.append(" ".join(map(str, a)) + "\n")
    out.append(" ".join(["4321"] * N) + "\n")            # 满规模全相等
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 34)]+special_cases()
    for c in cases: assert valid(c), c[:80]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
