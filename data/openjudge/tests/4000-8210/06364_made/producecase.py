import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'n, k = map(int, input().split())\n\nround1 = []\nfor i in range(n):\n    a, b = map(int, input().split())\n    round1.append((a, b, i+1))\n\nround1.sort(key = lambda x : -x[0])\n\nround2 = round1[:k]\n\nround2.sort(key = lambda x : -x[1])\n\nprint(round2[0][2])'
SAMPLE = '5 3\n3 10\n9 2\n5 6\n8 4\n6 5\n'
GENERATOR_NAME = 'g6364'
def g6364(r):
    n=r.randint(2,20); k=r.randint(1,n); a=r.sample(range(1,1000000),n); b=r.sample(range(1,1000000),n)
    return f"{n} {k}\n"+"\n".join(f"{x} {y}" for x,y in zip(a,b))+"\n"

def valid(text):
    """题面：1<=N<=50000，1<=K<=N，1<=Ai,Bi<=1e9；第一轮票数互异，第二轮（前 K 名）票数互异。"""
    try:
        lines = text.split("\n")
        if lines[-1] != "": return False
        lines = lines[:-1]
        head = lines[0].split(" ")
        if len(head) != 2: return False
        n, k = map(int, head)
        if not (1 <= n <= 50000 and 1 <= k <= n): return False
        if len(lines) != n + 1: return False
        rows = []
        for ln in lines[1:]:
            t = ln.split(" ")
            if len(t) != 2 or any(x != str(int(x)) for x in t): return False
            a, b = map(int, t)
            if not (1 <= a <= 10**9 and 1 <= b <= 10**9): return False
            rows.append((a, b))
        if len({a for a, _ in rows}) != n: return False
        top = sorted(rows, reverse=True)[:k]
        return len({b for _, b in top}) == k
    except Exception:
        return False

def extra(r, n, k, lim=10**9, trap=False):
    a = r.sample(range(1, lim + 1), n); b = r.sample(range(1, lim + 1), n)
    if trap and k < n:
        # 全体 B 最大的牛恰好落在第一轮被淘汰的那一批里
        order = sorted(range(n), key=lambda i: -a[i])
        out = order[r.randrange(k, n)]
        j = max(range(n), key=lambda i: b[i]); b[j], b[out] = b[out], b[j]
    return f"{n} {k}\n" + "".join(f"{x} {y}\n" for x, y in zip(a, b))

EXTRA = [
    lambda r: "1 1\n1000000000 1000000000\n",
    lambda r: "2 1\n1 1000000000\n1000000000 1\n",
    lambda r: "2 2\n1 1000000000\n1000000000 1\n",
    lambda r: extra(r, 30, 1, trap=True),
    lambda r: extra(r, 30, 30),
    lambda r: extra(r, 1000, 500, trap=True),
    lambda r: extra(r, 50000, 1, trap=True),
    lambda r: extra(r, 50000, 50000),
    lambda r: extra(r, 50000, 25000, trap=True),
    lambda r: extra(r, 50000, 49999, trap=True),
    lambda r: extra(r, 50000, 50000, lim=50000),
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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=[f(random.Random(1000+i)) for i,f in enumerate(EXTRA)]
    assert all(valid(c) for c in cases)
    assert len(set(cases))==len(cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
