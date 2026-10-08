import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/20974/\n# Accepted submission: 52686810\n# Source: http://cs101.openjudge.cn/practice/solution/52686810/\n# License: not declared on the submission page; no license is inferred.\n\nm, s, c = map(int, input().split())\ncows = [int(input()) for _ in range(c)]\nif c == 0:\n    print(0)\nelse:\n    cows.sort()\n    if m >= c:\n        print(c)\n    else:\n        total = cows[-1] - cows[0] + 1\n        gaps = [cows[i] - cows[i-1] - 1 for i in range(1, c)]\n        gaps.sort(reverse=True)\n        total -= sum(gaps[:m-1])\n        print(total)'
SAMPLE='4 50 18\n3 \n4 \n6 \n8 \n14\n15 \n16 \n17 \n21\n25 \n26 \n27 \n30 \n31 \n40 \n41 \n42 \n43\n'
GENERATOR_NAME='g20974'


def valid(text):
    """题面：第一行 m s c，1<=m<=50，1<=c<=s<=200；接下来 c 行各一个整数（牛棚编号 1..s，互不相同）。"""
    try:
        lines = text.split('\n')
        while lines and lines[-1].strip() == '':
            lines.pop()
        if not lines:
            return False
        head = lines[0].split()
        if len(head) != 3:
            return False
        m, s, c = map(int, head)
        if not (1 <= m <= 50 and 1 <= c <= s <= 200):
            return False
        if len(lines) != 1 + c:
            return False
        cows = []
        for ln in lines[1:]:
            t = ln.split()
            if len(t) != 1:
                return False
            v = int(t[0])
            if not 1 <= v <= s:
                return False
            cows.append(v)
        return len(set(cows)) == c
    except ValueError:
        return False


def fmt(m, s, cows):
    return f"{m} {s} {len(cows)}\n" + "\n".join(map(str, cows)) + "\n"


def g20974(r):
    s = r.randint(1, 200)
    c = r.randint(1, s) if r.random() < .6 else r.randint(1, min(50, s))
    cows = r.sample(range(1, s + 1), c)
    if r.random() < .3:
        cows.sort()
    m = r.randint(1, 50) if r.random() < .3 else r.randint(1, max(1, min(50, c - 1)))
    return fmt(m, s, cows)


def specials():
    r = random.Random(20974)
    out = []
    out.append(fmt(1, 1, [1]))                                   # 最小规模
    out.append(fmt(1, 200, [200, 1]))                            # 一块板覆盖两端，逆序给出
    full = list(range(1, 201)); r.shuffle(full)
    out.append(fmt(1, 200, full))                                # c=s=200，m=1
    full = list(range(1, 201)); r.shuffle(full)
    out.append(fmt(50, 200, full))                               # c=s=200，m=50
    odd = list(range(1, 201, 2)); r.shuffle(odd)
    out.append(fmt(50, 200, odd))                                # 间隔全为 1，m<c
    out.append(fmt(50, 200, sorted(r.sample(range(1, 201), 50))[::-1]))   # m==c，逆序
    out.append(fmt(49, 200, r.sample(range(1, 201), 50)))       # m==c-1
    out.append(fmt(50, 200, r.sample(range(1, 201), 49)))       # m>c
    out.append(fmt(2, 200, r.sample(range(1, 201), 199)))
    out.append(fmt(7, 200, r.sample(range(1, 201), 150)))
    out.append(fmt(3, 200, r.sample(range(1, 201), 20)))
    out.append(fmt(50, 200, [100]))
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g20974(random.Random(s)) for s in range(1, 40)]+specials()
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
