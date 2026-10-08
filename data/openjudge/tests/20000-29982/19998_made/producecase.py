import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19998 statistics, Accepted solution 52529434.\n# Source: http://cs101.openjudge.cn/practice/solution/52529434/\n# Statistics: http://cs101.openjudge.cn/practice/19998/statistics/\n# License: not declared on submission page; no license inferred\nm,n=map(int,input().split())\nhp=list(map(int,input().split()))+list(map(int,input().split()))\ndef mani():\n    con=False\n    for i in range(14):\n        if hp[i]>=2:\n            hp[i]-=1\n        elif hp[i]==1:\n            hp[i]-=1\n            con=True\n    if con:\n        mani()\n\ndef pan():\n    for i in range(14):\n        if hp[i]>0:\n            return False\n    return True\n\nwhile m>=1 and n>=2:\n    m-=1\n    n-=2\n    mani()\n\nif pan():\n    print("YES")\nelse:\n    print("NO")\n'
SAMPLE='2 10\n3 3 5 2 2 6 4 \n1 1 4 8 8 3 7\n'
GENERATOR_NAME='g19998'
def g19998(r):
    m, n = r.randint(0, 2), r.randint(0, 10)
    if r.random() < .5:
        m, n = 2, 10
        values = [r.randint(1, 3) for _ in range(14)]
    else:
        values = [r.randint(6, 10) for _ in range(14)]
    return f"{m} {n}\n" + "\n".join(
        " ".join(map(str, values[i:i + 7])) for i in (0, 7)
    ) + "\n"

def valid(text):
    """题面契约：第一行 M N（0<=M<=2，0<=N<=10）；接下来 2 行各 7 个整数 1<=x<=10。
    样例第二行带行尾空格，按空白切分时容忍行尾空格。"""
    import re
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 3:
        return False
    tok = [ln.split() for ln in lines]
    if [len(t) for t in tok] != [2, 7, 7] or not all(re.fullmatch(r"\d+", x) for t in tok for x in t):
        return False
    m, n = map(int, tok[0])
    return 0 <= m <= 2 and 0 <= n <= 10 and all(1 <= int(x) <= 10 for x in tok[1] + tok[2])

def clears(m, n, hp):
    """独立模拟：能打出 min(M, N//2) 张亵渎，每张反复 1 点 AOE 直到某轮无随从死亡。"""
    hp = list(hp)
    for _ in range(min(m, n // 2)):
        while True:
            died = any(h == 1 for h in hp if h > 0)
            hp = [h - 1 if h > 0 else 0 for h in hp]
            if not died:
                break
    return all(h == 0 for h in hp)

def gplay(r, m, n, kind):
    """追加组。kind：chain1=血量是 1..k 的连续段（一张清场）；chain2=两段连续、
    中间隔一格（需两张）；gap=中间断档两格以上（两张也不够）；rand=1..10 随机。"""
    if kind == "chain1":
        k = r.randint(1, 10); hp = [r.randint(1, k) for _ in range(14)]
        for v in range(1, k + 1): hp[r.randrange(14)] = v
        while sorted(set(hp)) != list(range(1, k + 1)):
            hp = [r.randint(1, k) for _ in range(14)]
    elif kind == "chain2":
        a = r.randint(1, 6); b = r.randint(a + 2, 10)
        vals = list(range(1, a + 1)) + list(range(a + 2, b + 1))
        hp = vals + [r.choice(vals) for _ in range(14 - len(vals))]; r.shuffle(hp)
    elif kind == "gap":
        a = r.randint(1, 5); b = r.randint(a + 3, 10)
        vals = list(range(1, a + 1)) + list(range(b, 11))
        hp = vals + [r.choice(vals) for _ in range(14 - len(vals))]; r.shuffle(hp)
    else:
        hp = [r.randint(1, 10) for _ in range(14)]
    return f"{m} {n}\n" + " ".join(map(str, hp[:7])) + "\n" + " ".join(map(str, hp[7:])) + "\n"

SAMPLE2 = "2 4\n8 1 5 8 8 6 2\n1 5 9 8 4 8 5\n"
EXTRA = [  # (种子, M, N, 类型)
    (501, 1, 2, "chain1"), (502, 1, 10, "chain1"), (503, 0, 10, "chain1"), (504, 2, 1, "chain1"),
    (505, 2, 4, "chain2"), (506, 2, 3, "chain2"), (507, 1, 10, "chain2"), (508, 2, 10, "chain2"),
    (509, 2, 10, "gap"), (510, 2, 0, "chain1"), (511, 2, 2, "chain1"), (512, 2, 5, "chain2"),
    (513, 2, 10, "rand"), (514, 2, 7, "rand"), (515, 1, 3, "chain1"), (516, 0, 0, "chain1"),
]

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 20)]  # 尾部 20 组让给下面的定制组，总数仍为 40（catalog 按文件列组）
    cases+=[SAMPLE2]+[gplay(random.Random(sd), m, n, k) for sd, m, n, k in EXTRA]
    cases+=["2 10\n1 1 1 1 1 1 1\n1 1 1 1 1 1 1\n", "2 10\n10 10 10 10 10 10 10\n10 10 10 10 10 10 10\n",
            "2 10\n1 2 3 4 5 6 7\n8 9 10 1 2 3 4\n"]
    assert len(cases) == 40 and len(set(cases)) == 40 and all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()
