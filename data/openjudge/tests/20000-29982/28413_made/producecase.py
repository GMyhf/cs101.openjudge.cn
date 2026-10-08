import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/28413/\n# Accepted submission: 52720583\n# Source: http://cs101.openjudge.cn/practice/solution/52720583/\n# License: not declared on the submission page; no license is inferred.\n\nfor _ in range(int(input())):\n    n = int(input())\n    names = []\n    edges = [[] for _ in range(n)]\n    for i in range(n):\n        s = input().split()\n        names.append(s[0])\n        for j in s[1:]:\n            j = int(j)-1\n            edges[i].append(j)\n    for i in range(n):\n        edges[i].sort()        \n    ans = []\n    part = []\n    for i in range(n):\n        cur = []\n        cur.append(names[i])\n        for ci in edges[i]:\n            cur.extend(part[ci])\n        part.append(cur)\n        ans.extend(part[-1])\n    print(len(ans))\n    print(*ans)'
SAMPLE='3\n3\nA\nB 1\nC 2 1\n4\nA\nB 1\nC 2\nD 3\n5\nTakamatsu\nKaname\nShiina 2\nChihaya 1\nNagasaki 1 4\n'
EXTRA_CASE=None
GENERATOR_NAME='g28413'
def valid(text):
    """题面契约：首行正整数 T；每组首行正整数 n，随后 n 行：姓名（字母数字，非空）+ 零个或若干序号，
    第 i 名成员（从 1 计）的序号都在 1..i-1（严格小于自己）。题面未给 T、n 上限，只核格式与结构。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def posint(s):
        return s.isdigit() and s[0] != "0"
    p = 0
    if not lines or not posint(lines[0]):
        return False
    t = int(lines[0]); p = 1
    for _ in range(t):
        if p >= len(lines) or not posint(lines[p]):
            return False
        n = int(lines[p]); p += 1
        if p + n > len(lines):
            return False
        for i in range(1, n + 1):
            row = lines[p]; p += 1
            toks = row.split(" ")
            if not toks[0] or not toks[0].isascii() or not toks[0].isalnum():
                return False
            for x in toks[1:]:
                if not posint(x) or int(x) >= i:
                    return False
    return p == len(lines)


ALNUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def names_for(r, n):
    out, used = [], set()
    while len(out) < n:
        s = "".join(r.choice(ALNUM) for _ in range(r.randint(1, 8)))
        if s not in used:
            used.add(s); out.append(s)
    return out


def g28413(r):
    # 序号列表故意打乱顺序（题面样例 "C 2 1" 即为乱序），卡掉不排序直接展开的写法；
    # 姓名随机，卡掉按姓名而非编号比字典序的写法。
    t = r.randint(1, 6); rows = [str(t)]
    for _ in range(t):
        mode = r.random()
        if mode < 0.12:
            n = 1
        elif mode < 0.25:
            n = r.randint(8, 13)          # 每人依赖全部前人：答案 2^n-1
        elif mode < 0.38:
            n = r.randint(30, 120)        # 链：每人依赖前一人
        else:
            n = r.randint(2, 40)
        names = names_for(r, n); rows.append(str(n))
        for i in range(n):
            if mode < 0.12:
                deps = []
            elif mode < 0.25:
                deps = list(range(1, i + 1))
            elif mode < 0.38:
                deps = [i] if i else []
            else:
                deps = r.sample(range(1, i + 1), r.randint(0, min(i, 4))) if i else []
            r.shuffle(deps)
            rows.append(names[i] + (" " + " ".join(map(str, deps)) if deps else ""))
    return "\n".join(rows) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+([EXTRA_CASE] if EXTRA_CASE else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
